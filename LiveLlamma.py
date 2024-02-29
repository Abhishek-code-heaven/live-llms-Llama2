import streamlit as st
from langchain.llms import CTransformers
from langchain_core.prompts import PromptTemplate
import requests

st.set_page_config(
    page_title="Generate Blogs",
    page_icon= "https://cdn-icons-png.flaticon.com/512/4712/4712035.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.header("Generate Job Description")

input_text = st.text_input("Enter your job description details")

col1, col2 = st.columns([5,5])

def llamma2response(input_text, no_words, description_type):

    llm = CTransformers(model = "C:/Users/Abhishek Vaid/Desktop/session/llama-2-7b-chat.ggmlv3.q8_0.bin",
                        model_type = "llama",
                        config = {"max_new_tokens": 256, "temperature": 0.01})

    template = f"""
    Write a job description for {description_type} job profile for a description {input_text}
    within {no_words} words.
    """
    prompt = PromptTemplate(input_variables= ["description_type","no_words","input_text"], template = template)

    response = llm(prompt.format(description_type=description_type, no_words = no_words, input_text = input_text))

    return response

with col1:
    no_words = st.text_input("Enter the number of words for Job Description")

with col2:
    description_type = st.selectbox("Writing the description for",("Researchers", "Data Scientist", "Data Analyst"), index = 0)

submit = st.button("Generate Blog")

if submit:
    st.write(llamma2response(input_text, no_words, description_type))


st.title('Ask a Flexon Question')

if st.button('Get Flexon company Question'):
    message = {"sender": "test_user", "message": "Give me a Flexon specific question"}
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', json=message)
    if response.status_code == 200:
        flexon_question = response.json()[0]['text']
        st.write(flexon_question)
    else:
        st.write('Failed to get response from Rasa server.')