# English Tutor Anki Addon

## Overview
The English Tutor Anki Addon is designed to help users create Anki cards using AI. This addon integrates with AnkiConnect to automate the creation of flashcards, making it easier to build your language learning deck.

## Features
- Create Anki cards using predefined models.
- Supports multiple card models: Basic, Basic (and reversed card), Cloze, Basic (type in the answer).
- Safe message display using Anki's UI thread.
- Simple HTTP server to handle card creation requests.

## Requirements
- Python 3.9
- Anki 2.1+
- AnkiConnect
- Requests library

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/english_tutor_gpt_addon.git
    ```
2. Navigate to the project directory:
    ```sh
    cd english_tutor_gpt_addon
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Start Anki.
2. The addon will automatically initialize and start the server.
3. Use the HTTP server to create cards by sending POST requests to [http://localhost:8766](http://_vscodecontentref_/1).

## Configuration
You can configure the addon by modifying the [config.json](http://_vscodecontentref_/2) file. Currently, the file is empty, but you can add your configurations as needed.

## Running Tests
To run the unit tests, use the following command:
```sh 
python -m unittest discover -s tests
```
## Project Structure
```
english_tutor_gpt_addon/
├── __init__.py
├── anki_sync.py
├── check_dependencies.py
├── config.json
├── manifest.json
├── meta.json
├── README.md
├── requirements.txt
├── server.py
└── tests/
    ├── test__init__.py
    ├── test_anki_sync.py
    └── test_server.py
```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or suggestions, please contact Cleber Ribeiro at cleber.ramos.ribeiro@gmail.com.