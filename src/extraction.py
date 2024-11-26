import json
from pathlib import Path

from langchain_community.document_loaders import DataFrameLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import BaseModel, Field



from query import DataLoader

embeddings = HuggingFaceEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")
text_splitter = RecursiveCharacterTextSplitter()

from langchain_core.output_parsers import JsonOutputParser


class DiagnosisSearchDict(BaseModel):
    diagnosis_boolean: str = Field(description="1 if the diagnosis is found, else 0")
    explanation: str = Field(
        description="A concise explanation for how the determination of the diagnosis was made"
    )


class NoteResponse(BaseModel):
    """Pydantic class for the diagnosis jsons."""

    Mild_to_moderate_esophagitis: bool = Field(
        description="Mild to moderate esophagitis"
    )
    GERD: bool = Field(description="GERD")
    Peptic_Ulcer_Disease: bool = Field(description="Peptic Ulcer Disease")
    Upper_GI_symptoms: bool = Field(description="Upper GI symptoms")
    ICU_Stress_Ulcer_Prophylaxis: bool = Field(
        description="ICU Stress Ulcer Prophylaxis"
    )
    Barretts_Esophagus: bool = Field(description="Barrett's Esophagus")
    Chronic_NSAID_use_with_bleeding_risk: bool = Field(
        description="Chronic NSAID use with bleeding risk"
    )
    Severe_esophagitis: bool = Field(description="Severe esophagitis")
    Documented_history_of_bleeding_GI_ulcer: bool = Field(
        description="Documented history of bleeding GI ulcer"
    )
    H_pylori_infection: bool = Field(description="H pylori infection")
    Reasoning: str = Field(description="Explain the reasoning for your answer")


class llmAgent:
    """ """

    def __init__(self, groq_key: str, data_path: Path) -> None:
        """ """
        self.data_path = data_path
        self.data_loader = DataLoader(data_path=data_path)

        # cascade of LLMs
        llama_31_70b = "llama-3.1-70b-versatile"
        llama_32_90b = "llama-3.2-90b-vision-preview"
        self.llm = ChatGroq(temperature=0, model=llama_31_70b, api_key=groq_key)

        # llama_tool_70 = "llama3-groq-70b-8192-tool-use-preview"
        # self.llm2 = ChatGroq(temperature=0, model=llama_tool_70, api_key=groq_key)

    @staticmethod
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    @staticmethod
    def extract_json_from_content(content):
        """ """
        # Find the JSON part within the content
        start_index = content.find("{")
        end_index = content.rfind("}") + 1
        json_str = content[start_index:end_index]

        # Parse the JSON string
        parsed_json = json.loads(json_str)

        return parsed_json

    @staticmethod
    def replace_underscores_in_keys(json_obj):
        if isinstance(json_obj, dict):
            new_obj = {}
            for key, value in json_obj.items():
                new_key = key.replace("_", " ")
                new_obj[new_key] = llmAgent.replace_underscores_in_keys(value)
            return new_obj
        elif isinstance(json_obj, list):
            return [llmAgent.replace_underscores_in_keys(item) for item in json_obj]
        else:
            return json_obj
        
    def set_retriever(self, noteText):
        
        loader = DataFrameLoader(
            data_frame=noteText,
            page_content_column="NoteText",
            engine="pandas",
        )
        documents = loader.load_and_split()
        vector_store = FAISS.from_documents(documents, embeddings)
        self.retriever = vector_store.as_retriever(search_type="similarity", k=5)

    # @staticmethod
    def get_bool(output):
        """ """
        bo = False
        if output in [0, "0", "0", "F", "False"]:
            bo = False
        elif output in [1, "1", "1", "T", "True"]:
            bo = True
        else:
            print(f"Issue parsing {output} into Boolean...")

        return bo

    def get_data(self, encounter_key: str, source: str):
        """Return the data given an encounter_key."""
        if source == "diagnosis":
            # diagnosis_data_dict
            data = self.data_loader.get_diagnosis_data(encounter_key=encounter_key)
        elif source == "encounters":
            # encounters_data_dict
            data = self.data_loader.get_encounter_data(encounter_key=encounter_key)
        elif source == "notes":
            # noteText
            data = self.data_loader.get_notes_data(encounter_key=encounter_key)

        return data

    def extract_without_RAG(self, data_dict, diagnosis_searched_for):
        """ """
        parser = JsonOutputParser(pydantic_object=DiagnosisSearchDict)

        prompt = PromptTemplate(
            template="""You are a knowledgeable medical provider who specializes in medication management. In the following case, your patient is prescribed
            a PPI (proton pump inhibitor) and need to make a decision to continue, reduce, or stop the PPI. Determine if there is evidence of the specific
            condition which will help determine whether to continue, reduce, or stop the medication on discharge.
            # Response Format Instructions #
            {format_instructions}
            # Question #
            {query}""",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm

        output = chain.invoke(
            {
                "query": f"Based on the provided information here: {data_dict}, is there evidence of {diagnosis_searched_for}? Do NOT assume a condition based on prescribed medication. We know all of these patients are prescribed a ppi, but we need to know why. Be very sure of a diagnosis."
            }
        )

        token_count = output.response_metadata["token_usage"]["total_tokens"]
        output_dict = parser.parse(output.content)

        return output_dict, token_count

    def extract_RAG(self, diagnosis_searched_for: str):
        """
        Extraction Agent/Step 3

        """

        parser = JsonOutputParser(pydantic_object=DiagnosisSearchDict)

        prompt = PromptTemplate(
            template="""You are a knowledgeable medical provider who specializes in medication management. In the following case, your patient is prescribed a PPI (proton pump inhibitor) and need to make a decision to continue, reduce, or stop the PPI. Determine if there is evidence of the specific condition which will help determine whether to continue, reduce, or stop the medication on discharge.
            Use the Context as information for your answer: 
            # Context #
            {context}
            Do NOT assume a condition based on prescribed medication. We know all of these patients are prescribed a ppi, but we need to know why. Be very sure of a diagnosis.
            # Format Instructions #
            {format_instructions}
            # Question #
            {query}
            """,
            input_variables=["context", "query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        rag_chain = (
            {
                "context": self.retriever | llmAgent.format_docs,
                "query": RunnablePassthrough(),
            }
            | prompt
            | self.llm
        )

        rag_chain_output = rag_chain.invoke(
            f"Is there evidence of {diagnosis_searched_for}?"
        )

        token_count = rag_chain_output.response_metadata["token_usage"]["total_tokens"]
        output_dict = parser.parse(rag_chain_output.content)

        return output_dict, token_count

    def summarize_reasonings(self, recommendation_str, search_history_so_far):
        """Summarize a final explanation for the recommendation."""
        system = "You are a knowledgeable medical provider who specializes in medication management."
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )

        chain = prompt | self.llm
        chain_result = chain.invoke(
            {
                "text": f"""Medications can either be continued, deprescribed, or stopped. 
                The recommendation ({recommendation_str}) was given because the diagnosis ({list(search_history_so_far.keys())[-1]}) was found in the patient's data. 
                Provide a short and concise summary of the recommendation and the explanation for the recommendation: {search_history_so_far}. 
                Provide your answer in a single line of text."""
            }
        )
        return chain_result.content, chain_result.response_metadata["token_usage"][
            "total_tokens"
        ]
