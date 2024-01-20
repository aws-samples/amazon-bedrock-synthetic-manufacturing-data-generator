import os

from constructs import Construct
from aws_cdk import Duration, Stack, Size
from aws_cdk import aws_iam as iam

from utils.config import Config
from infrastructure.common.lambda_docker_construct import LambdaDockerConstruct
from infrastructure.backend.backend_stack import BackendStack
from infrastructure.imagebuild.imagebuild_stack import ImagebuildStack


class APIStack(Stack):
    """APIStack class to deploy the AWS CDK stack."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        backend: BackendStack,
        pipeline: ImagebuildStack,
        **kwargs,
    ) -> None:
        """Init the class

        Args:
            scope:                              The app construct
            construct_id:                       The name of the stack
            backend:                            The application BackendStack

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        config = Config(path=os.path.dirname(os.path.realpath(__file__)))

        # Define the IAM role
        lambda_policy_list = [
            iam.PolicyStatement(
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=[
                    "arn:aws:logs:*:*:log-group:*",
                    "arn:aws:logs:*:*:log-group:*:log-stream:*",
                ],
            ),
            iam.PolicyStatement(
                actions=[
                    "dynamodb:PutItem",
                    "dynamodb:Scan",
                    "dynamodb:GetItem",
                ],
                resources=[backend.history_table.table_arn],
            ),
            iam.PolicyStatement(
                actions=[
                    "kms:Decrypt",
                    "kms:Encrypt",
                    "kms:GenerateDataKey",
                ],
                resources=[
                    backend.s3_kms_key.key_arn,
                    backend.ddb_kms_key.key_arn,
                ],
            ),
            iam.PolicyStatement(
                actions=[
                    "s3:PutObject",
                    "s3:GetObject",
                ],
                resources=[backend.code_bucket.bucket_arn],
            ),
            iam.PolicyStatement(
                actions=[
                    "codepipeline:StartPipelineExecution",
                ],
                resources=[
                    f"arn:aws:codepipeline:{self.region}:{self.account}:{pipeline.pipeline.pipeline_name}",
                ],
            ),
            iam.PolicyStatement(
                actions=[
                    "bedrock:*",
                ],
                resources=[
                    "*",
                ],
            ),
        ]

        LambdaDockerConstruct(
            self,
            "async-lambda",
            function_name=f"{construct_id}-async",
            environment_variables={
                "model_id": "anthropic.claude-v2",
                "table_name": backend.history_table.table_name,
                "column_name": config.COLUMN_NAME,
                "pipeline_name": pipeline.pipeline.pipeline_name,
            },
            kms_key=backend.lambda_kms_key,
            initial_policy=lambda_policy_list,
            code_dir=f"{config.CODE_DIR}/async/",
            timeout=Duration.seconds(config.TIMEOUT),
            memory_size=config.MEMORY_SIZE,
            ephemeral_storage_size=Size.mebibytes(
                config.EMPHEMERAL_STORAGE_SIZE
            ),
        ).lambda_function
