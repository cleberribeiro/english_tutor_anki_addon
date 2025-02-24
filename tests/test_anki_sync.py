import unittest
from unittest.mock import patch, MagicMock
from english_tutor_gpt_addon.anki_sync import create_card, show_message_safe

# FILE: tests/test_anki_sync.py


class TestAnkiSync(unittest.TestCase):

    @patch('english_tutor_gpt_addon.anki_sync.requests.post')
    @patch('english_tutor_gpt_addon.anki_sync.show_message_safe')
    def test_create_card_success(self, mock_show_message_safe, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": 123, "error": None}
        mock_post.return_value = mock_response

        result = create_card("basic", {"Front": "What is the capital of France?", "Back": "Paris"})
        
        self.assertEqual(result, 123)
        mock_show_message_safe.assert_called_once_with("Card criado com sucesso!")

    @patch('english_tutor_gpt_addon.anki_sync.requests.post')
    @patch('english_tutor_gpt_addon.anki_sync.show_message_safe')
    def test_create_card_model_not_supported(self, mock_show_message_safe, mock_post):
        result = create_card("unsupported_model", {"Front": "What is the capital of France?", "Back": "Paris"})
        
        self.assertIsNone(result)
        mock_show_message_safe.assert_called_once_with("Erro: Modelo 'unsupported_model' não suportado.", True)
        mock_post.assert_not_called()

    @patch('english_tutor_gpt_addon.anki_sync.requests.post')
    @patch('english_tutor_gpt_addon.anki_sync.show_message_safe')
    def test_create_card_anki_connect_error(self, mock_show_message_safe, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": None, "error": "Some error"}
        mock_post.return_value = mock_response

        result = create_card("basic", {"Front": "What is the capital of France?", "Back": "Paris"})
        
        self.assertIsNone(result)
        mock_show_message_safe.assert_called_once_with("Erro do AnkiConnect: Some error", True)

    @patch('english_tutor_gpt_addon.anki_sync.requests.post')
    @patch('english_tutor_gpt_addon.anki_sync.show_message_safe')
    def test_create_card_connection_error(self, mock_show_message_safe, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        result = create_card("basic", {"Front": "What is the capital of France?", "Back": "Paris"})
        
        self.assertIsNone(result)
        mock_show_message_safe.assert_called_once_with("Erro de conexão com AnkiConnect: Connection error", True)

    @patch('english_tutor_gpt_addon.anki_sync.requests.post')
    @patch('english_tutor_gpt_addon.anki_sync.show_message_safe')
    def test_create_card_json_decode_error(self, mock_show_message_safe, mock_post):
        mock_response = MagicMock()
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        mock_post.return_value = mock_response

        result = create_card("basic", {"Front": "What is the capital of France?", "Back": "Paris"})
        
        self.assertIsNone(result)
        mock_show_message_safe.assert_called_once_with("Erro ao decodificar resposta do AnkiConnect", True)

if __name__ == '__main__':
    unittest.main()