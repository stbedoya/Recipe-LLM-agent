import unittest
from unittest.mock import patch
from pydantic import SecretStr
from src.llm.openai_llm import OpenAILLM


class TestOpenAILLM(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        """Set up the test environment before each test."""
        self.api_key = SecretStr("dummy_api_key")
        self.model_name = "gpt-3.5-turbo"
        self.temperature = 0.7
        self.max_tokens = 1000
        self.openai_llm = OpenAILLM(
            model_name=self.model_name,
            api_key=self.api_key,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

    @patch("src.llm.openai_llm.ChatOpenAI.__init__")
    async def test_initialization(self, MockChatOpenAI_init):
        """Test that the OpenAILLM class is initialized correctly."""

        MockChatOpenAI_init.return_value = None

        openai_llm_instance = OpenAILLM(
            model_name=self.model_name,
            api_key=self.api_key,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        self.assertEqual(openai_llm_instance.model_name, self.model_name)
        self.assertEqual(openai_llm_instance.temperature, self.temperature)
        self.assertEqual(openai_llm_instance.max_tokens, self.max_tokens)
        self.assertEqual(
            openai_llm_instance.api_key.get_secret_value(), "dummy_api_key"
        )

    @patch("src.llm.openai_llm.ChatOpenAI.invoke")
    async def test_generate_response_success(self, MockInvoke):
        """Test the generate_response method when OpenAI returns a successful response."""
        MockInvoke.return_value = "Mocked response"
        response = await self.openai_llm.generate_response("Hello!")
        self.assertEqual(response, "Mocked response")
        MockInvoke.assert_called_once_with("Hello!", **{})

    @patch("src.llm.openai_llm.ChatOpenAI.invoke")
    async def test_generate_response_failure(self, MockInvoke):
        """Test the generate_response method when OpenAI fails (raises exception)."""
        MockInvoke.side_effect = Exception("API error")

        with self.assertRaises(ValueError):
            await self.openai_llm.generate_response("Hire me, please!")


if __name__ == "__main__":
    unittest.main()
