from aws_cdk import aws_ec2 as ec2
from constructs import Construct


class VPCConstruct(Construct):
    """LambdaConstruct class to construct Lambda.

    Attributes:
    :vpc:       The VPC CDK object
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        resource_prefix: str,
        **kwargs,
    ) -> None:
        """
        Args:
            scope:                  The app construct
            construct_id:           The name of the stack
            resource_prefix:        The prefix for resources in the account
        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "vpc",
            vpc_name=f"{resource_prefix}-vpc",
            cidr="10.0.0.0/16",
            nat_gateways=1,
            max_azs=3,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            flow_logs={
                "traffic_type": ec2.FlowLogTrafficType.REJECT,
                "destination": ec2.FlowLogDestination.to_s3(),
            },
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"{resource_prefix}-PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                ),
                ec2.SubnetConfiguration(
                    name=f"{resource_prefix}-PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    map_public_ip_on_launch=False,
                    cidr_mask=24,
                ),
            ],
        )

        eip = ec2.CfnEIP(self, "eip", domain="vpc")

        nat_gateway = ec2.CfnNatGateway(
            self,
            "nat-gateway",
            allocation_id=eip.attr_allocation_id,
            subnet_id=self.vpc.public_subnets[0].subnet_id,
        )

        ec2.CfnRoute(
            self,
            "RouteTableEntry",
            route_table_id=self.vpc.select_subnets(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
            .subnets[0]
            .route_table.route_table_id,
            destination_cidr_block="0.0.0.0/0",
            nat_gateway_id=nat_gateway.ref,
        )
