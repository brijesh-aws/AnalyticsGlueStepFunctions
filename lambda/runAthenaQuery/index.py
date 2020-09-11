import time
import boto3
import os
import sys

def lambda_handler(event, context):

    client = boto3.client('athena')

    database = os.environ['DATABASE']
    query = os.environ['query']
    dropTableQuery = "DROP TABLE {}".format(os.environ['dropTableName'])

    print( "Database : " + database )
    print( "Drop Table Query : " + dropTableQuery )

    try:
        if len(os.environ['dropTableName']) != 0:
            response = client.start_query_execution(
                QueryString=dropTableQuery,
                QueryExecutionContext={
                    'Database': database
                },
                ResultConfiguration={
                    'OutputLocation': os.environ['outputPath'],
                }
            )
    except:
        print("Unexpected error in Drop table:", sys.exc_info()[0])

    print( response )
    print("Query : " + query)
    print( "Executing Query start...." )

    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': os.environ['outputPath'],
        }
    )

    print("Executing Query end....")
    print(response)

    return response
