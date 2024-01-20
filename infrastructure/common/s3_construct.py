import aws_cdk as cdk
from aws_cdk import aws_kms as kms
from aws_cdk import aws_s3 as s3
from constructs import Construct


class S3Construct(Construct):
    """S3Construct class to construct S3.

    Attributes:
    :bucket:                      The S3 bucket object
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        bucket_name: str,
        kms_key: kms.Key,
        **kwargs,
    ) -> None:
        """
        Args:
            scope:                  The app construct
            construct_id:           The name of the stack
            bucket_name:            The S3 bucket_name
            kms_key:                The KMS key CDK object

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = s3.Bucket(
            self,
            "bucket",
            bucket_name=bucket_name,
            server_access_logs_bucket=self,
            server_access_logs_prefix="logging-",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms_key,
            enforce_ssl=True,
            versioned=False,
        )
