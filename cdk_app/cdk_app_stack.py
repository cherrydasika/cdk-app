from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_lambda as lambda_
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an s3 buckets
        s3.Bucket(
            self,
            id="test_bucket_dev_personal_123",
            bucket_name="test-bucket-cdk-input-datasets"

        )

        # First lambda function 
        hello_function = lambda_.Function(
        self, 
        "HelloHandler",
        code=lambda_.Code.from_asset('lambda'),
        runtime=lambda_.Runtime.PYTHON_3_11,
        handler="hello.handler"
        )
        

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkAppQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
