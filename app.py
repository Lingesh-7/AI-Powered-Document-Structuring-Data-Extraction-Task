import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAI
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import tempfile
import ast
from io import BytesIO
from lang_helper import PDFtoEXCEL

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")




st.set_page_config(page_title="AI-Powered Document Structuring & Data Extraction Task", page_icon="📄")
st.title("AI-Powered Document Structuring & Data Extraction Task")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if st.button("Convert to Excel"):
    if uploaded_file is None:
        st.warning("Please upload a PDF file")
    else:
        with st.spinner("Reading PDF..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                temp_pdf_path = tmp.name

            # Load PDF using PyPDFLoader
            loader = PyPDFLoader(temp_pdf_path)
            documents = loader.load()

        st.success(f"Extracted {len(documents)} pages from PDF!")

        # Instantiate converter
        converter = PDFtoEXCEL()

        # Split all pages into chunks
        all_chunks = []
        for doc in documents:
            page_chunks = converter.split(doc.page_content)
            all_chunks.extend(page_chunks)

        st.write(f"Total chunks to process: {len(all_chunks)}")

        with st.spinner("Extracting key-value-comment data using LLM..."):
            nested_results = converter.key_value_extractor(all_chunks)
            excel_buffer = converter.convert_to_excel(nested_results)

        if excel_buffer is None:
            st.error("No structured data was extracted. Check the prompt or model output.")
        else:
            st.success("Conversion completed!")
            st.download_button(
                label="Download Excel",
                data=excel_buffer,
                file_name="output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
