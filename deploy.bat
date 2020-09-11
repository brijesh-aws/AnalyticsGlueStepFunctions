cls

aws cloudformation package --template-file etlcf.yaml --output-template-file etlcf-deploy.yaml --s3-bucket mytestbucket143 --profile opencloud

aws cloudformation deploy --template-file etlcf-deploy.yaml --stack-name Test1 --capabilities CAPABILITY_IAM --profile opencloud

aws s3 cp etlcf-deploy.yaml s3://mytestbucket143/ --profile opencloud
