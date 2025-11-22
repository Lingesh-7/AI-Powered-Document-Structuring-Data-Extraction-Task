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

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

class PDFtoEXCEL:
    def __init__(self):
        self.llm = GoogleGenerativeAI(model="gemini-2.5-pro")
        self.prompt_template = PromptTemplate.from_template(
            """
            From the given text extract all the information as key, value, comment (additional contextual notes)
            in this format:
            [{{'key':'<key>', 'value':'<value>', 'comment':'<comment>'}},{{'key':'<key>', 'value':'<value>', 'comment':'<comment>'}},...]

            {text}

            ## RESPONSE INSTRUCTION:
            1. Retain the exact original wording, sentence structure, and phrasing from the text.
            2. Do not introduce new information and no preamble or unwanted text in the response.
            3. Do not wrap the response in ``` or json or any other formatting. I only want the output as a Python list literal.

            Example:
            text:
            Vijay Kumar was born on March 15, 1989, in Jaipur, Rajasthan, making him 35 years old as of 2024.
            His birthdate is formatted as 1989-03-15 in ISO format for easy parsing, while his age serves as a
            key demographic marker for analytical purposes. Born and raised in the Pink City of India, his
            birthplace provides valuable regional profiling context, and his O+ blood group is noted for
            emergency contact purposes. As an Indian national, his citizenship status is important for
            understanding his work authorization and visa requirements across different employment
            opportunities.

            output:
            [
              {{'key':'First Name', 'value':'Vijay', 'comment':''}},
              {{'key':'Last Name', 'value':'Kumar', 'comment':''}},
              {{'key':'Date of Birth', 'value':'15-Mar-89', 'comment':''}},
              {{'key':'Birth City', 'value':'Jaipur', 'comment':'Born and raised in the Pink City of India, his birthplace provides valuable regional profiling context'}},
              {{'key':'Birth State', 'value':'Rajasthan', 'comment':'Born and raised in the Pink City of India, his birthplace provides valuable regional profiling context'}}
            ]
            """
        )

    def split(self, page_content: str):
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ". ", " ", ""],
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_text(page_content)
        return chunks

    def key_value_extractor(self, chunks):
        """
        chunks: list of strings
        returns: list of lists of dicts (one list per chunk)
        """
        all_results = []
        chain = self.prompt_template | self.llm

        for chunk in chunks:
            # Call LLM
            raw_resp = chain.invoke({"text": chunk})

            # Ensure string
            if not isinstance(raw_resp, str):
                raw_resp = str(raw_resp)

            # Clean common junk
            cleaned = (
                raw_resp
                .replace("```", "")
                .replace("json", "")
                .strip()
            )

            # Convert string representation of list to Python object
            try:
                parsed = ast.literal_eval(cleaned)
            except Exception as e:
                
                continue

            # Make sure it's a list
            if isinstance(parsed, dict):
                parsed = [parsed]

            all_results.append(parsed)

        return all_results

    def convert_to_excel(self, nested_key_value_list):
        """
        nested_key_value_list: list of lists of dicts
        returns: BytesIO buffer with Excel file
        """
        # Flatten list-of-lists into a single list
        flat = []
        for item in nested_key_value_list:
            if isinstance(item, list):
                flat.extend(item)
            elif isinstance(item, dict):
                flat.append(item)

        if not flat:
            return None

        df = pd.DataFrame(flat)

        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        return buffer