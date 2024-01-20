import boto3
import markdown

from bs4 import BeautifulSoup
from typing import List, Dict
from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


class MachineGeneratorApp:
    def __init__(
        self,
        model_id: str,
        streaming: bool,
        callbacks: List,
        model_kwargs: Dict,
        verbose: bool = True,
    ):
        """
        Initialize the DataGeneratorApp.

        Args:
            model_id (str): Identifier for the machine learning model.
            streaming (bool): Flag indicating whether to use streaming mode.
            callbacks (List): List of callbacks for the machine learning model.
            model_kwargs (Dict): Additional keyword arguments for the machine learning model.
            verbose (bool): Flag indicating whether to display verbose information.
        """
        # Initialize Bedrock client
        self.client = boto3.client("bedrock-runtime")

        # Initialize Bedrock model
        self.llm = Bedrock(
            model_id=model_id,
            streaming=streaming,
            callbacks=callbacks,
            model_kwargs=model_kwargs,
            client=self.client,
        )

        # Initialize ConversationChain for generating synthetic machine signals
        self.conversation = ConversationChain(
            llm=self.llm, verbose=verbose, memory=ConversationBufferMemory()
        )

        # Set the default prompt template for data generation
        default_prompt = """
            Generate a NUMBERED list of at least {number} different {industry} manufacturing machines.
            IMPORTANT: Fence the list with '```'. DO NOT add any explanations, only the machine name.
        """
        self.prompt = PromptTemplate(
            template=default_prompt,
            input_variables=["number", "industry"],
        )

    def get_client(self) -> None:
        """Get the Bedrock client."""
        return self.client

    def get_llm(self) -> None:
        """Get the Bedrock model."""
        return self.llm

    def get_conversation(self) -> None:
        """Get the ConversationChain instance."""
        return self.conversation

    def get_prompt(self) -> None:
        """Get the current prompt template."""
        return self.prompt

    def set_client(self, client: boto3.client) -> None:
        """Set the Bedrock client."""
        self.client = client

    def set_llm(
        self,
        model_id: str,
        streaming: bool,
        callbacks: List,
        model_kwargs: Dict,
    ) -> None:
        """
        Set the Bedrock model.

        Args:
            model_id (str): Identifier for the machine learning model.
            streaming (bool): Flag indicating whether to use streaming mode.
            callbacks (List): List of callbacks for the machine learning model.
            model_kwargs (Dict): Additional keyword arguments for the machine learning model.
        """
        self.llm = Bedrock(
            model_id=model_id,
            streaming=streaming,
            callbacks=callbacks,
            model_kwargs=model_kwargs,
            client=self.client,
        )

    def set_conversation(self, verbose: bool) -> None:
        """
        Set the ConversationChain instance.

        Args:
            verbose (bool): Flag indicating whether to display verbose information.
        """
        self.conversation = ConversationChain(
            llm=self.llm, verbose=verbose, memory=ConversationBufferMemory()
        )

    def set_prompt(self, prompt_template: str, input_vars: List) -> None:
        """
        Set the prompt template for data generation.

        Args:
            prompt_template (str): The new prompt template.
            input_vars (List): List of input variables for the prompt.
        """
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=input_vars,
        )

    def _predict(self, **kwargs) -> str:
        """
        Generate a prediction using the current prompt.

        Args:
            kwargs: Keyword arguments to fill in the prompt template.

        Returns:
            str: The generated prediction.
        """
        output = self.conversation.predict(input=self.prompt.format(**kwargs))
        return output

    def predict_list(self, **kwargs) -> str:
        """
        Generate and extract an array from the prediction.

        Args:
            kwargs: Keyword arguments to fill in the prompt template.

        Returns:
            str: The generated array.
        """
        the_list = self._predict(**kwargs)
        html = markdown.markdown(the_list, extensions=["fenced_code"])
        soup = BeautifulSoup(html, features="lxml")
        the_list = soup.find("code").get_text()
        items = []
        for line in the_list.splitlines():
            items.append(
                line.replace("- ", "")
                .split(". ")[-1]
                .split(": ")[0]
                .split(" - ")[0]
            )
        return items
