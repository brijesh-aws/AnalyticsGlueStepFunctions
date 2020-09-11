# ETL Automation using Step Functions & AWS Glue
Creating Analytics application using AWS Glue and end to end workflow automation using AWS Step Functions.

### CloudFormation 
Please find etlcf.yaml file which creates below resources in AWS

- S3 Buckets - Raw, Currated, Confirmed, Archive, Test, Glue (for scripts & logs)
- Glue Crawler Databases - Raw, Currated, Confirmed
- Glue Crawler
- Glue ETL Jobs
- DynamoDB tables to store the ETL Events & History
- SQS to send ETL Event messages for asynchronous processing
- Lambda functions to call Glue Crawler, ETL Jobs, status of crawler & jobs along with other utilities.
- Step Function for ETL Workflow Automation
- SNS Topic & Subscriber for Email Notifications

### Run below commands or deploy.bat file to create SAM template file for CloudFormation deployments

```bash
aws cloudformation package --template-file etlcf.yaml --output-template-file etlcf-deploy.yaml --s3-bucket mytestbucket143 --profile brijesh

aws cloudformation deploy --template-file etlcf-deploy.yaml --stack-name Test1 --capabilities CAPABILITY_IAM --profile brijesh

aws s3 cp etlcf-deploy.yaml s3://mytestbucket143/ --profile brijesh
```  

#### Run copyfiles.bat file to upload Glue ETL Job Scripts & Test CSV files.

##### Run invokeStepFunction lambda to test Step Function. You can also call this Lambda based on S3 event when raw csv file will be uploaded.


###### Notes:
- When we run Clawler first time when it has only one file with single folder in currated bucket, it is not doing crawlering better way, instead it just creates single table with name 'json' only.
- When we have multiple folders with files in currated bucket, then it is able to create tables with proper folder names.


###### Future Enhancements:
- Providing Job Configuration table and providing support of N ETL jobs instead of just row & confirm. (We can use Step Choice with Dynamic Input)
- Providing support of Step Function Activity
- Providing support of Glue Workflow
- 