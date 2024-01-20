from aws_cdk import aws_codebuild as codebuild


class MapComputeTypes:
    """MapComputeTypes class to help map compute types."""

    def map_compute_types(self, compute_type: str):
        """Map the compute types
        Args:
            compute_type:       The compute type (Options: "small", "medium", "large", "x2_large")

        Returns:
            codebuild.ComputeType
        """
        return {
            "small": codebuild.ComputeType.SMALL,
            "medium": codebuild.ComputeType.MEDIUM,
            "large": codebuild.ComputeType.LARGE,
            "x2_large": codebuild.ComputeType.X2_LARGE,
        }[compute_type]
