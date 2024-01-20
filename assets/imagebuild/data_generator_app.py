import re
import os
import boto3
import shutil
import markdown
import logging

from bs4 import BeautifulSoup
from typing import List, Dict
from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)


class DataGeneratorApp:
    """
    A class for generating synthetic machine signals data and implementing a simple machine learning model for failure prediction.

    # file: data_generator_app.py - start
    """

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
Write a high-quality {language} script for the following task, something a {context} {language} expert would write. You are writing code for an experienced developer so only add comments for things that are non-obvious. Make sure to include any imports required.

NEVER write anything before the ```{language}``` block. After you are done generating the code and after the ```{language}``` block, check your work VERY CAREFULLY to make sure there are no mistakes, errors, or inconsistencies. It's IMPORTANT that if there are ERRORS, LIST THOSE ERRORS in <error> tags, then GENERATE a new version with those ERRORS FIXED. If there are no errors, write "CHECKED: NO ERRORS" in <error> tags.

Here is the task:
<task>
* Write code to generate synthetic {question} data using ACTUAL and REALISTIC physical signal names and values
* Add some occasional anomalies to the signals that are created
* The first column is `Timestamp` in the format `yyyy-MM-dd HH:mm:ss`
* The `Timestamp` is collected every minute and the dataset should span an entire year
* Write a `main` function that executes the data generation and saves the entire data to local disk. Make sure the file contains the headers!
* Use object-oriented programming for all code and add docstrings
</task>
"""
        self.prompt = PromptTemplate(
            template=default_prompt,
            input_variables=["context", "question", "language"],
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

    def predict_code(self, **kwargs) -> str:
        """
        Generate and extract code from the prediction.

        Args:
            kwargs: Keyword arguments to fill in the prompt template.

        Returns:
            str: The generated code.
        """
        code = self._predict(**kwargs)
        html = markdown.markdown(code, extensions=["fenced_code"])
        soup = BeautifulSoup(html, features="lxml")
        soup.error.decompose()
        code = soup.find("code").get_text()
        return code

    def write_parsed_code(self, code: str, dir: str) -> None:
        """
        Write the parsed code to a folder.

        Args:
            code: The generated code.
            dir: The directory that is created and used to store the content.
        """
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)
        with open(f"{dir}/main.py", "w") as f:
            f.write(code)


def create_directory_string(machine: str):
    """
    Create a repository string

    Args:
        machine: A generated machine name.

    Return:
        str: The directory for the files as string.
    """
    return (
        re.sub("[^a-zA-Z \n\.]", "", machine.lower()).strip().replace(" ", "-")
    )


def create_bash_script(machines: List, s3_bucket: str, user_id: str) -> None:
    """
    Create a bash script to be executed by CodeBuild.

    Args:
        machines: A list of generated machine dataset codes.
        s3_bucket: The Amazon S3 bucket data will be sent to
    """
    script = """
#!/bin/bash

export AnException=100
export AnotherException=101

execute_python() {
    echo "Starting the script at " `date`
    cd $1
    python main.py
    aws s3 cp . $2 --recursive --exclude "*" --include="*.csv"
    cd ../
}

function try()
{
    [[ $- = *e* ]]; SAVED_OPT_E=$?
    set +e
}

function throw()
{
    exit $1
}

function catch()
{
    export ex_code=$?
    (( $SAVED_OPT_E )) && set +e
    return $ex_code
}

function throwErrors()
{
    set -e
}

function ignoreErrors()
{
    set +e
}

"""
    for machine in machines:
        directory = create_directory_string(machine=machine)
        script += """
# start with a try
try
(
    echo "Start the try statement"
    execute_python %s %s || true # ignore a single failing command
    echo "finished"
)
# directly after closing the subshell you need to connect a group to the catch using ||
catch || {
    # now you can handle
    case $ex_code in
        $AnException)
            echo "AnException was thrown"
        ;;
        $AnotherException)
            echo "AnotherException was thrown"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code # you can rethrow the "exception" causing the script to exit if not caught
        ;;
    esac
}""" % (
            directory,
            f"s3://{s3_bucket}/{user_id}/{directory}/",
        )

    with open("deploy.sh", "w") as f:
        f.write(script)
