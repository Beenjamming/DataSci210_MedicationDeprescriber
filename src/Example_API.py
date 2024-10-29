# 1. Library imports
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from extraction import llmAgent
from ppi_deprescribe import merge_results, ppi_deprescribe

app = FastAPI()
path = Path("F:/LangChain/data")
groq = os.environ["groqkey"]


@app.get("/")
def index():
    # add link to documentation
    link = "http://127.0.0.1:8000/docs"
    content = f"""<h1>Rx Deprescribe API</h1>
            <h2>Click <a href={link}>here</a> to view the API documentation</h2>
                """
    return HTMLResponse(content=content)


@app.get("/Deprescribe")
def deprescribe(encounter_key):
    """_summary_

    Parameters
    ----------
    encounter_key : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    # extract information
    llm_agent = llmAgent(groq_key=groq, data_path=path)

    diagnosis_json, diagnosis_token_count = llm_agent.extract_diagnosis(
        encounter_key=encounter_key
    )
    encounter_json, encounter_token_count = llm_agent.extract_encounter_info(
        encounter_key=encounter_key
    )
    # NOTE notes_context is a list of Document objects for RAGAs metrics
    notes_json, notes_token_count, notes_context = llm_agent.extract_notes(
        encounter_key=encounter_key
    )

    results_dict = {
        "diagnosis_dict": diagnosis_json,
        "encounter_dict": encounter_json,
        "notes_dict": notes_json,
    }

    # print(results_dict['notes_dict'])

    # # #   master formatter step   # # #
    # merge the diagnosis booleans (just use OR logic for now)
    # make a final "reasoning" behind the recommendation
    final_dict = merge_results(results_dict=results_dict)

    # feed the three reasonings to LLM to get a single summary
    final_reasoning, reasoning_summary_token_count = llm_agent.summarize_reasonings(
        results_dict=results_dict
    )

    # count tokens used by LLM queries
    total_token_count = (
        diagnosis_token_count
        + encounter_token_count
        + notes_token_count
        + reasoning_summary_token_count
    )

    # # #   get recommendation from PPI algorithm   # # #
    recommendation_str = ppi_deprescribe(patient_diagnosis=final_dict)

    return recommendation_str, final_reasoning, total_token_count


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
