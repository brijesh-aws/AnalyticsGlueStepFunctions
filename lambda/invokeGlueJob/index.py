import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

import os
import uuid

client = boto3.client('glue')
glue = boto3.client(service_name='glue', region_name=os.environ['AWS_REGION'],
                    endpoint_url='https://glue.{}.amazonaws.com'.format( os.environ['AWS_REGION'] ) )

client_sf = boto3.client('stepfunctions')
# replace activity arn with respective activivty arn
activity = "arn:aws:states:us-west-2:XXXXXXXXXXXX:activity:file-transfer"


def lambda_handler(event, context):

    class ETLException(Exception):
        pass

    print( 'Event : ' , event )
    print( 'Context : ' , context )

    event['guid'] = str( uuid.uuid4() )

    #jobName = os.environ['ETL_JOB_NAME']

    try:

        order   = event['order']
        print( "Job Key : {}".format( order ) )

        jobDetailsMain  = event[ "analytics_job_details" ]
        print( "Job Details Main : {}".format( jobDetailsMain ) )

        jobDetails      = jobDetailsMain['etl_jobs']
        print( "Job Details : {}".format( jobDetails ) )

        etlBuckets = event[ "analytics_job_details" ]['buckets']
        currBucketName  = etlBuckets['curr_bucket']
        print( "Curration Bucket : {}".format( currBucketName ) )

        confBucketName  = etlBuckets['conf_bucket']
        print( "Confirm Bucket : {}".format( confBucketName ) )

        rawfBucketName  = etlBuckets['raw_bucket']
        print( "Raw Bucket : {}".format( rawfBucketName ) )

        rawDB       = jobDetailsMain['crawler_db']['raw']
        curratedDB  = jobDetailsMain['crawler_db']['currated']
        confDB      = jobDetailsMain['crawler_db']['conf']


        jobName = jobDetails[ order ]
        print( 'Glue ETL Job : ' + jobName )

        
        

        event.pop( 'JobRunId', None )
        event.pop( 'job_response', None )
    
        response = client.start_job_run( JobName=jobName, Arguments={ 
                                                                        "--currBucketName"  : currBucketName, 
                                                                        "--confBucketName"  : confBucketName, 
                                                                        "--rawfBucketName"  : rawfBucketName, 
                                                                        "--rawDB"           : rawDB,
                                                                        "--curratedDB"      : curratedDB,
                                                                        "--confDB"          : confDB
                                                                    })
                                                                    
        print( "ETL Job ran with ID : {} ".format( response['JobRunId'] ) )

        output = {}
        output['analytics_job_details']      = jobDetailsMain
        output['order']                      = order
        output['job_response']               = response

        event['output'] = str( uuid.uuid4() )
        return output

    except client.exceptions.ConcurrentRunsExceededException:
        print('ETL Job in progress...')
        raise ETLException('ETL Job In Progress!')

    except Exception as e:

        print( 'Error:' )
        print( e )
        raise e

