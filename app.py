#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_app.cdk_app_stack import CdkAppStack
from cdk_app.cdk_app_second_stack import CdkAppSecondStack

app = cdk.App()
env_UK = cdk.Environment(account="875257978630", region="eu-west-2")
first_stack = CdkAppStack(app, "CdkAppStack", env=env_UK)

second_stack = CdkAppSecondStack(app, "CdkAppSecondStack", 
                                 env=env_UK, 
                                 glue_workflow_name = first_stack.glue_workflow.name, 
                                 glue_crawler_name = first_stack.glue_crawler.name, 
                                 glue_transform_job_name = first_stack.glue_tranform_job.name,
                                 
                                 )
second_stack.add_dependency(first_stack)
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    

app.synth()
