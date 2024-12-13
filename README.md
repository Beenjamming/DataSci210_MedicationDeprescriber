# RxReduce: A Medication Deprescribing Agent Framework
## Datasci 210 Capstone Project

### Description
Medication deprescribing application leveraging Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) to evaluate and extract patient diagnosis information, enabling clinicians to make informed patient medication recommendations.

The main branch is currently configured to use Groq for LLM calls.

### Directions
The scripts necessary to run RxReduce may be found in the `src` folder. The script `main.py` may be used to retrieve a patient’s data using an encounter key and call the deprescribing agent to make a recommendation and associated explanation. A Python dictionary is defined in `main.py`, containing recommendations and associated diagnosis information. For a different medication class, this dictionary would need to be updated to include diagnosis information relevant to the medication class being considered.

### Data
Unfortunately, we are not at liberty to share the labeled patient dataset developed from the deidentified patient data provided by the University of California, San Francisco. However, it may be possible to share synthetic patient data in the future.