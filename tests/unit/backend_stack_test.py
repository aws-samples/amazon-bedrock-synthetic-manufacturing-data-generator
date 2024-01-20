#!/usr/bin/env python3

import aws_cdk as cdk

from infrastructure.backend.backend_stack import BackendStack
from utils.environment import Environment


def test_s3_resources():
    app = cdk.App()
    ENV = cdk.Environment(
        account=Environment.AWS_ACCOUNT_ID, region=Environment.AWS_REGION
    )
    backend = BackendStack(
        scope=app,
        construct_id="backend",
        env=ENV,
    )
    template = cdk.assertions.Template.from_stack(backend)
    template.resource_count_is("AWS::KMS::Key", 4)
    template.resource_count_is("AWS::KMS::Alias", 4)
    template.resource_count_is("AWS::S3::Bucket", 2)
    template.resource_count_is("AWS::S3::BucketPolicy", 2)
    template.resource_count_is("AWS::EC2::EIP", 2)
    template.resource_count_is("AWS::EC2::FlowLog", 2)
    template.resource_count_is("AWS::EC2::InternetGateway", 1)
    template.resource_count_is("AWS::EC2::NatGateway", 2)
    template.resource_count_is("AWS::EC2::Route", 4)
    template.resource_count_is("AWS::EC2::RouteTable", 6)
    template.resource_count_is("AWS::EC2::SecurityGroup", 1)
    template.resource_count_is("AWS::EC2::Subnet", 6)
    template.resource_count_is("AWS::EC2::SubnetRouteTableAssociation", 6)
    template.resource_count_is("AWS::EC2::VPC", 1)
    template.resource_count_is("AWS::EC2::VPCEndpoint", 7)
    template.resource_count_is("AWS::EC2::VPCGatewayAttachment", 1)
    template.resource_count_is("AWS::IAM::Policy", 2)
    template.resource_count_is("AWS::IAM::Role", 2)
    template.resource_count_is("AWS::Logs::LogGroup", 2)
