from aws_cdk import Stack
from constructs import Construct

from infrastructure.common.kms_construct import KMSConstruct
from infrastructure.common.s3_construct import S3Construct
from infrastructure.common.securitygroup_construct import (
    SecurityGroupConstruct,
)
from infrastructure.common.vpc_construct import VPCConstruct
from infrastructure.common.dynamodb_construct import DynamoDBConstruct


class BackendStack(Stack):
    """BackendStack class to deploy the AWS CDK stack.

    Attributes:
    :vpc:                   The VPC CDK object
    :security_group:        The Security Group CDK object
    :ecr_kms_key:           The KMS Key for ECR CDK object
    :codebuild_kms_key:     The KMS Key for CodeBuild CDK object
    :artifact_bucket:       The S3 bucket CDK object
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ):
        """Initialize the class.

        Args:
            scope:                     The AWS CDK app that is deployed
            construct_id:              The construct ID visible on the CloudFormation console for this resource

        Returns:
            No return
        """
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = VPCConstruct(self, "vpc", resource_prefix=construct_id).vpc

        self.security_group = SecurityGroupConstruct(
            self, "security-group", vpc=self.vpc, resource_prefix=construct_id
        ).security_group

        self.ddb_kms_key = KMSConstruct(
            self,
            "kms-ddb",
            account_id=self.account,
            key_alias=f"alias/{construct_id}-ddb",
        ).key

        self.codebuild_kms_key = KMSConstruct(
            self,
            "kms-codebuild",
            account_id=self.account,
            key_alias=f"alias/{construct_id}-codebuild",
        ).key

        self.s3_kms_key = KMSConstruct(
            self,
            "kms-s3",
            account_id=self.account,
            key_alias=f"alias/{construct_id}-s3",
        ).key

        self.lambda_kms_key = KMSConstruct(
            self,
            "kms-lambda",
            account_id=self.account,
            key_alias=f"alias/{construct_id}-lambda",
        ).key

        self.code_bucket = S3Construct(
            self,
            "s3-code",
            bucket_name=f"{construct_id}-code-{self.account}-{self.region}",
            kms_key=self.s3_kms_key,
        ).bucket

        self.data_bucket = S3Construct(
            self,
            "s3-data",
            bucket_name=f"{construct_id}-data-{self.account}-{self.region}",
            kms_key=self.s3_kms_key,
        ).bucket

        self.history_table = DynamoDBConstruct(
            self,
            "dynomdb-table",
            table_name=f"{construct_id}-interaction-history",
            encryption_key=self.ddb_kms_key,
            partition_key="user_id",
            time_to_live_attribute="dttm",
        ).table
