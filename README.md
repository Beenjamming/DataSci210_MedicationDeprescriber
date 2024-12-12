# RxReduce: A Medication Deprescribing Agent Framework
## Datasci 210 Capstone Project

### Description
Medication deprescribing application leveraging Large Language Models (LLMs) and Retrieval Augmented Generation (RAG) to evaluate and extract patient diagnosis information to enable clinicians to make informed patient medication recommendations.

The main branch is currently configured to use Groq to make LLM calls.

### Directions
The scripts necessary to run RxReduce may be found in the src folder. The script main.py may be used to retrieve a patients data using an encounter key and call the deperscribing agent to make a recommendation and associated explanation. A python dictionary is defiend in main.py containing recommendations and associated diagnosis information. For a different medication class, this dictionary would be changed to contain diagnosis information relevant to the medication class considered.

### Data
Unforunately we are not at liberity to share the labeled patient dataset developed from the deidentified patient data provided by the University of Califnoria, San Fransisco. It may be possible to share synthetic patient data in the future.

GoogleDrive Folder: https://drive.google.com/drive/folders/1PX8pTgWNC4u1_lPhzhS_tVMaPwuiaryJ

