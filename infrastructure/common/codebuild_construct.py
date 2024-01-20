from typing import Dict

from aws_cdk import Duration
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_codecommit as codecommit
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kms as kms
from constructs import Construct


class CodeBuildConstruct(Construct):
    """CodeBuildConstruct class to construct a CodeBuild project.

    Attributes:
    :project:       The CodeBuild CDK project object
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        project_name: str,
        codebuild_role: iam.Role,
        environment_variables: Dict[str, codebuild.BuildEnvironmentVariable],
        repository: codecommit.Repository,
        kms_key: kms.Key,
        vpc: ec2.Vpc,
        security_group: ec2.SecurityGroup,
        timeout: Duration = Duration.hours(2),
        build_image_id: str = "aws/codebuild/amazonlinux2-x86_64-standard:4.0",
        build_image_compute_type: str = codebuild.ComputeType.SMALL,
        **kwargs,
    ) -> None:
        """
        Args:
            scope:                          The app construct
            construct_id:                   The name of the stack
            project_name:                   The name of the project
            codebuild_role:                 The IAM role for the CodeBuild project
            environment_variables:          The environmental variables
            repository:                     The CodeCommit repository
            kms_key:                        The KMS encryption key
            vpc:                            The VPC CodeBuild will run in
            security_group:                 The security group CodeBuild can leverage
            timeout:                        The timeout for CodeBuild in hours
            build_image_id:                 The Linux image CodeBuild will run on
            build_image_compute_type:       The CodeBuild instance type

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        # Define the AWS CodeBuild project
        self.project = codebuild.Project(
            self,
            "codebuild-project",
            project_name=project_name,
            description="Builds the model building workflow code repository.",
            role=codebuild_role,
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.from_code_build_image_id(
                    id=build_image_id
                ),
                compute_type=build_image_compute_type,
                privileged=True,
            ),
            environment_variables=environment_variables,
            source=codebuild.Source.code_commit(repository=repository),
            timeout=timeout,
            encryption_key=kms_key,
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(
                availability_zones=[f"{scope.region}a"],
            ),
            security_groups=[security_group],
        )
