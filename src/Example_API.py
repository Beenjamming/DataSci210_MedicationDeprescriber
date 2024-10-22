# 1. Library imports
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from IPython.display import Markdown, display
from extraction import llmAgent
from ppi_deprescribe import merge_results, ppi_deprescribe
import os 
from pathlib import Path 
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

path = os.getenv("datapath")
groq = os.getenv("groqkey")

@app.get('/')
def index():
    #add link to documentation
    link = 'http://127.0.0.1:8000/docs'
    content = f'''<h1>Rx Deprescribe API</h1>
            <h2>Click <a href={link}>here</a> to view the API documentation</h2>
                ''' 
    return HTMLResponse(content=content)   

@app.get('/Deprescribe')
def deprescribe(key):
    # extract information
    llm_agent = llmAgent(groq_key=groq, data_path=path)

    results_dict = {
        "diagnosis_dict": llm_agent.extract_diagnosis(encounter_key=key),
        "encounter_dict": llm_agent.extract_encounter_info(encounter_key=key),
        # Is the reasoning in the json or sepearte?
        # Should the reasoning be included in any of them or just the diangosis with the reasoning seperate?
        "notes_dict": llm_agent.extract_notes(encounter_key=key),
    }
    print(results_dict['notes_dict'])
    # # #   master formatter step   # # #
    # merge the diagnosis booleans (just use OR logic for now)
    # make a final "reasoning" behind the recommendation
    final_dict = merge_results(results_dict=results_dict)

    # feed the three reasonings to LLM to get a single summary
    final_reasoning = llm_agent.summarize_reasonings(results_dict=results_dict)

    # # #   get recommendation from PPI algorithm   # # #
    recommendation_str = ppi_deprescribe(patient_diagnosis=final_dict)
    return recommendation_str, final_reasoning
    #print("Recommendation: ")
    #print(recommendation_str)
    #print("\nReasoning: ")
    #print(final_reasoning)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)