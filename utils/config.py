import json
from typing import Any, Dict


class Config:
    """Config class to read the config for this stack.

    Attributes:
        :DIR_NAME:                      The directory name with the source code for Lambda
        :CODE_DIR:                      The directory with the source code for CodeCommit
        :MEMORY_SIZE:                   The Lambda memory size
        :TIMEOUT:                       The CodeBuild pipeline timeout
        :BUILD_IMAGE_ID:                The build image ID
        :BUILD_IMAGE_COMPUTE_TYPE:      The build image compute type size
        :BRANCH:                        The branch to be automated
        :CODE_BUILD_CLONE_OUTPUT:       The flag whether to clone output or not
        :EMPHEMERAL_STORAGE_SIZE:       The Lambda ephemeral storage size
        :HANDLER:                       The Lambda handler path
        :IMAGE_TYPE:                    The image build image type
        :COLUMN_NAME:                   The column name for a DynamoDB table
        :MODEL_ID:                      The Bedrock model ID
    """

    def __init__(self, path: str):
        """Initialize the class

        Args:
            path:       The path to the stack

        Returns:
            None
        """
        with open(f"{path}/config.json", "r") as file:
            config = json.loads(file.read())
        self.DIR_NAME: str = self._read_config_variable(
            config, "dir_name", "cicd-pipeline"
        )
        self.CODE_DIR: str = self._read_config_variable(
            config, "code_dir", "apis"
        )
        self.MEMORY_SIZE: int = self._read_config_variable(
            config, "memory_size", 256
        )
        self.TIMEOUT: int = int(
            self._read_config_variable(config, "timeout", "2")
        )
        self.BUILD_IMAGE_ID: str = self._read_config_variable(
            config,
            "build_image_id",
            "aws/codebuild/amazonlinux2-x86_64-standard:4.0",
        )
        self.BUILD_IMAGE_COMPUTE_TYPE: str = self._read_config_variable(
            config, "build_image_compute_type", "small"
        )
        self.BRANCH: str = self._read_config_variable(config, "branch", "main")
        self.CODE_BUILD_CLONE_OUTPUT: bool = (
            self._read_config_variable(
                config, "code_build_clone_output", "True"
            )
            == "True"
        )
        self.EMPHEMERAL_STORAGE_SIZE: int = self._read_config_variable(
            config, "ephemeral_storage_size", 512
        )
        self.HANDLER: str = self._read_config_variable(
            config, "handler", "app.index"
        )
        self.COLUMN_NAME: str = self._read_config_variable(
            config, "column_name", "active"
        )
        self.MODEL_ID: str = self._read_config_variable(
            config, "model_id", "bedrock-model-id"
        )

    def _read_config_variable(
        self, config: Dict, variable_name: str, default_value: Any = None
    ):
        """Read config key-value pairs

        Args:
            config:                 The config dictionary
            variable_name:          The name of the variable
            default_value:          The default value

        Returns:
            value:                  The env var defined
        """
        value = variable_name in config
        if value:
            return config[variable_name]
        else:
            return default_value
