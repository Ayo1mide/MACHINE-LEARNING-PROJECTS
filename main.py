import os
import json
import random

import nltk
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# UNCOMMENT THIS BUT CCOMMENT IT BACK ONCE YOU'VE RUN THE ENTIRE CODE TO AVOID DOWNLOADING THE RESOURCES MORE THAN ONCE
# Download required NLTK resources
#nltk.download('punkt')
#nltk.download('wordnet')


class ChatbotModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(ChatbotModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x
    

class ChatbotAssistant:
    def __init__(self, intents_path, function_mappings=None):
        self.model = None
        self.intents_path = intents_path

        self.documents = []
        self.vocabulary = []
        self.intents = []
        self.responses = {}

        self.function_mappings = function_mappings

        self.X = None
        self.y = None

    @staticmethod
    def tokenize_and_lemmatize(text):
        lemmatizer = nltk.WordNetLemmatizer()
        words = nltk.word_tokenize(text)
        words = [lemmatizer.lemmatize(word.lower()) for word in words]
        return words
    def bag_of_words(self, words):
        return [1 if word in words else 0 for word in self.vocabulary]
    
    def parse_intents(self):
        lemmatizer = nltk.WordNetLemmatizer()

        if os.path.exists(self.intents_path):
            with open(self.intents_path, 'r') as f:
                intents_data = json.load(f)

            for intent in intents_data['intents']:
                if intent['tag'] not in self.intents:
                    self.intents.append(intent['tag'])
                    self.responses[intent['tag']] = intent['responses']

                for pattern in intent['patterns']:
                    pattern_words = self.tokenize_and_lemmatize(pattern)
                    self.vocabulary.extend(pattern_words)
                    self.documents.append((pattern_words, intent['tag']))

            self.vocabulary = sorted(set(self.vocabulary))
    def prepare_data(self):
        bags = []
        indices = []

        for doc in self.documents:
            words = doc[0]
            bag = self.bag_of_words(words)

            intent_index = self.intents.index(doc[1])
            indices.append(intent_index)

            bags.append(bag)

        self.X = np.array(bags)
        self.y = np.array(indices)

    def train_model(self, batch_size=8, epochs=1000, learning_rate=0.001):
        X_tensor = torch.tensor(self.X, dtype=torch.float32)
        y_tensor = torch.tensor(self.y, dtype=torch.long)

        dataset = TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.model = ChatbotModel(self.X.shape[1], len(self.intents))

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)

        for epoch in range(epochs):
            running_loss = 0.0

            for batch_X, batch_y in loader:
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()

            print(f"Epoch {epoch + 1}: Loss: {running_loss / len(loader): .4f}")

    def save_model(self, model_path, dimensions_path):
        torch.save(self.model.state_dict(), model_path)

        with open(dimensions_path, 'w') as f:
            json.dump({'input_size': self.X.shape[1], 'output_size': len(self.intents)}, f)

    def load_model(self, model_path, dimensions_path):
        with open(dimensions_path, 'r') as f:
            dimensions = json.load(f)

        self.model = ChatbotModel(dimensions['input_size'], dimensions['output_size'])
        self.model.load_state_dict(torch.load(model_path), strict=True)

    def chat(self, message):
        words = self.tokenize_and_lemmatize(message)
        bag = self.bag_of_words(words)

        bag_tensor = torch.tensor(bag, dtype=torch.float32)

        self.model.eval()
        with torch.no_grad():
            predictions = self.model(bag_tensor)

        predicted_class_index = torch.argmax(predictions, dim=0).item()
        predicted_intent = self.intents[predicted_class_index]

        if self.function_mappings and predicted_intent in self.function_mappings:
            self.function_mappings[predicted_intent]()

        if self.responses.get(predicted_intent):
            return random.choice(self.responses[predicted_intent])
        else:
            return "I'm sorry, I don't understand."
        

def get_stocks():
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
    return random.sample(stocks, 3)

if __name__ == "__main__":
    # assistant = ChatbotAssistant('intents.json', function_mappings={'stocks': get_stocks})
    # assistant.parse_intents()
    # assistant.prepare_data()
    # assistant.train_model(batch_size=8, epochs=100, learning_rate=0.001)

    # assistant.save_model('chatbot_model.pth', 'model_dimensions.json')
    
    # ----------AFTER TRAINING USE 'CTRL + /' TO COOMENT THE CODES ABOVE BEFORE RUNNING THE CHATBOT--------
    
    assistant = ChatbotAssistant('intents.json', function_mappings={'stocks': get_stocks})
    assistant.parse_intents()
    assistant.load_model('chatbot_model.pth', 'model_dimensions.json')

    while True:
        message = input("You: ")
        if message.lower() == '/quit':
            break

        print("Chatbot:", assistant.chat(message))
