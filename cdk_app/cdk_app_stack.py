from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_iam as aws_iam,
    aws_glue as glue_,
    Duration
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an s3 buckets
        s3.Bucket(
            self,
            id="test_bucket_dev_personal_456-1",
            bucket_name="test-bucket-cdk-input-datasets-2"

        )

        # First lambda function 
        hello_function = lambda_.Function(
        self, 
        "HelloHandler",
        code=lambda_.Code.from_asset('lambda'),
        runtime=lambda_.Runtime.PYTHON_3_11,
        handler="hello.handler",
        timeout=Duration.seconds(60)
        )

        # Create a new role for glue
        glue_role = aws_iam.Role(self, 'glue-role',
                                 role_name='my-glue-job-role',
                                 assumed_by=aws_iam.ServicePrincipal('glue.amazonaws.com'),
                                 inline_policies={
                                     'glue_policy':aws_iam.PolicyDocument(
                                         statements=[
                                             aws_iam.PolicyStatement(
                                                 effect=aws_iam.Effect.ALLOW,
                                                 actions=['s3:*', 'cloudwatch:*', 'sqs:*', 'glue:*'],
                                                 resources=['*']
                                             )
                                         ]
                                     )
                                 }

        )        

        # Define the glue job
        glue_.CfnJob(self, 'my-glue-job', 
            name='glue-job-for-testing',
            role = glue_role.role_arn,
            command = glue_.CfnJob.JobCommandProperty(
                name='pythonshell',
                python_version='3.9',
                script_location='s3://test-bucket-cdk-input-datasets-1/hello.py'
            ),
            glue_version='3.0',
            timeout=2          
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkAppQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
