
# Chatbot with NLP and PyTorch

This project is a chatbot application built using PyTorch for training a machine learning model that classifies user input into predefined intents. The chatbot utilizes Natural Language Processing (NLP) techniques, including tokenization, lemmatization, and word embeddings, to respond to users with predefined responses or invoke functions based on the user's query.

## Installation

Follow these steps to install and run the project.

### Prerequisites

- Python 3.x
- Install the required dependencies using the `requirements.txt` file.

### Steps

1. Clone the repository:
    ```bash
    git clone  https://github.com/Ayo1mide/MACHINE-LEARNING-PROJECTS.git
    ```

2. Navigate to the project directory:
    ```bash
    cd chatbot-nlp-pytorch
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Download the necessary NLTK resources:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('wordnet')
    ```

### Troubleshooting

If you encounter the following error:
```
ModuleNotFoundError: No module named 'nltk'
```
**Solution**: In VS Code, press `Ctrl+Shift+P` to open the command palette, and then select the appropriate Python interpreter (e.g., `python.exe`) to resolve the issue.

## Usage

Once the setup is complete, you can run the chatbot.

1. Prepare your intents data in a JSON file (`intents.json`), and make sure to include your predefined patterns, responses, and any functions you'd like the chatbot to invoke.
   
2. Train the model:
    ```python
    assistant = ChatbotAssistant('intents.json', function_mappings={'stocks': get_stocks})
    assistant.parse_intents()
    assistant.prepare_data()
    assistant.train_model(batch_size=8, epochs=100, learning_rate=0.001)
    assistant.save_model('chatbot_model.pth', 'model_dimensions.json')
    ```

3. Start chatting with the bot:
    ```python
    assistant.load_model('chatbot_model.pth', 'model_dimensions.json')

    while True:
        message = input("You: ")
        if message.lower() == '/quit':
            break

        print("Chatbot:", assistant.chat(message))
    ```

## Features

- **Intent Classification**: Classifies user input into one of the predefined intents.
- **Custom Function Invocation**: Trigger custom functions (e.g., fetching stock prices).
- **Pre-trained Embeddings**: Optionally use word embeddings like GloVe for improved NLP.
- **Easy Integration**: Simple interface to add new intents and responses.

## Contributing

We welcome contributions! If you'd like to help improve the project, please fork the repository, create a new branch, and submit a pull request.

## Improvements
- addition of glove nlp to replace bag of words using 6billions words file

## License

This project is licensed under the MIT License - 

## Contacts

Email: ayojoshua11411@gmail.com
Github : https://github.com/Ayo1mide
