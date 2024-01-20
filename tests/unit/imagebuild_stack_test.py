#!/usr/bin/env python3

import aws_cdk as cdk

from infrastructure.backend.backend_stack import BackendStack
from infrastructure.imagebuild.imagebuild_stack import ImagebuildStack
from utils.environment import Environment


def test_cicd_resources():
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
    template = cdk.assertions.Template.from_stack(imagebuild)
    template.resource_count_is("AWS::IAM::Policy", 5)
    template.resource_count_is("AWS::IAM::Role", 4)
    template.resource_count_is("AWS::CodeBuild::Project", 1)
    template.resource_count_is("AWS::CodeCommit::Repository", 1)
    template.resource_count_is("AWS::CodePipeline::Pipeline", 1)
    template.resource_count_is("AWS::Events::Rule", 1)
