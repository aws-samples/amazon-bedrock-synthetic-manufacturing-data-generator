from typing import Dict, List

from aws_cdk import Duration, Size
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kms as kms
from aws_cdk import aws_lambda as lambda_func
from constructs import Construct


class LambdaDockerConstruct(Construct):
    """LambdaDockerConstruct class to construct Lambda.

    Attributes:
    :lambda_function:       The Lambda CDK object
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        function_name: str,
        environment_variables: Dict[str, str],
        initial_policy: List[iam.PolicyStatement],
        kms_key: kms.Key,
        code_dir: str = "api",
        timeout: Duration = Duration.seconds(15),
        memory_size: int = 256,
        ephemeral_storage_size: Size = Size.mebibytes(256),
        **kwargs,
    ) -> None:
        """Initialize class

        Args:
            function_name:          The name of the Lambda function
            environment_variables:  The Lambda environmental variables
            initial_policy:         The list of IAM PolicyStatements
            kms_key:                The KMS key for encryption
            code_dir:               The directory name with code
            handler:                The entry Lambda handler path
            timeout:                The number of minutes for timeout
            memory_size:            The memory size in MB

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_function = lambda_func.DockerImageFunction(
            self,
            "docker-lambda",
            function_name=function_name,
            description="AWS Lambda function for Langchain",
            code=lambda_func.DockerImageCode.from_image_asset(
                f"assets/{code_dir}"
            ),
            timeout=timeout,
            memory_size=memory_size,
            ephemeral_storage_size=ephemeral_storage_size,
            environment=environment_variables,
            initial_policy=initial_policy,
            environment_encryption=kms_key,
        )
