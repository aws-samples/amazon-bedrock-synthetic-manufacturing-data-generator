#!/usr/bin/env python3

import aws_cdk as cdk

from infrastructure.backend.backend_stack import BackendStack
from infrastructure.imagebuild.imagebuild_stack import ImagebuildStack
from infrastructure.api.api_stack import APIStack
from tests.nag.nag_test import NAGTest
from utils.environment import Environment

# --------------------------------
# Set stack environment variables
# --------------------------------

PROJECT_NAME = Environment.PROJECT_NAME
IMAGE_TYPE = Environment.IMAGE_TYPE
ENV = cdk.Environment(
    account=Environment.AWS_ACCOUNT_ID, region=Environment.AWS_REGION
)

# --------------------------------
# Initialize App
# --------------------------------

app = cdk.App()

# --------------------------------
# Backend
# --------------------------------

backend = BackendStack(
    scope=app,
    construct_id=f"{PROJECT_NAME}-backend",
    env=ENV,
)

# --------------------------------
# Imagebuilds
# --------------------------------

build = ImagebuildStack(
    scope=app,
    construct_id=f"{PROJECT_NAME}-{IMAGE_TYPE}",
    backend=backend,
    image_type=IMAGE_TYPE,
    env=ENV,
)
builds = [build]

# --------------------------------
# APIs
# --------------------------------

api = APIStack(
    scope=app,
    construct_id=f"{PROJECT_NAME}-api",
    backend=backend,
    pipeline=build,
    env=ENV,
)

# --------------------------------
# Nag Test
# --------------------------------

if Environment.RUN_NAG:
    NAGTest.run(
        app=app,
        api=api,
        backend=backend,
        builds=builds,
    )

# --------------------------------

cdk.Tags.of(app).add("project", PROJECT_NAME)
app.synth()
