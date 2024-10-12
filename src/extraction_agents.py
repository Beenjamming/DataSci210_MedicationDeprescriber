import os
import json
import numpy as np
import pandas as pd
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from data_query import DataLoader

base_embeddings = HuggingFaceEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")
text_splitter = RecursiveCharacterTextSplitter()


class LLMAgent:
    """ """

    def __init__(self, groq_key: str, data_path: Path) -> None:
        """ """
        self.data_path = data_path
        self.data_loader = DataLoader(data_path=data_path)

        llama_31 = "llama-3.1-70b-versatile"
        self.llm = ChatGroq(temperature=0, model=llama_31, api_key=groq_key)

    @staticmethod
    def extract_json_from_content(content) -> json:
        """ """
        # Find the JSON part within the content
        start_index = content.find("{")
        end_index = content.rfind("}") + 1
        json_str = content[start_index:end_index]

        # Parse the JSON string
        parsed_json = json.loads(json_str)

        return parsed_json

    def extract_diagnosis(self, encounter_key: str) -> dict:
        """Extraction agent for the descrete hospital acquired diagnosis or
        present on admit diagnosis."""
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
                    1. Mild to moderate esoophagitis
                    2. GERD 
                    3. Peptic Ulcer Disease
                    4. Upper GI symptoms
                    5. ICU Stress Ulcer Prophylaxis
                    6. Barrett's Esophagus
                    7. Chronic NSAID use with bleeding risk
                    8. Severe esophagitis
                    9. Documented history of bleeding GI ulcer
                    10. Explain the reasoning for your answer
                    Return the answer for each of these as a formatted JSON object with the key being the condition and the value being a boolean value for the first 9.  For the final question, return a string with the reasoning for your answer."""
            }
        )
        return LLMAgent.extract_json_from_content(response.content)
    
    def extract_encounter_info(self, encounter_key: str) -> dict:
        """Extraction agent for encounter information."""
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
                    1. Mild to moderate esoophagitis
                    2. GERD 
                    3. Peptic Ulcer Disease
                    4. Upper GI symptoms
                    5. ICU Stress Ulcer Prophylaxis
                    6. Barrett's Esophagus
                    7. Chronic NSAID use with bleeding risk
                    8. Severe esophagitis
                    9. Documented history of bleeding GI ulcer
                    10. Explain the reasoning for your answer
                    Return the answer for each of these as a formatted JSON object with the key being the condition and the value being a boolean value for the first 9.  For the final question, return a string with the reasoning for your answer."""
            }
        )
        return LLMAgent.extract_json_from_content(response.content)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def extract_notes(self, encounter_key: str) -> dict:
        """ """
        from langchain_community.document_loaders import DataFrameLoader
        loader = DataFrameLoader(
        data_frame = noteText,
        page_content_column = "NoteText",
        engine="pandas",
        )

        documents = loader.load_and_split()
        
        import faiss
        from langchain_community.docstore.in_memory import InMemoryDocstore
        from langchain_community.vectorstores import FAISS


        vector_store = FAISS.from_documents(documents, embeddings)
        
        retriever = vector_store.as_retriever(search_type="similarity", k=5)
        
        from langchain_core.documents import Document
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnablePassthrough
        
        rag_chain = (
            {"context": retriever | format_docs,
            "input": RunnablePassthrough()}
            | prompt 
            | llama_3_1
            | StrOutputParser()
        )
