import unittest
from unittest.mock import patch, MagicMock
from english_tutor_gpt_addon import test_add_card, init_addon

# FILE: tests/test___init__.py


class TestInit(unittest.TestCase):

    @patch('english_tutor_gpt_addon.create_card')
    def test_test_add_card(self, mock_create_card):
        test_add_card()
        mock_create_card.assert_called_once_with("basic", {
            "Front": "What is the capital of France?",
            "Back": "Paris"
        })

    @patch('english_tutor_gpt_addon.mw')
    @patch('english_tutor_gpt_addon.run_server')
    @patch('english_tutor_gpt_addon.QAction')
    @patch('english_tutor_gpt_addon.qconnect')
    def test_init_addon(self, mock_qconnect, mock_QAction, mock_run_server, mock_mw):
        mock_action = MagicMock()
        mock_QAction.return_value = mock_action
        mock_menuTools = MagicMock()
        mock_mw.form.menuTools = mock_menuTools

        init_addon()

        mock_QAction.assert_called_once_with("Test AI Sync", mock_mw)
        mock_qconnect.assert_called_once_with(mock_action.triggered, test_add_card)
        mock_menuTools.addAction.assert_called_once_with(mock_action)
        mock_run_server.assert_called_once()

if __name__ == '__main__':
    unittest.main()