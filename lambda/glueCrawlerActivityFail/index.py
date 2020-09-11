import os
import boto3
import json
import re
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

client_sf = boto3.client('stepfunctions')

def lambda_handler(event, context):

    print( 'Calling Lambda - glueCrawlerActivityFail...' )

    print( 'Event : ' , event )
    print( 'Context : ' , context )

    crawlerName = os.environ['crawlerName']
    activity = os.environ['crawlerActivity']

    print('Clawler Name: {}'.format(crawlerName))
    print('Activity Name: {}'.format(activity))

    task = client.get_activity_task( activityArn=activity, workerName=crawlerName )
    print(task)

    response = client.send_task_failure(taskToken=task['taskToken'])