import json
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter

from query import DataLoader

embeddings = HuggingFaceEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")
text_splitter = RecursiveCharacterTextSplitter()


class llmAgent:
    """ """

    def __init__(self, groq_key: str, data_path: Path) -> None:
        """ """
        self.data_path = data_path
        self.data_loader = DataLoader(data_path=data_path)

        llama_31 = "llama-3.1-70b-versatile"
        llama_tool_70 = 'llama3-groq-70b-8192-tool-use-preview'
        self.llm = ChatGroq(temperature=0, model=llama_31, api_key=groq_key)
        self.llm2 = ChatGroq(temperature=0, model=llama_tool_70, api_key=groq_key)

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
                new_key = key.replace('_', ' ')
                new_obj[new_key] = llmAgent.replace_underscores_in_keys(value)
            return new_obj
        elif isinstance(json_obj, list):
            return [llmAgent.replace_underscores_in_keys(item) for item in json_obj]
        else:
            return json_obj

    def extract_diagnosis(self, encounter_key: str):
        """
        Extraction Agent/Step 1

        Extraction agent for the descrete hospital acquired diagnosis or
        present on admit diagnosis.
        """
        diagnosis_data_dict = self.data_loader.get_diagnosis_data(
            encounter_key=encounter_key
        )

        hospitalAcquiredDx_json = diagnosis_data_dict["hospitalAcquiredDx"]
        presentOnAdmitDx_json = diagnosis_data_dict["presentOnAdmitDx"]

        system = "You are a knowledgeable medical provider who specializes in medication management."
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )

        chain = prompt | self.llm
        response = chain.invoke(
            {
                "text": f"""Based on the information from this JSON information: {hospitalAcquiredDx_json}, {presentOnAdmitDx_json}, does the patient have any of the following:
                    1. Mild to moderate esophagitis
                    2. GERD 
                    3. Peptic Ulcer Disease
                    4. Upper GI symptoms
                    5. ICU Stress Ulcer Prophylaxis
                    6. Barretts Esophagus
                    7. Chronic NSAID use with bleeding risk
                    8. Severe esophagitis
                    9. Documented history of bleeding GI ulcer
                    10. H pylori infection
                    11. Explain the reasoning for your answer with the key being 'Reasoning'
                    Return the answer for each of these as a formatted JSON object with the key being the condition and the value being a boolean value for the first 10.  For the final question, return a string with the reasoning for your answer.

                    """
            }
        )
        return llmAgent.extract_json_from_content(response.content), response.response_metadata['token_usage']['total_tokens']

    def extract_encounter_info(self, encounter_key: str):
        """
        Extraction Agent/Step 2

        Extraction agent for encounter information.
        """
        encounters_json = self.data_loader.get_encounter_data(
            encounter_key=encounter_key
        )

        system = "You are a knowledgeable medical provider who specializes in medication management."
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )

        chain = prompt | self.llm
        response = chain.invoke(
            {
                "text": f"""Based on the information from this JSON information: {encounters_json}, does the patient have any of the following:
                    1. Mild to moderate esophagitis
                    2. GERD 
                    3. Peptic Ulcer Disease
                    4. Upper GI symptoms
                    5. ICU Stress Ulcer Prophylaxis
                    6. Barretts Esophagus
                    7. Chronic NSAID use with bleeding risk
                    8. Severe esophagitis
                    9. Documented history of bleeding GI ulcer
                    10. H pylori infection
                    11. Explain the reasoning for your answer with the key being 'Reasoning'
                    Return the answer for each of these as a formatted JSON object with the key being the condition and the value being a boolean value for the first 10.  For the final question, return a string with the reasoning for your answer.
                    """
            }
        )
        return llmAgent.extract_json_from_content(response.content), response.response_metadata['token_usage']['total_tokens']

    def extract_notes(self, encounter_key: str):
        """
        Extraction Agent/Step 3

        """
        noteText = self.data_loader.get_notes_data(encounter_key=encounter_key)

        from langchain_community.document_loaders import DataFrameLoader

        loader = DataFrameLoader(
            data_frame=noteText,
            page_content_column="NoteText",
            engine="pandas",
        )

        documents = loader.load_and_split()

        from langchain_community.vectorstores import FAISS

        vector_store = FAISS.from_documents(documents, embeddings)

        retriever = vector_store.as_retriever(search_type="similarity", k=5)

        from typing import List
        from langchain.output_parsers import PydanticOutputParser
        from langchain_core.prompts import PromptTemplate
        from pydantic import BaseModel, Field
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnablePassthrough
        
        class NoteResponse(BaseModel):
            Mild_to_moderate_esophagitis: bool = Field(description="Mild to moderate esophagitis")
            GERD: bool = Field(description="GERD")
            Peptic_Ulcer_Disease: bool = Field(description="Peptic Ulcer Disease")
            Upper_GI_symptoms: bool = Field(description="Upper GI symptoms")
            ICU_Stress_Ulcer_Prophylaxis: bool = Field(description="ICU Stress Ulcer Prophylaxis")
            Barretts_Esophagus: bool = Field(description="Barrett's Esophagus")
            Chronic_NSAID_use_with_bleeding_risk: bool = Field(description="Chronic NSAID use with bleeding risk")
            Severe_esophagitis: bool = Field(description="Severe esophagitis")
            Documented_history_of_bleeding_GI_ulcer: bool = Field(description="Documented history of bleeding GI ulcer")
            H_pylori_infection: bool = Field(description="H pylori infection")
            Reasoning: str = Field(description="Explain the reasoning for your answer")

         # You can add custom validation logic easily with Pydantic.
        @classmethod
        def validate_question(cls, value: str) -> str:
            if not value.endswith("?"):
                raise ValueError("Badly formed question!")
            return value
        #parser = PydanticOutputParser(pydantic_object=NoteResponse)

        system = "You are a knowledgeable medical provider who specializes in medication management. Given a list of diagnosis and some snippets from patients notes {context}, answer if the patient notes contain any of the diagnosis."
        parser = PydanticOutputParser(pydantic_object=NoteResponse)
        prompt = PromptTemplate(
                template="Answer the user query.\n{format_instructions}\n{context}\n",
                input_variables=[("system", system), ("human", "{input}")],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )
        #prompt = ChatPromptTemplate.from_messages(
        #    [("system", system), ("human", "{input}")]
        #)

        # # #   Approach 2   # # #
        
        rag_chain = (
            RunnablePassthrough.assign(
                context=(lambda x: llmAgent.format_docs(x["context"]))
            )
            | prompt
            | self.llm
            #| StrOutputParser()
        )

        #retrieve_docs = {
        #    "context": retriever | (lambda x: llmAgent.format_docs(x)),
        #    "input": RunnablePassthrough(),
        #}
        
        retrieve_docs = (lambda x: x["input"]) | retriever
        chain = RunnablePassthrough.assign(context=retrieve_docs).assign(
            answer=rag_chain
        ) 


        result = chain.invoke(
            {
                "input": """Based on the information from the note {context}, does the patient have any of the following:
              1. Mild to moderate esophagitis
              2. GERD 
              3. Peptic Ulcer Disease
              4. Upper GI symptoms
              5. ICU Stress Ulcer Prophylaxis
              6. Barretts Esophagus
              7. Chronic NSAID use with bleeding risk
              8. Severe esophagitis
              9. Documented history of bleeding GI ulcer
              10. H pylori infection
              11. Explain the reasoning for your answer
            Return the answer for each of these as a formatted JSON object with the key being the condition and the value being a boolean value for the first 10.  For the final question, return a string with the reasoning for your answer."""
            }
        )

        # resulting json output
        #try:
        temp_json = llmAgent.extract_json_from_content(result['answer'].content)        
        #temp_json = llmAgent.extract_json_from_content(StrOutputParser(result))
        #except:
        #    rag_chain = (
        #    RunnablePassthrough.assign(
        #        context=(lambda x: llmAgent.format_docs(x["context"]))
        #    )
        #    | prompt
        #    | self.llm2
        #    | StrOutputParser()
        #    )
        #    result = chain.invoke(
        #        {
        #            "input": """Based on the information from the note context, does the patient have any of the following:
        #        1. Mild to moderate esophagitis
        #        2. GERD 
        #        3. Peptic Ulcer Disease
        #        4. Upper GI symptoms
        #        5. ICU Stress Ulcer Prophylaxis
        #        6. Barretts Esophagus
        #        7. Chronic NSAID use with bleeding risk
        #        8. Severe esophagitis
        #        9. Documented history of bleeding GI ulcer
        #        10. H pylori infection
        #        11. Explain the reasoning for your answer with the key being 'Reasoning'
        #        Return the answer for each of these as a formatted JSON object with the key being the condition and the value being a boolean value for the first 10.  For the final question, return a string with the reasoning for your answer.
        #            
        #           """
        #        }
        #        ) 
            #temp_json = llmAgent.extract_json_from_content(result["answer"])
        result_json = llmAgent.replace_underscores_in_keys(temp_json)
        

        return result_json, result['answer'].response_metadata['token_usage']['total_tokens'] #result['answer'], result.response_metadata['token_usage']['total_tokens']
    
    def summarize_reasonings(self, results_dict):
        """Summarize the reasonings from the three sources."""
        diagnosis_dict = results_dict["diagnosis_dict"]
        encounter_dict = results_dict["encounter_dict"]
        notes_dict = results_dict["notes_dict"]
        
        system = "You are a knowledgeable medical provider who specializes in medication management."
        human = "{text}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )

        chain = prompt | self.llm
        response = chain.invoke(
            {
                "text": f"""Based on the following json files, please provide a single explanation of the reasoning given by the 'Reasoning' key. Summarize given equal 
                weight to each. Do not add any additional information, only summarize what is given.
                {diagnosis_dict}
                {encounter_dict}
                {notes_dict}"""
            }
        )
        return response.content
