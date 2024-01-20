import os
from typing import Any


class Environment:
    def _read_env_variable(variable_name: str, default_value: Any = None):
        value = os.environ.get(variable_name, default_value)
        if value:
            return value
        raise KeyError(f"Variable {variable_name} is not defined")

    PROJECT_NAME: str = _read_env_variable("PROJECT_NAME", "synthetic-data")

    IMAGE_TYPE: str = _read_env_variable("IMAGE_TYPE", "cicd")

    RUN_NAG: bool = _read_env_variable("RUN_NAG", True)
    AWS_REGION: str = _read_env_variable("CDK_DEFAULT_REGION", "us-east-1")
    AWS_ACCOUNT_ID: str = _read_env_variable(
        "CDK_DEFAULT_ACCOUNT", "1234567890"
    )
