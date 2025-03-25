
import os  
import base64

from openai import AzureOpenAI  
from dotenv import load_dotenv

MAX_TOKENS = 10000

class AzureOpenAITranslate:
    _client: AzureOpenAI
    _prompt: str = f'''
        Please translate the entire text verbatim to English
    '''

    def __init__(self):
        self._prepare()

    def _prepare(self):
        # load env
        load_dotenv()
        endpoint = os.getenv("ENDPOINT_URL")  
        self.deployment = os.getenv("DEPLOYMENT_NAME", "o3-mini")  
        subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

        # Initialize Azure OpenAI Service client with key-based authentication    
        self._client = AzureOpenAI(  
            azure_endpoint=endpoint,  
            api_key=subscription_key,  
            api_version="2024-12-01-preview",
        )

    # Translate with the given deployment
    def translate(self, file_contents):
        chunks = self._split_text_into_chunks(file_contents)
        batch_results = []

        # Process each chunk with OpenAI API
        for chunk in chunks:
            response_text = self.chat(self._prompt + chunk)
            batch_results.append(response_text)

        # Combine results from all batches
        final_result = " ".join(batch_results)
        
        # response from prompt one
        return final_result

    # Read the file contents
    def read_file(self, path=""):
        if path == "": path = self._file_path
        file_contents = ""

        # Read the file contents
        with open(path, 'r') as f:
            file_contents = f.read()
        return file_contents
    
    def chat(self, prompt):
        print(prompt)
        try:
            res1 = self._client.chat.completions.create(
                model = self.deployment,
                messages = [{'role': 'user', 'content': prompt}]
            )
        except Exception as e:
            print(f"Error: {e}")

        return res1.choices[0].message.content

    def _split_text_into_chunks(self, file_contents):
        tokens = file_contents.split() # Poor man's splitter
        chunk_size = MAX_TOKENS - 100  # Leave space for the model's response
        chunks = []

        for i in range(0, len(tokens), chunk_size):
            chunk = tokens[i:i + chunk_size]
            chunks.append(" ".join(chunk))

        return chunks