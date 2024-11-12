import json
from pathlib import Path

from langchain.output_parsers import PydanticOutputParser
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

from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate


class DiagnosisSearchDict(BaseModel):
    diagnosis_boolean: str = Field(
        description="True if the diagnosis is found, else False"
    )
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

    def search(self, encounter_key: str, diagnosis: str):
        """Search for a diagnosis given an encounter key and source."""
        # search diagnosis source data
        diagnosis_data_dict = self.get_data(
            encounter_key=encounter_key, source="diagnosis"
        )
        diagnosis_dict = self.extract_diagnosis(
            diagnosis_data_dict=diagnosis_data_dict, diagnosis=diagnosis
        )
        # search encounter source data
        encounters_data_dict = self.get_data(
            encounter_key=encounter_key, source="encounters"
        )
        encounter_dict = self.extract_encounter(
            encounters_data_dict=encounters_data_dict, diagnosis=diagnosis
        )
        # search note source data
        noteText = self.get_data(encounter_key=encounter_key, source="notes")
        notes_dict = self.extract_notes(noteText=noteText, diagnosis=diagnosis)

        # package dictinoaries into dictionary
        diagnosis_dict = {
            "diagnosis": diagnosis_dict,
            "encounters": encounter_dict,
            "notes": notes_dict,
        }
        # token_count = diagnosis_token_count + encounter_token_count + notes_token_count

        return diagnosis_dict  # , token_count, notes_context

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

    def extract_diagnosis(self, diagnosis_data_dict: dict, diagnosis: str):
        """
        Extraction Agent/Step 1

        Extraction agent for the descrete hospital acquired diagnosis or
        present on admit diagnosis.
        """
        parser = JsonOutputParser(pydantic_object=DiagnosisSearchDict)

        prompt = PromptTemplate(
            template="You are a knowledgeable medical provider who specializes in medication management. In the following case, your patient is prescribed a PPI (proton pump inhibitor) and need to make a decision to continue, reduce, or stop the PPI. Determine if there is evidence of the specific condition which will help determine whether to continue, reduce, or stop the medication on discharge.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        output_dict = chain.invoke(
            {
                "query": f"Based on the provided information here: {diagnosis_data_dict}, is there evidence of {diagnosis}? Do NOT assume a condition based on prescribed medication. We know all of these patients are prescribed a ppi, but we need to know why. Be very sure of a diagnosis."
            }
        )

        return output_dict

    def extract_encounter(self, encounters_data_dict: dict, diagnosis: str):
        """
        Extraction Agent/Step 2

        Extraction agent for encounter information.
        """
        parser = JsonOutputParser(pydantic_object=DiagnosisSearchDict)

        prompt = PromptTemplate(
            template="You are a knowledgeable medical provider who specializes in medication management. In the following case, your patient is prescribed a PPI (proton pump inhibitor) and need to make a decision to continue, reduce, or stop the PPI. Determine if there is evidence of the specific condition which will help determine whether to continue, reduce, or stop the medication on discharge.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser

        output_dict = chain.invoke(
            {
                "query": f"Based on the provided information here: {encounters_data_dict}, is there evidence of {diagnosis}? Do NOT assume a condition based on prescribed medication. We know all of these patients are prescribed a ppi, but we need to know why. Be very sure of a diagnosis."
            }
        )

        return output_dict

    def extract_notes(self, noteText, diagnosis: str):
        """
        Extraction Agent/Step 3

        """
        loader = DataFrameLoader(
            data_frame=noteText,
            page_content_column="NoteText",
            engine="pandas",
        )

        documents = loader.load_and_split()

        vector_store = FAISS.from_documents(documents, embeddings)

        retriever = vector_store.as_retriever(search_type="similarity", k=5)

        parser = JsonOutputParser(pydantic_object=DiagnosisSearchDict)

        prompt = PromptTemplate(
            template="You are a knowledgeable medical provider who specializes in medication management. In the following case, your patient is prescribed a PPI (proton pump inhibitor) and need to make a decision to continue, reduce, or stop the PPI. Determine if there is evidence of the specific condition which will help determine whether to continue, reduce, or stop the medication on discharge.\n{format_instructions}\nUse this information for your answer: {context}\n{query}\n",
            input_variables=["context", "query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        rag_chain = (
            {
                "context": retriever | llmAgent.format_docs,
                "query": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | parser
        )

        chain_result = rag_chain.invoke(
            f"Is there evidence of {diagnosis}? Do NOT assume a condition based on prescribed medication. We know all of these patients are prescribed a ppi, but we need to know why. Be very sure of a diagnosis."
        )

        return chain_result

    def summarize_reasonings(self, recommendation_str, diagnosis_dict_dict):
        """Summarize a final explanation for the recommendation."""
        system = "You are a knowledgeable medical provider who specializes in medication management."
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )

        chain = prompt | self.llm
        chain_result = chain.invoke(
            {
                "text": f"""Medications can either be continued, deprescribed, or stopped. The recommendation ({recommendation_str}) was given because the diagnosis ({list(diagnosis_dict_dict.keys())[-1]}) was found in the patient's data. Provide a short and concise summary of the recommendation and the explanation for the recommendation: {diagnosis_dict_dict}. Provide your answer in a single line of text."""
            }
        )
        return chain_result.content, chain_result.response_metadata["token_usage"][
            "total_tokens"
        ]
