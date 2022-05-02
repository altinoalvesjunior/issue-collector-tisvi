from pymongo import MongoClient
import certifi


class Mongo:
    CONNECTION_STRING = "[INSER YOUR CONNECTION STRING]"
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    db = client["[INSER YOUR DB NAME HERE]"]
    collection = db["[INSER YOUR COLLECTION NAME HERE]"]

    def insert_one_repository(self, value):
        self.collection.insert_one(value)
        print('Repositório inserido!\n', value)

    def remove_repository(self, repo_name):
        self.collection.delete_many(repo_name)
        print(f'Repositório: {repo_name} removido com sucesso!')
