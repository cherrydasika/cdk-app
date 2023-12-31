from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3Deploy,
    RemovalPolicy,
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

        glue_job_1_name="glue_script_test.py"  

        # Create an s3 buckets
        glue_bucket = s3.Bucket(
            self,
            id="test_bucket_dev_personal_456-2",
            bucket_name="test-bucket-cdk-input-datasets-3",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY

        )

        # Upload glue script to s3 bucket
        glue_scripts = s3Deploy.BucketDeployment(self, 
                                                 "glue-script-uploads", 
                                                 sources=[s3Deploy.Source.asset('C:\D\github\cdk-app\glue')],
                                                 destination_bucket=glue_bucket
                                                )

        
        # Create a ouput bucket to hold csv files
        csv_bucket = s3.Bucket(
            self,
            id="csv-output-1",
            bucket_name="test-csv-ouput-1",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY

        )    

        # Upload glue script to s3 bucket (csv file)
        csv_uploads = s3Deploy.BucketDeployment(self, 
                                                 "output_csv_files", 
                                                 sources=[s3Deploy.Source.asset('C:\D\github\cdk-app\output_files')],
                                                 destination_bucket=csv_bucket
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

        # Define the crawler
        crawler = glue_.CfnCrawler(
            self,
            'csv-crawler',
            role=glue_role.role_arn,
            database_name='csv_db',
            targets={
                's3Targets': [{"path": f"s3://{csv_bucket.bucket_name}"}]
            }


        )       

        # Define the glue job
        glue_.CfnJob(self, 'my-glue-job', 
            name='glue-job-for-testing',
            role = glue_role.role_arn,
            command = glue_.CfnJob.JobCommandProperty(
                name='pythonshell',
                python_version='3.9',
                script_location=f's3://{glue_bucket.bucket_name}/{glue_job_1_name}'
            ),
            glue_version='3.0',
            timeout=2          
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkAppQueue",git
        #     visibility_timeout=Duration.seconds(300),
        # )
