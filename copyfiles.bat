cls
aws s3 cp glue\etl-job-scripts\address_raw.py   s3://analytics-glue-work/scripts/address_raw.py --profile opencloud
aws s3 cp glue\etl-job-scripts\address_conf.py  s3://analytics-glue-work/scripts/address_conf.py --profile opencloud
aws s3 cp glue\etl-job-scripts\person_raw.py    s3://analytics-glue-work/scripts/person_raw.py --profile opencloud
aws s3 cp glue\etl-job-scripts\person_conf.py   s3://analytics-glue-work/scripts/person_conf.py --profile opencloud

aws s3 cp glue\test-files\person.csv    s3://glueanalytics-glueanalyticsraw-did9zh4g938e/csv/person/person.csv --profile opencloud
aws s3 cp glue\test-files\address.csv   s3://glueanalytics-glueanalyticsraw-did9zh4g938e/csv/address/address.csv --profile opencloud