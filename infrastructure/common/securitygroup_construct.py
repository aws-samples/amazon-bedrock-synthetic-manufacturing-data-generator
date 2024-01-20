from typing import Dict

from aws_cdk import aws_ec2 as ec2
from constructs import Construct


class SecurityGroupConstruct(Construct):
    """SecurityGroupConstruct class to construct SecurityGroup and interface endpoints.

    Attributes:
    :security_group:       The Security Group CDK object
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.Vpc,
        resource_prefix: str,
        **kwargs,
    ) -> None:
        """
        Args:
            scope:                  The app construct
            construct_id:           The name of the stack
            vpc:                    The VPC used with the security groups
            resource_prefix:        The prefix for resources in the account
        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        interface_endpoints: Dict[str, ec2.InterfaceVpcEndpoint] = {
            "CODECOMMIT": ec2.InterfaceVpcEndpointAwsService.CODECOMMIT,
            "CODECOMMIT_GIT": ec2.InterfaceVpcEndpointAwsService.CODECOMMIT_GIT,
            "CODEBUILD": ec2.InterfaceVpcEndpointAwsService.CODEBUILD,
            "S3": ec2.InterfaceVpcEndpointService(
                f"com.amazonaws.{scope.region}.s3", 443
            ),
            "KMS": ec2.InterfaceVpcEndpointAwsService.KMS,
            "CLOUDWATCH": ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH,
            "CLOUDWATCH_LOGS": ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS,
        }

        self.security_group = ec2.SecurityGroup(
            self,
            "security-group",
            vpc=vpc,
            description="Security Group for AI & Data Platform",
            security_group_name=f"{resource_prefix}-sg",
        )

        self.security_group.add_ingress_rule(
            peer=ec2.Peer.ipv4("0.0.0.0/0"), connection=ec2.Port.tcp(443)
        )

        for service, endpoint in interface_endpoints.items():
            ec2.InterfaceVpcEndpoint(
                self,
                f"vpc-endpoint-{service}",
                vpc=vpc,
                service=endpoint,
                security_groups=[self.security_group],
            )
