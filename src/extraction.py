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
import time
from botocore.exceptions import ClientError

from langchain_aws import ChatBedrock

from query import DataLoader

embeddings = HuggingFaceEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")
text_splitter = RecursiveCharacterTextSplitter()


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
        llama_31 = "llama-3.1-70b-versatile"
        #model = "llama-3.1-70b-versatile"
        model = 'meta.llama3-70b-instruct-v1:0'
        #self.llm = ChatGroq(temperature=0, model=llama_31, api_key=groq_key)

        self.llm = ChatBedrock(
            model_id=model,
            model_kwargs=dict(temperature=0),
            # other params...
        )

        # llama_tool_70 = "llama3-groq-70b-8192-tool-use-preview"
        # self.llm2 = ChatGroq(temperature=0, model=llama_tool_70, api_key=groq_key)
    def set_encounter_key(self, encounter_key: str):
        self.encounter_key=encounter_key
    
    def set_retriever(self):
        noteText = self.data_loader.get_notes_data(encounter_key=self.encounter_key)
        
        loader = DataFrameLoader(
            data_frame=noteText,
            page_content_column="NoteText",
            engine="pandas",
        )
        documents = loader.load_and_split()
        vector_store = FAISS.from_documents(documents, embeddings)
        self.retriever = vector_store.as_retriever(search_type="similarity", k=5)

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

        # pydantic parser
        # parser = PydanticOutputParser(pydantic_object=NoteResponse)

        system = "You are a knowledgeable medical provider who specializes in medication management."
        human = "{input}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), ("human", human)]
        )
        # prompt = PromptTemplate(
        #     template="Answer the user query.\n{format_instructions}\nFormat your response as a json as directed.",
        #     input_variables=[("system", system), ("human", human)],
        #     partial_variables={"format_instructions": parser.get_format_instructions()},
        # )

        chain = prompt | self.llm

        # chain_result = chain.invoke(
        #     {
        #         "input": f"""Based on the information from this JSON information: {hospitalAcquiredDx_json}, {presentOnAdmitDx_json}, does the patient have any of the following:
        #             1. Mild to moderate esophagitis
        #             2. GERD
        #             3. Peptic Ulcer Disease
        #             4. Upper GI symptoms
        #             5. ICU Stress Ulcer Prophylaxis
        #             6. Barretts Esophagus
        #             7. Chronic NSAID use with bleeding risk
        #             8. Severe esophagitis
        #             9. Documented history of bleeding GI ulcer
        #             10. H pylori infection
        #             11. Explain the reasoning for your answer with the key being 'Reasoning'
        #             Return the answer for each of these as a formatted JSON object with the key being the condition and the value being a boolean value for the first 10.  For the final question, return a string with the reasoning for your answer.
        #             """
        #     }
        # )
        chain_result = chain.invoke(
            {
                "input": f"""Based on the information from this JSON information: {hospitalAcquiredDx_json}, {presentOnAdmitDx_json}, does the patient have any of the following:
                    Mild to moderate esophagitis
                    GERD 
                    Peptic Ulcer Disease
                    Upper GI symptoms
                    ICU Stress Ulcer Prophylaxis
                    Barretts Esophagus
                    Chronic NSAID use with bleeding risk
                    Severe esophagitis
                    Documented history of bleeding GI ulcer
                    H pylori infection
                    Explain the reasoning for your answer with the key being 'Reasoning'
                    Return the answer for each of these as a formatted JSON object with the key being the condition and the value being a boolean value for the first 10.  For the final question, return a string with the reasoning for your answer.
                    """
            }
        )
        return (
            llmAgent.extract_json_from_content(chain_result.content),
            chain_result.response_metadata["token_usage"]["total_tokens"],
        )

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
        # chain_result = chain.invoke(
        #     {
        #         "text": f"""Based on the information from this JSON information: {encounters_json}, does the patient have any of the following:
        #             1. Mild to moderate esophagitis
        #             2. GERD
        #             3. Peptic Ulcer Disease
        #             4. Upper GI symptoms
        #             5. ICU Stress Ulcer Prophylaxis
        #             6. Barretts Esophagus
        #             7. Chronic NSAID use with bleeding risk
        #             8. Severe esophagitis
        #             9. Documented history of bleeding GI ulcer
        #             10. H pylori infection
        #             11. Explain the reasoning for your answer with the key being 'Reasoning'
        #             Return the answer for each of these as a formatted JSON object with the key being the condition and the value being a boolean value for the first 10.  For the final question, return a string with the reasoning for your answer.
        #             """
        #     }
        # )
        chain_result = chain.invoke(
            {
                "text": f"""Based on the information from this JSON information: {encounters_json}, does the patient have any of the following:
                    Mild to moderate esophagitis
                    GERD 
                    Peptic Ulcer Disease
                    Upper GI symptoms
                    ICU Stress Ulcer Prophylaxis
                    Barretts Esophagus
                    Chronic NSAID use with bleeding risk
                    Severe esophagitis
                    Documented history of bleeding GI ulcer
                    H pylori infection
                    Explain the reasoning for your answer with the key being 'Reasoning'
                    Return the answer for each of these as a formatted JSON object with the key being the condition and the value being a boolean value for the first 10.  For the final question, return a string with the reasoning for your answer.
                    """
            }
        )
        return (
            llmAgent.extract_json_from_content(chain_result.content),
            chain_result.response_metadata["token_usage"]["total_tokens"],
        )

    def extract_notes(self, encounter_key: str):
        """
        Extraction Agent/Step 3

        """
        noteText = self.data_loader.get_notes_data(encounter_key=encounter_key)

        loader = DataFrameLoader(
            data_frame=noteText,
            page_content_column="NoteText",
            engine="pandas",
        )

        documents = loader.load_and_split()

        vector_store = FAISS.from_documents(documents, embeddings)

        retriever = vector_store.as_retriever(search_type="similarity", k=5)

        # Pydantic example
        # You can add custom validation logic easily with Pydantic.
        # @classmethod
        # def validate_question(cls, value: str) -> str:
        #     if not value.endswith("?"):
        #         raise ValueError("Badly formed question!")
        #     return value

        # parser = PydanticOutputParser(pydantic_object=NoteResponse)

        system = "You are a knowledgeable medical provider who specializes in medication management. Given a list of diagnosis and some snippets from patients notes {context}, answer if the patient notes contain any of the diagnosis."
        parser = PydanticOutputParser(pydantic_object=NoteResponse)
        prompt = PromptTemplate(
            template="Answer the user query.\n{format_instructions}\n{context}\n",
            input_variables=[("system", system), ("human", "{input}")],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        rag_chain = (
            RunnablePassthrough.assign(
                context=(lambda x: llmAgent.format_docs(x["context"]))
            )
            | prompt
            | self.llm
        )

        retrieve_docs = (lambda x: x["input"]) | retriever
        chain = RunnablePassthrough.assign(context=retrieve_docs).assign(
            answer=rag_chain
        )

        chain_result = chain.invoke(
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
        # try:
        temp_json = llmAgent.extract_json_from_content(chain_result["answer"].content)
        # temp_json = llmAgent.extract_json_from_content(StrOutputParser(result))
        # except:
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
        # temp_json = llmAgent.extract_json_from_content(result["answer"])
        result_json = llmAgent.replace_underscores_in_keys(temp_json)

        # returning the pydantic json and token count (int)
        return (
            result_json,
            chain_result["answer"].response_metadata["token_usage"]["total_tokens"],
            chain_result["context"],
        )

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
        chain_result = chain.invoke(
            {
                "text": f"""Based on the following json files, please provide a single explanation of the reasoning given by the 'Reasoning' key. Summarize given equal 
                weight to each. Do not add any additional information, only summarize what is given.
                {diagnosis_dict}
                {encounter_dict}
                {notes_dict}"""
            }
        )
        return chain_result.content, chain_result.response_metadata["token_usage"]["total_tokens"]

    def invoke_with_retry(self, chain, input_data, max_retries=5):
        """Invoke the chain with a retry mechanism for throttling errors."""
        for attempt in range(max_retries):
            try:
                return chain.invoke(input_data)
            except ClientError as e:
                if e.response['Error']['Code'] == 'ThrottlingException':
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"ThrottlingException encountered. Waiting for {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                else:
                    raise  # Re-raise if it's not a throttling error
        raise Exception("Max retries exceeded for invoking the model.")
    
    
    def extract_notes_individual(self, encounter_key: str):
        """
        Extraction Agent/Step 3 - Individual Processing
        Processes each diagnosis separately through the RAG chain for more focused analysis
        """

        

        
        # Define the diagnoses to check
        diagnoses = {
            # "Mild_to_moderate_esophagitis": "Mild to moderate esophagitis",
            # "GERD": "GERD",
            "continue": {"Barretts_Esophagus": "Barrett's Esophagus",
                "Chronic_NSAID_use_with_bleeding_risk": "Chronic NSAID use with bleeding risk",
                "Severe_esophagitis": "Severe esophagitis",
                "Documented_history_of_bleeding_GI_ulcer": "Documented history of bleeding GI ulcer"
                },
            "stop": {
                "Peptic_Ulcer_Disease": "Peptic Ulcer Disease",
                "Upper_GI_symptoms": "Upper GI symptoms",
                "ICU_Stress_Ulcer_Prophylaxis": "ICU Stress Ulcer Prophylaxis",
                "H_pylori_infection": "H pylori infection"
                }
        }
        
        system = """You are a knowledgeable medical provider who specializes in medication management. In the following case, your patient is prescribed a PPI (proton pump inhibitor) and need to make a decisions to continue, reduce, or stop the PPI.
        Given the patient notes <notes> {context} </notes>, determine if there is evidence of the specific condition which will help determine whether to continue, reduce, or stop the medication on discharge. """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", "Based on the provided notes, is there evidence of {condition}? Do NOT assume a condition based on prescribed medication. We know all of these patients are prescribed a ppi, but we need to know why. Be very sure of a diagnosis. Respond with a simple 'yes' or 'no', followed by a brief explanation.")
        ])
        
        rag_chain = (
            RunnablePassthrough.assign(
                context=(lambda x: llmAgent.format_docs(x["context"]))
            )
            | prompt
            | self.llm
        )
        
        retrieve_docs = (lambda x: x["input"]) | self.retriever
        chain = RunnablePassthrough.assign(context=retrieve_docs).assign(
            answer=rag_chain
        )
        
        results = {}
        relevant_contexts = {}
        should_break = False  # Add flag variable
        recommendation = 'deprescribe'
        diag = ''

        for recc_type, conditions in diagnoses.items():
            if should_break:  # Check flag at start of outer loop
                break
                
            for key, condition in conditions.items():
                print(condition)
                chain_result = self.invoke_with_retry(chain,{
                    "input": condition,
                    "condition": condition
                })
                
                response = chain_result["answer"].content.strip().lower()
                print(response)
                #print(response)
                is_positive = "yes" in response[:5]
                results[key] = is_positive
                
                if is_positive:
                    relevant_contexts[key] = chain_result["context"]
                    recommendation = recc_type
                    diag = condition
                    should_break = True  # Set flag when condition met
                    print(f"{self.encounter_key}:rec:{recommendation},{response}")
                    break  # Break inner loop
                

                        # Print the formatted prompt
                formatted_prompt = prompt.format(
                    context=llmAgent.format_docs(chain_result["context"]),
                    condition=condition
                )
                #print("\nComplete Prompt:")
                #print(formatted_prompt)

        return recommendation, response, results, diag, relevant_contexts
        
       