import logging
from langchain_openai import ChatOpenAI


class OpenAILLM:
    """Class for interacting with OpenAI's GPT models via Langchain's ChatOpenAI."""

    def __init__(
        self,
        model_name: str,
        api_key: str,
        temperature: float = 0,
        max_tokens: int = 1000,
    ):
        """
        Initializes the OpenAI LLM with required parameters via Langchain's ChatOpenAI.

        Args:
            model_name (str): The OpenAI model to use (e.g., "gpt-3.5-turbo", "gpt-4").
            api_key (str): The API key for authenticating with OpenAI.
            temperature (float, optional): Sampling temperature, default is 0.7.
            max_tokens (int, optional): The maximum number of tokens to generate, default is 100.
            **kwargs: Any additional parameters for further customization.
        """
        self.model_name = model_name
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.llm = ChatOpenAI(
            model=self.model_name,
            api_key=self.api_key,
            temperature=self.temperature,
            max_completion_tokens=self.max_tokens,
        )

    async def generate_response(self, prompt: str, **kwargs):
        """
        Generate a response based on the provided prompt.

        Args:
            prompt (str): The prompt to send to the OpenAI API.
            **kwargs: Any additional parameters to pass to the API call.

        Returns:
            str: The generated response from the model.
        """
        try:
            return self.llm.invoke(prompt, **kwargs)
        except Exception as e:
            logging.error(f"OpenAI API request failed: {e}")
            raise ValueError(f"Failed to generate response from OpenAI: {e}")
