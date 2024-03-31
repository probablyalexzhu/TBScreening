import json
from flask import Flask, request
from pathlib import Path
from report-generator import generate_report
import langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain import OpenAI, LLMChain
from langchain.prompts import Prompt
import os
from langchain.text_splitter import Language
from google.cloud import aiplatform
from langchain_google_vertexai import VertexAI
from vertexai.language_models import CodeGenerationModel
from langchain_community.llms import VertexAI
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import RetrievalQA
import os
from langchain.schema.document import Document
from langchain.chains import ConversationChain, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.prompts import QA_PROMPT
from langchain.prompts.chat import SystemMessagePromptTemplate,HumanMessagePromptTemplate
from vertexai.preview.generative_models import GenerativeModel
from vertexai.generative_models._generative_models import HarmCategory, HarmBlockThreshold, ResponseBlockedError
import google.generativeai as genai
from google.cloud import secretmanager
import warnings
from google.cloud import aiplatform
import vertexai
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.schema.runnable import RunnableMap
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferMemory

notes = []
memory = []

def access_secret_version(secret_version_id):
  client = secretmanager.SecretManagerServiceClient()
  response = client.access_secret_version(name=secret_version_id)
  return response.payload.data.decode('UTF-8')

## HERE IS THE PROJECT NUMBER, NOT NAME --  GET WITH: gcloud projects list

credential_path = '/Users/aryans0921/Downloads/oval-relic-418817-4dfc7520a574.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

secret_version_id = f"projects/19770672095/secrets/GOOGLE_APPLICATION_CREDENTIALS/versions/1"

key=access_secret_version(secret_version_id)
# os.getenv(key)

## HERE IS THE PROJECT NAME
vertexai.init(project='oval-relic-418817', location='us-central1')

import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')

EMBEDDING_QPM = 100
EMBEDDING_NUM_BATCH = 5
embeddings = VertexAIEmbeddings(
    requests_per_minute=EMBEDDING_QPM,
    num_instances_per_batch=EMBEDDING_NUM_BATCH,
    model_name = "textembedding-gecko",max_output_tokens=512,
temperature=0.1,
top_p=0.8,
top_k=40
)

text_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,chunk_size=2000, chunk_overlap=500
)

docs = WikipediaLoader(query="Tuberculosis in India", load_max_docs=3).load()
docs += WikipediaLoader(query="Tuberculosis", load_max_docs=2).load() 

paan_doc = {
    'page_content': "Tuberculosis (TB) accounts for the highest number of mortalities among infectious diseases worldwide. Laryngeal TB is an extremely rare presentation of TB. It has many similarities to laryngeal carcinoma, one of the three most common cancers among males in the city, with an age standardized rate of 8.6. The associated risk factors of laryngeal carcinoma i.e. smoking, paan, betel nut usage and alcohol use also tend to be concentrated in the same demographic background as that of TB, creating a diagnostic dilemma. We present a case of granulomatous laryngeal TB, in a 40 year old male, with characteristic presenting features of laryngeal carcinoma i.e. persistent hoarseness and weight loss. He had no associated symptoms of fever, night sweats, cough or dysphagia, nor did he have any history of tobacco or irritant use. There was no history of tuberculosis (TB) contact. He was initially worked up for laryngeal carcinoma; however laryngoscopic biopsy revealed laryngeal TB. We present this case to emphasize the point that although primary laryngeal tuberculosis is a rarity, it must not be overlooked as a possibility when evaluating dysphonia and/or considering laryngeal carcinoma.",
    'source': 'https://pubmed.ncbi.nlm.nih.gov/22755382/'
}
disease_doc = {
    'page_content': "Elderly age (odds ratio [OR] 2.68-8.09), Eastern residence (OR 2.01), positive sputum bacteriology (OR 2.54), abnormal chest X-ray (OR 2.28), and comorbidity with chronic kidney disease (OR 2.35), stroke (OR 1.74) or chronic liver disease (OR 1.29) were most likely to be the cause of TB-specific deaths, whereas cancer (OR 0.79) was less likely to be implicated. For non-TB-specific deaths in patients younger than 65 years of age, male sex (OR 2.04) and comorbidity with HIV (OR 5.92), chronic kidney disease (OR 8.02), stroke (OR 3.75), cancer (OR 9.79), chronic liver disease (OR 2.71) or diabetes mellitus (OR 1.38) were risk factors.",
    'source': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4348515/'
}
xdr_doc = {
    'page_content': "A total of 392 XDR-TB cases were initiated on second-line standardized treatment under PMDT in 201384. Subsequently, 939 XDR-TB cases including Ofx-resistant cases were detected among 2184 MDR-TB cases from January to September 201485. Of the 939 XDR-TB cases, 879 (93.6%) were treated with standardized treatment. According to the current report, 2130 XDR-TB cases were registered and initiated on treatment in 2015 with maximum cases belonging to Maharashtra (899), Gujarat (288) and Delhi (166)77. The WHO has recently introduced standardized as well as individualized regimens in managing MDR and XDR-TB patients based on the recent classification69 as shown in Table IV.",
    'source': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5555056/'
}
machine_learning_doc = {
    'page_content': "TB is an opportunistic infection (OI). OIs are infections that occur more often or are more severe in people with weakened immune systems than in people with healthy immune systems. HIV weakens the immune system, increasing the risk of TB in people with HIV. Infection with both HIV and TB is called HIV/TB coinfection. Untreated latent TB infection is more likely to advance to TB disease in people with HIV than in people without HIV. In people with HIV, TB disease is considered an AIDS-defining condition. AIDS-defining conditions are infections and cancers that are life-threatening in people with HIV. Treatment with HIV medicines is called antiretroviral therapy (ART). HIV medicines protect the immune system and prevent HIV from advancing to acquired immunodeficiency syndrome (AIDS). In people with HIV and latent TB infection, treatment with HIV and TB medicines reduces the chances that latent TB infection will advance to TB disease.",
    'source': 'https://hivinfo.nih.gov/understanding-hiv/fact-sheets/hiv-and-tuberculosis-tb'
}
deep_learning_doc = {
    'page_content': "The WHO has recently introduced standardized as well as individualized regimens in managing MDR and XDR-TB patients based on the recent classification69 as shown in Table IV. The standardized regimen includes a 9-12 month regimen for MDR-TB and a 20-24 month regimen for XDR-TB. The individualized regimen is based on the drug susceptibility test results and includes a minimum of 18 months of treatment for MDR-TB and a minimum of 24 months of treatment for XDR-TB. The WHO has also introduced a shorter regimen for MDR-TB, which includes 9-12 months of treatment with a combination of bedaquiline, pretomanid, linezolid, and moxifloxacin.",
    'source': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5555056/'
}
neural_networks_doc = {
    'page_content': "The high prevalence of DM and TB being in epidemic proportions has rightly earned them the names ‘the converging epidemics’ and ‘double burden’ (11,12). Due to rapid changes in lifestyle, urbanization, and epidemiological changes, DM is increasingly seen in low- and medium-income groups, and in younger individuals more frequently than before. The prevalence of DM is increasing faster where TB is endemic already. Unfortunately, these are the regions in the world where health care facilities are less common. According to International Diabetes Federation, the 50-55% increase in the prevalence of DM over the next 2 decades will occur predominantly in the continent of Africa (10). A longitudinal, multi-national study involving low-income countries concluded that an odds ratio of 4.7 for prevalence and 8.1 for incidence of TB is highly likely in those counties where DM has increased over the last decade (13).",
    'source': 'https://www.ncbi.nlm.nih.gov/books/NBK570126/'
}
treatment_doc = {
    'page_content': "The standardized regimen includes a 9-12 month regimen for MDR-TB and a 20-24 month regimen for XDR-TB. The individualized regimen is based on the drug susceptibility test results and includes a minimum of 18 months of treatment for MDR-TB and a minimum of 24 months of treatment for XDR-TB. The WHO has also introduced a shorter regimen for MDR-TB, which includes 9-12 months of treatment with a combination of bedaquiline, pretomanid, linezolid, and moxifloxacin.",
    'source': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5555056/'
}
diagnosis_doc = {
    'page_content': "The diagnosis of TB in people with HIV is more difficult than in people without HIV. TB symptoms are similar to symptoms of other diseases that occur more often in people with HIV. In addition, people with HIV are more likely to have TB in parts of the body other than the lungs. These forms of TB are called extrapulmonary TB. Extrapulmonary TB can affect the lymph nodes, abdomen, brain, bones, and other parts of the body. Extrapulmonary TB can be difficult to diagnose because the symptoms are not specific to TB. The diagnosis of TB in people with HIV is based on a combination of medical history, physical examination, chest X-ray, and laboratory tests. The most common laboratory test for TB is the sputum test. The sputum test is used to detect TB bacteria in the lungs. The sputum test is not always accurate in people with HIV. Other tests for TB include the tuberculin skin test, the interferon-gamma release assay, and the chest X-ray. These tests are used to detect TB bacteria in the body. The diagnosis of TB in people with HIV is based on a combination of medical history, physical examination, chest X-ray, and laboratory tests. The most common laboratory test for TB is the sputum test. The sputum test is used to detect TB bacteria in the lungs. The sputum test is not always accurate in people with HIV. Other tests for TB include the tuberculin skin test, the interferon-gamma release assay, and the chest X-ray. These tests are used to detect TB bacteria in the body.",
    'source': 'https://hivinfo.nih.gov/understanding-hiv/fact-sheets/hiv-and-tuberculosis-tb'
}
region_doc ={
    'page_content': "As per the national TB prevalence survey, for every one lakh population in India, there are 199 TB patients. Going by the prevalence rate, Maharashtra, with its 12.87 crore population, is expected to have 2.5 lakh TB patients. Of these, almost 1 lakh seek care from private doctors, and the rest go to state and municipal corporation-run health units.",
    'source': 'https://timesofindia.indiatimes.com/city/pune/maharashtra-intensifies-focus-on-private-health-sector-to-eliminate-tb/articleshow/99544076.cms'
}

for doc in [paan_doc, disease_doc, xdr_doc, machine_learning_doc, deep_learning_doc, neural_networks_doc, treatment_doc, diagnosis_doc, region_doc]:
    docs.append(Document(page_content = doc['page_content'], source = doc['source']))

vectorstore = DocArrayInMemorySearch.from_documents(docs, embedding = embeddings)

model = VertexAI(
        temperature=0.15, model_name='gemini-1.0-pro', max_output_tokens=2000
    )

retriever = vectorstore.as_retriever()

template = """Hey there! Let's have a friendly chat. I'm here to assist you. Answer the question in 5 sentences, keeping it simple and easy to understand. Feel free to share any info related to your question, and I'll do my best to help. If you mention cold sweats, I'd love to know when you experience them during the day. By the way, as we talk, I'll gently collect some key details like your name, age, gender, location, symptoms, and recent experiences. Don't worry, it'll be part of our natural conversation.
{context}

Remember, there's no such thing as too much information when it comes to helping you out! Share your question, and I'll be here to support you!
{question}

This is our previous conversation and answers:
{conversation_history}
"""
prompt = ChatPromptTemplate.from_template(template)

output_parser = StrOutputParser()
from langchain.schema.document import Document

def ML(current_question, chat_history):
    def get_full_context(question):
        context = retriever.get_relevant_documents(question)
        if chat_history:
            memory_docs = [Document(page_content=entry) for entry in chat_history]
            conv_history = memory_docs
        else:
            conv_history = ""

        return context, conv_history

    chain = RunnableMap({
        "context": lambda x: get_full_context(x["question"])[0],
        "question": lambda x: x["question"],
        "conversation_history": lambda x: get_full_context(x["question"])[1]
    }) | prompt | model | output_parser

    # Invoke the chain with the input question
    result = chain.invoke({"question": current_question})

    return result

model = VertexAI(
    temperature=0.15, model_name='gemini-1.0-pro', max_output_tokens=2000
)

summary_template = """
Given the following conversation between a patient and a medical professional, extract only the requested information. Your task is to identify and provide only the specific information as requested in the question. If the question asks for age, gender, name, or location, provide only that information and only that information.

Question: {question}

"""

# Initialize an empty list to store extracted information
extracted_info = []

# Define prompts for each type of information extraction
prompts = {
    'Date': "Extract the date from the following text:",
    'Age': "Extract the age from the following text:",
    'Gender': "Extract the gender from the following text:",
    'Location': "Extract the location from the following text:",
    'AI_Patient_Summary': "Extract the AI patient summary from the following text:"
}

# Iterate through question-answer pairs
summary_model = VertexAI(
    temperature=0.15, model_name='gemini-1.0-pro', max_output_tokens=2000
)

def generate_report_1():
    concat_string = ". ".join(memory)
    new_dict = dict()
    for key, value in prompts.items():
        prompt = f"{value}\n{concat_string}"
        res = summary_model.generate_content(prompt)
        new_dict[key] = res[0]
        print(res)
    return generate_report(new_dict['Name'], new_dict['Age'], new_dict['Gender'], new_dict['Location'], new_dict['AI_Patient_Summary'], None)


# --------------------------------- FLASK SECTION ---------------------------------

app = Flask(__name__)

@app.route('/send-data', methods=['POST'])
def receive_data():
    global notes
    notes = request.json  # Get the JSON data from the request
    print("Received data:", notes)
    return "Data received successfully"

# Members API Route : pass data from backend to frontend
@app.route("/members")
def members():
    global notes
    print("members is membering!!!!")
    return notes

# Generate model response for the frontend
@app.route("/response")
def response():
    global memory
    memory.append("Question: " + request.json)
    # respond to question_memory[-1], use the rest as memory of previous question/answer pairs
    response = ML(memory[-1], memory[:-1])
    print("response is responding!!!!")
    memory.append("Answer: " + response)
    return response

# Generate report


if __name__ == "__main__":
    # switch to port 8000 for mac, because 5000 is taken by control centre
    app.run(port=8000, debug=True)