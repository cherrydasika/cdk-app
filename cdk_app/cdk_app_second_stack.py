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

class CdkAppSecondStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,glue_workflow_name, glue_crawler_name, glue_transform_job_name, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a workflow trigger
        glue_.CfnTrigger(self, 
                         id='glue_crawler_trigger',
                         name='glue_crawler_trigger',
                         actions=[
                             glue_.CfnTrigger.ActionProperty(
                                crawler_name= glue_workflow_name,
                                notification_property=glue_.CfnTrigger.NotificationPropertyProperty(notify_delay_after=3),
                                timeout=3
                             )
                         ],
                         type='EVENT',
                         workflow_name=glue_workflow_name
                         )
        # Create a workflow trigger with dependency
        glue_.CfnTrigger(
                            self,
                            id='glue_job_trigger',
                            name='glue_job_trigger',
                            actions=[
                                glue_.CfnTrigger.ActionProperty(
                                    job_name=glue_transform_job_name,
                                    notification_property=glue_.CfnTrigger.NotificationPropertyProperty(notify_delay_after=3),
                                    timeout=3
                                )
                            ],
                            type='CONDITIONAL',
                            start_on_creation=True,
                            workflow_name=glue_workflow_name,
                            predicate=glue_.CfnTrigger.PredicateProperty(
                                conditions=[
                                    glue_.CfnTrigger.ConditionProperty(
                                        crawler_name= glue_crawler_name,
                                        logical_operator='EQUALS',
                                        crawl_state='SUCCEEDED'
                                    )
                                ]
                            )                        
                        )
        

       
