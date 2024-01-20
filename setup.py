from setuptools import setup

with open("README.md") as fp:
    """Returns the required readme defined in README.md"""
    long_description = fp.read()

setup(
    name="SyntheticDataGenerator",
    version="1.0",
    description="This is the repository with an end-to-end synthetic data generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AWS ProServe Team",
    author_email="aws-proserve-ai-hub@amazon.com",
    python_requires=">3.9",
    install_requires=[
        "pre-commit",
        "pytest",
        "boto3",
        "aws-cdk-lib",
        "cdk-nag",
        "checkov",
        "cfn-lint",
    ],
    tests_require=["pytest"],
    packages=["infrastructure"],
)
