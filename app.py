## For this popplrt need to be installed 


## I was facing issue with poppler so I decided to use PyPDF2 and it is in main.py




from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import io 
import base64
import pdf2image
from PIL import Image


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Load and Get Response from Model
def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(pdf_file):
    if pdf_file is not None:

        ## converting Pdf to image 
        images = pdf2image.convert_from_bytes(pdf_file.read(),poppler_path='/usr/local/bin')

        first_page = images[0]

        ## converting image to bytes
        img_bytes = io.BytesIO()
        first_page.save(img_bytes,format ='png')
        img_bytes = img_bytes.getvalue()

        pdf_parts = [ {
            'mime_file': 'image/png',
             # encode to base64
            'data': base64.b64encode(img_bytes).decode()
        }]

        return pdf_parts
    else:
        raise FileNotFoundError('No PDF file found')
    
## Initialize st app
    

st.set_page_config(page_title="ATS Resume")
st.header("Application Tracking System")
input_text=st.text_area("Job Description: ",key="input")
pdf_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if pdf_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("Percentage match")

submit3 = st.button("How Can I Improvise my Resume")


input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

input_prompt3 = """
As a skilled ATS (Applicant Tracking System) scanner with expertise in data science and ATS functionality, 
your task is to provide insights on how to improve a resume. What suggestions do you have for enhancing my resume?
"""

if submit1:
    if pdf_file is not None:
        pdf_content=input_pdf_setup(pdf_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit2:
    if pdf_file is not None:
        pdf_content=input_pdf_setup(pdf_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")


elif submit3:
    if pdf_file is not None:
        pdf_content=input_pdf_setup(pdf_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")





