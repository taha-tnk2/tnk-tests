# Libraries
import numpy as np
import tiktoken
from openai import OpenAI

"""
A simple wrapper for the open ai's client to abstract repetitive functionality
"""
class ClientWrapper():

    # The secret key for this project.
    OPENAI_API_KEY = "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"

    # Initializes the class.
    def __init__(self, limit = True):
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)

        # The parameters of the model can be swapped between a limited and more thorough setting.
        self.limit = limit
        self.response_model = "gpt-4" if self.limit == False else "gpt-3.5-turbo"
        self.embedding_model = "text-embedding-ada-002" if self.limit == False else "text-embedding-3-small"
        self.token_model = "cl100k_base"

    # Gets a response based on a prompt.
    def get_response(self, prompt):
        response = self.client.chat.completions.create(
            model=self.response_model,
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
        return response
    
    def get_message(self, response):
        message = response.choices[0].message.content
        return message

    # Embeds the given text.
    def get_embedding(self, text):
        text = text.replace("\n", " ")
        embedding = self.client.embeddings.create(input = [text], model=self.embedding_model).data[0].embedding
        return embedding

    def get_tokens(self, text):
        encoding = tiktoken.get_encoding(self.token_model)
        num_tokens = len(encoding.encode(text))
        return num_tokens
    
def main():
    client = ClientWrapper(True)

    prompt = "Tell me a joke"
    token_cost = client.get_tokens(prompt)
    print("Prompt: " + prompt + ", costing " + str(token_cost) + " Tokens")

    response = client.get_response(prompt)
    message = client.get_message(response)
    print("Message back: " + message)

if __name__ == "__main__":
    main()