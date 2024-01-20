from typing import List

import aws_cdk as cdk
import cdk_nag as nag

# --------------------------------
# CDK NAG checks
# --------------------------------


class NAGTest:
    def run(
        app: cdk.App,
        api: cdk.Stack,
        backend: cdk.Stack,
        builds: List[cdk.Stack],
        **kwargs,
    ) -> None:
        cdk.Aspects.of(app).add(nag.AwsSolutionsChecks())

        nag.NagSuppressions.add_stack_suppressions(
            backend,
            [
                nag.NagPackSuppression(
                    id="AwsSolutions-EC23",
                    reason="Inbound access needed",
                ),
                nag.NagPackSuppression(
                    id="AwsSolutions-DDB3",
                    reason="Point in time recovery not necessary for this demo",
                ),
            ],
        )

        nag.NagSuppressions.add_stack_suppressions(
            api,
            [
                nag.NagPackSuppression(
                    id="AwsSolutions-IAM4",
                    reason="Managed policies are accepted.",
                ),
                nag.NagPackSuppression(
                    id="AwsSolutions-IAM5",
                    reason="Use AWS managed policies CodeBuild Project with defaults from cdk",
                ),
                nag.NagPackSuppression(
                    id="AwsSolutions-COG4",
                    reason="Cognito user pool not necessary.",
                ),
                nag.NagPackSuppression(
                    id="AwsSolutions-L1",
                    reason="Latest runtime not necessary.",
                ),
            ],
        )

        for stack in builds:
            nag.NagSuppressions.add_stack_suppressions(
                stack,
                [
                    nag.NagPackSuppression(
                        id="AwsSolutions-CB3",
                        reason="Privileged mode accepted for this code",
                    ),
                    nag.NagPackSuppression(
                        id="AwsSolutions-CB4",
                        reason="S3 and Sagemaker Jobs are encrypted",
                    ),
                    nag.NagPackSuppression(
                        id="AwsSolutions-IAM5",
                        reason="Use AWS managed policies CodeBuild Project with defaults from cdk",
                    ),
                ],
            )
