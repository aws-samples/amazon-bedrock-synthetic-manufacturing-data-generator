from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    aws_dynamodb as _dynamodb,
    aws_kms as _kms,
)


class DynamoDBConstruct(Construct):
    """DynamoDBConstruct class to construct a DynamoDB table.

    Attributes:
    :table:       The DynamoDB CDK table
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        table_name: str,
        encryption_key: _kms.Key,
        partition_key: str = "name",
        time_to_live_attribute: str = "dttm",
        **kwargs,
    ) -> None:
        """
        Args:
            scope:                      The app construct
            construct_id:               The name of the stack
            table_name:                 The DDB table name
            encryption_key:             The KMS encryption key
            partition_key:              The name of the partition column
            time_to_live_attribute:     The TTL attribute

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        self.table = _dynamodb.Table(
            self,
            "dynamodb-table",
            table_name=table_name,
            partition_key=_dynamodb.Attribute(
                name=partition_key, type=_dynamodb.AttributeType.STRING
            ),
            encryption=_dynamodb.TableEncryption.CUSTOMER_MANAGED,
            encryption_key=encryption_key,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            time_to_live_attribute=time_to_live_attribute,
        )
