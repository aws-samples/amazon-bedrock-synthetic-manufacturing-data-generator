from aws_cdk import RemovalPolicy
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kms as kms
from constructs import Construct


class KMSConstruct(Construct):
    """KMSConstruct class to construct KMS.

    Attributes:
    :key:                 The KMS encryption key
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        account_id: str,
        key_alias: str = None,
        **kwargs,
    ) -> None:
        """
        Args:
            scope:                  The app construct
            construct_id:           The name of the stack
            account_id:             AccountId of the parent stack
            key_alias:              (optional) Name of the key alias, has to have alias/ prefix

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        self.key = kms.Key(
            self,
            "key",
            enable_key_rotation=True,
            removal_policy=RemovalPolicy.DESTROY,
            policy=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=["kms:*"],
                        principals=[
                            iam.ArnPrincipal(f"arn:aws:iam::{account_id}:root")
                        ],
                        resources=["*"],
                    )
                ]
            ),
        )

        if key_alias:
            kms.Alias(self, "alias", alias_name=key_alias, target_key=self.key)
