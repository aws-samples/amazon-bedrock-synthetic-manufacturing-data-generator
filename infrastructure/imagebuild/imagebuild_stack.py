import os

from aws_cdk import Duration, Stack
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_iam as iam
from constructs import Construct

from infrastructure.common.codebuild_construct import CodeBuildConstruct
from infrastructure.common.codecommit_construct import CodeCommitConstruct
from infrastructure.common.codepipeline_construct import CodePipelineConstruct

from utils.config import Config
from utils.environment import Environment
from utils.map_compute_types import MapComputeTypes


class ImagebuildStack(Stack):
    """ImagebuildStack class to deploy the AWS CDK stack."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        backend: Stack,
        image_type: str,
        **kwargs,
    ):
        """Initialize the class.

        Args:
            scope:                     The AWS CDK app that is deployed
            construct_id:              The construct ID visible on the CloudFormation console for this resource
            backend:                   The backend services put in a stack
            image_type:                The type of imagebuild (processing, training, inference)

        Returns:
            No return
        """
        super().__init__(scope, construct_id, **kwargs)

        mapper = MapComputeTypes()
        config = Config(path=os.path.dirname(os.path.realpath(__file__)))

        codebuild_role = iam.Role(
            self,
            "image-role",
            assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
            inline_policies={
                "codebuild-inline": iam.PolicyDocument(
                    statements=[
                        iam.PolicyStatement(
                            actions=[
                                "iam:PassRole",
                                "sts:AssumeRole",
                            ],
                            resources=[
                                "arn:aws:iam::*:role/*",
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
                                "bedrock:*",
                            ],
                            resources=["*"],
                        ),
                        iam.PolicyStatement(
                            actions=[
                                "s3:PutObject",
                                "s3:GetObject",
                                "s3:CreateMultipartUpload",
                                "s3:ListMultipartUploadParts",
                                "s3:AbortMultipartUpload",
                            ],
                            resources=[
                                backend.data_bucket.bucket_arn,
                                backend.data_bucket.bucket_arn + "/*",
                                backend.code_bucket.bucket_arn,
                                backend.code_bucket.bucket_arn + "/*",
                            ],
                        ),
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
                    ]
                ),
            },
        )

        # Add more service principals the IAM role can assume
        codebuild_role.assume_role_policy.add_statements(
            iam.PolicyStatement(
                actions=["sts:AssumeRole"],
                effect=iam.Effect.ALLOW,
                principals=[
                    iam.ServicePrincipal("codepipeline.amazonaws.com"),
                ],
            )
        )

        repository = CodeCommitConstruct(
            self,
            "codecommit-repository",
            repository_name=f"{Environment.PROJECT_NAME}-{image_type}-run",
            dir_name=config.DIR_NAME,
            branch=config.BRANCH,
        ).repository

        codebuild_project = CodeBuildConstruct(
            self,
            "processing-image-codebuild",
            project_name=f"{Environment.PROJECT_NAME}-{image_type}-run",
            codebuild_role=codebuild_role,
            environment_variables={
                "CODE_BUCKET": codebuild.BuildEnvironmentVariable(
                    value=backend.code_bucket.bucket_name
                ),
                "DATA_BUCKET": codebuild.BuildEnvironmentVariable(
                    value=backend.data_bucket.bucket_name
                ),
                "TABLE_NAME": codebuild.BuildEnvironmentVariable(
                    value=backend.history_table.table_name
                ),
                "COLUMN_NAME": codebuild.BuildEnvironmentVariable(
                    value=config.COLUMN_NAME
                ),
                "MODEL_ID": codebuild.BuildEnvironmentVariable(
                    value=config.MODEL_ID
                ),
            },
            repository=repository,
            kms_key=backend.codebuild_kms_key,
            vpc=backend.vpc,
            security_group=backend.security_group,
            timeout=Duration.hours(config.TIMEOUT),
            build_image_id=config.BUILD_IMAGE_ID,
            build_image_compute_type=mapper.map_compute_types(
                compute_type=config.BUILD_IMAGE_COMPUTE_TYPE
            ),
        ).project

        self.pipeline = CodePipelineConstruct(
            self,
            "pipeline",
            pipeline_name=f"{Environment.PROJECT_NAME}-{image_type}-run",
            role=codebuild_role,
            repository=repository,
            codebuild_project=codebuild_project,
            artifact_bucket=backend.code_bucket,
            branch=config.BRANCH,
            code_build_clone_output=config.CODE_BUILD_CLONE_OUTPUT,
        ).pipeline
