# AI-Powered Document Structuring & Data Extraction Task

This project is an **AI-powered application** that extracts **structured data** from unstructured PDF documents and exports it to Excel.
It uses **LangChain**, **Google Gemini**, and **recursive text chunking** to identify **key-value pairs** along with **contextual comments**.

## Features

* **PDF Parsing**: Extracts text from PDF documents using PyPDFLoader.
* **AI Extraction**: Uses Google Gemini (via LangChain) to intelligently identify data points.
* **Structured Output**: Generates an Excel file with columns: `Key`, `Value`, `Comments`.
* **Streamlit UI**: Simple and user-friendly web interface for uploading PDFs and downloading results.

## Installation

1. Clone the repository.
2. Install dependencies (using uv or pip):

### Using uv (recommended)

```bash
uv add streamlit langchain-community langchain-text-splitters langchain-google-genai pypdf pandas openpyxl python-dotenv
```

### Using pip

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:

### Using uv

```bash
uv run streamlit run app.py
```

### Using pip

```bash
streamlit run app.py
```

2. Open the app in your browser (usually `http://localhost:8501`).
3. Upload the PDF file you want to convert.
4. Click **Convert to Excel** to process the document.
5. Download the generated `output.xlsx` file.

## Dependencies

* `streamlit`
* `langchain-community`
* `langchain-text-splitters`
* `langchain-google-genai`
* `pypdf`
* `pandas`
* `openpyxl`
* `python-dotenv`

## Project Structure

* `app.py`: Main Streamlit application (UI + processing).
* `PDFtoEXCEL`: Class handling PDF parsing, chunking, LLM extraction, and Excel generation.
* `README.md`: Project documentation.
* `.env`: Stores your Google Gemini API key.
* `requirements.txt`: List of dependencies (optional if using uv).


