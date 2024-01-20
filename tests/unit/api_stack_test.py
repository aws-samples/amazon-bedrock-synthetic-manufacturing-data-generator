#!/usr/bin/env python3

import aws_cdk as cdk

from infrastructure.backend.backend_stack import BackendStack
from infrastructure.imagebuild.imagebuild_stack import ImagebuildStack
from infrastructure.api.api_stack import APIStack
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
    imagebuild = ImagebuildStack(
        scope=app,
        construct_id="build",
        backend=backend,
        image_type="run",
        env=ENV,
    )
    api = APIStack(
        scope=app,
        construct_id="api",
        backend=backend,
        pipeline=imagebuild,
        env=ENV,
    )
    template = cdk.assertions.Template.from_stack(api)
    template.resource_count_is("AWS::IAM::Policy", 1)
    template.resource_count_is("AWS::IAM::Role", 1)
    template.resource_count_is("AWS::Lambda::Function", 1)
