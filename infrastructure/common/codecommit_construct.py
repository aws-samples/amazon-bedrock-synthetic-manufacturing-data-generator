from aws_cdk import aws_codecommit as codecommit
from constructs import Construct

from utils.utils import zip_repo


class CodeCommitConstruct(Construct):
    """CodeCommitConstruct class to construct a CodeCommit repository.

    Attributes:
    :repository:       The CodeCommit CDK repository object
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        repository_name: str,
        dir_name: str,
        branch: str = "main",
        **kwargs,
    ) -> None:
        """
        Args:
            scope:                  The app construct
            construct_id:           The name of the stack
            repository_name:        The CodeCommit repository name
            dir_name:               The name of the project
            branch:                 The branch to be created

        Returns:
            None
        """
        super().__init__(scope, construct_id, **kwargs)

        zip_repo(src=f"assets/{dir_name}", dst=f"assets/{dir_name}")

        self.repository = codecommit.Repository(
            self,
            "repository",
            repository_name=repository_name,
            description="Workflow infrastructure as code for the Project.",
            code=codecommit.Code.from_zip_file(
                file_path=f"assets/{dir_name}.zip", branch=branch
            ),
        )
