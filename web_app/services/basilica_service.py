import os
import basilica
from dotenv import load_dotenv


load_dotenv()
BASILICA_API_KEY = os.getenv("BASILICA_API_KEY")
connection = basilica.Connection(BASILICA_API_KEY)

if __name__ == "__main__":
    sentences = ["Hello world!", "How are you?"]
    embeddings = connection.embed_sentences(sentences)
    print(list(embeddings))
