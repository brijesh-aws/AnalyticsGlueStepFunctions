import json
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import boto3
import os
import time
import uuid

client = boto3.client('glue')

glue = boto3.client( service_name='glue', region_name=os.environ['AWS_REGION'], endpoint_url='https://glue.{}.amazonaws.com'.format( os.environ['AWS_REGION'] ) )


def lambda_handler(event, context):

    class InvalidBucketException( Exception ):
        pass
    class InvalidFolderException( Exception ):
        pass

    print( 'Context : ' , context )
    print( 'Event : ' , event )

    event['guid'] = str( uuid.uuid4() )

    rawBucketName   = os.environ['rawBucketName']
    currBucketName  = os.environ['currBucketName']
    confBucketName  = os.environ['confBucketName']
    archiveBucket   = os.environ['archiveBucket']

    rawCrawlerDB   = os.environ['rawCrawlerDB']
    currCrawlerDB  = os.environ['currCrawlerDB']
    confCrawlerDB  = os.environ['confCrawlerDB']


    print( "Bucket Name : {}".format( rawBucketName ) )

    eventBucket = event['detail']['requestParameters']['bucketName']
    print( "Event Bucket Name : {}".format( eventBucket ) )

    if( eventBucket != rawBucketName ):
        bucketError = "Initialization~Bucket '{}' is not valid".format( eventBucket )
        print( bucketError ) 
        raise InvalidBucketException( bucketError )

    folderPath  = event['detail']['requestParameters']['key']
    folderArray = folderPath.split( '/' )
    folderName  = folderArray[-2]
    folderName = folderName.lower()

    print( "Folder Name : {}".format( folderName ) )

    # Added for CSV Conversion

    if( folderName == "person" or folderName == "address"  ):

        response = {
            "analytics_job_details" : {
                "name" : folderName,
                "etl_jobs" : {
                    "1" : folderName + "_raw",
                    "2" : folderName + "_conf"
                },
                "buckets" : {
                    "raw_bucket"  : rawBucketName,
                    "curr_bucket" : currBucketName,
                    "conf_bucket" : confBucketName,
                    "archive_bucket" : archiveBucket
                },
                "crawler_db" : {
                    "raw"       : rawCrawlerDB,
                    "currated"  : currCrawlerDB,
                    "conf"      : confCrawlerDB
                }
            },
            "Records": [{
                "s3" : {
                    "bucket": {
                        "name" : rawBucketName
                    },
                    "object": {
                        "key" : folderPath
                    }
                }
            }]

        }

    else:    
        error = "Initialization~Folder {} is not valid".format( folderName )
        raise InvalidFolderException( error )

    response['guid'] = str( uuid.uuid4() )    
    return response


