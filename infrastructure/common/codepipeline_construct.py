from typing import List

from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_codecommit as codecommit
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as actions
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from constructs import Construct


class CodePipelineConstruct(Construct):
    """CodePipelineConstruct class to construct a CodePipeline project.

    Attributes:
    :pipeline:              The CodePipeline CDK project object
    :source_artifact:       The CodePipeline artifat object
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        pipeline_name: str,
        role: iam.Role,
        repository: codecommit.Repository,
        codebuild_project: codebuild.Project,
        artifact_bucket: s3.Bucket,
        branch: str = "main",
        code_build_clone_output: bool = True,
        **kwargs
    ) -> None:
        """
        Args:
            scope:                          The app construct
            construct_id:                   The name of the stack
            pipeline_name:                  The name of the project
            role:                           The IAM role for the CodePipeline project
            repository:                     The CodeCommit repository
            codebuild_project:              The CodeBuild project to add
            artifact_bucket:                The S3 bucket CDK object
            branch:                         The branch to be leveraged
            code_build_clone_output:        The indication if code build will clone output

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        self.source_artifact = codepipeline.Artifact()

        # Defines the AWS CodePipeline
        self.pipeline = codepipeline.Pipeline(
            self,
            "codepipeline-project",
            pipeline_name=pipeline_name,
            role=role,
            artifact_bucket=artifact_bucket,
        )

        self._create_codecommit_codebuild_pipeline(
            repository=repository,
            codebuild_project=codebuild_project,
            outputs=[codepipeline.Artifact()],
            branch=branch,
            code_build_clone_output=code_build_clone_output,
        )

    def _create_codecommit_codebuild_pipeline(
        self,
        repository: codecommit.Repository,
        codebuild_project: codebuild.Project,
        outputs: List[codepipeline.Artifact],
        branch: str = "main",
        code_build_clone_output: bool = True,
    ):
        """
        Args:
            repository:                     The CodeCommit repository
            codebuild_project:              The CodeBuild project to add
            outputs:                        The list of output artifacts
            branch:                         The branch to be leveraged
            code_build_clone_output:        The indication if code build will clone output

        Returns:
            None
        """
        # Define actions that are executed in CodePipeline:
        # - `Source` leverages the AWS CodeCommit `repository` and copies that into AWS CodeBuild
        # - `Deploy` will run AWS CodeBuild leveraging the pulled `repository`
        source_action = actions.CodeCommitSourceAction(
            action_name="Source",
            output=self.source_artifact,
            branch=branch,
            repository=repository,
            code_build_clone_output=code_build_clone_output,
        )

        build_action = actions.CodeBuildAction(
            action_name="Deploy",
            project=codebuild_project,
            input=self.source_artifact,
            outputs=outputs,
        )

        # Add the stages defined above to the pipeline
        self.pipeline.add_stage(stage_name="Source", actions=[source_action])
        self.pipeline.add_stage(stage_name="Deploy", actions=[build_action])
