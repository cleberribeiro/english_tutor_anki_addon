from unittest import TestCase
from unittest.mock import patch, MagicMock
from english_tutor_gpt_addon.server import run_server, SafeHTTPServer, RequestHandler

class TestServer(TestCase):

    @patch('english_tutor_gpt_addon.server.show_message_safe')
    @patch('english_tutor_gpt_addon.server.SafeHTTPServer')
    def test_run_server_success(self, mock_SafeHTTPServer, mock_show_message_safe):
        mock_httpd = MagicMock()
        mock_SafeHTTPServer.return_value = mock_httpd

        run_server()

        mock_SafeHTTPServer.assert_called_once_with(('127.0.0.1', 8766), RequestHandler)
        mock_httpd.serve_forever.assert_called_once()
        mock_show_message_safe.assert_called_once_with("Servidor do Add-on iniciado na porta 8766")

    @patch('english_tutor_gpt_addon.server.show_message_safe')
    @patch('english_tutor_gpt_addon.server.SafeHTTPServer')
    def test_run_server_exception(self, mock_SafeHTTPServer, mock_show_message_safe):
        mock_SafeHTTPServer.side_effect = Exception("Test exception")

        run_server()

        mock_SafeHTTPServer.assert_called_once_with(('127.0.0.1', 8766), RequestHandler)
        mock_show_message_safe.assert_called_once_with("Erro ao iniciar servidor: Test exception", True)