import boto3
import os
import sys
import json
# Import Clients
session = boto3.session.Session(region_name=os.environ['AWS_REGION'])
dynamodb = session.client('dynamodb')
cloudwatch = session.client('cloudwatch')

# Describe All Tables Returned from ListTables
def get_size(tables):
    table_and_size = []
    for table in tables:
        try:
            res = dynamodb.describe_table(TableName=table)
            # Add Size for Base Table
            table_and_size.append({'TableName': table, 'Size': res['Table']['TableSizeBytes']})
            # Check for GSI's and Add Size
            if 'GlobalSecondaryIndexes' in res['Table']:
                for index in res['Table']['GlobalSecondaryIndexes']:
                    table_and_size.append(
                        {'IndexName': index['IndexName'], 'Size': index['IndexSizeBytes'], 'TableName': table, 'IndexType': 'Global'})
            # Check for LSI's and Add Size            
            if 'LocalSecondaryIndexes' in res['Table']:
                for index in res['Table']['LocalSecondaryIndexes']:
                    table_and_size.append(
                        {'IndexName': index['IndexName'], 'Size': index['IndexSizeBytes'], 'TableName': table, 'IndexType': 'Local'})
        except Exception as e:
            sys.exit(e.response['ResponseMetadata'])
    return table_and_size

# Publish Table Size Metrics to CloudWatch
def publish_metrics(metrics):
    for metric in metrics:
        # Table Alone
        dimensions = [{
            'Name': 'TableName',
            'Value': metric['TableName']
        }]
        # Table with Indexes
        if 'IndexName' in metric:
            dimensions.extend([{
                'Name': 'IndexName',
                'Value': metric['IndexName']
            }, {
                'Name': 'IndexType',
                'Value': metric['IndexType']
            }])

        try:
            cloudwatch.put_metric_data(
                Namespace='DynamoDB Table Size',
                MetricData=[
                    {
                        'MetricName': 'Table Size',
                        'Dimensions': dimensions,
                        'Value': metric['Size'],
                        'Unit': 'Bytes'
                    },
                ]
            )

        except Exception as e:
            sys.exit(e.response['ResponseMetadata'])

# Lambda Handler
def lambda_handler(event, context):
    # Get list of all tables in the region
    table_names = []
    try:
        res = dynamodb.list_tables()
        table_names = res['TableNames']
    except Exception as e:
        sys.exit(e.response['ResponseMetadata'])

    # If more than 100 tables in region, paginate to list them all
    while 'LastEvaluatedTableName' in res:
        try:
            res = dynamodb.list_tables(
                Limit=10,
                ExclusiveStartTableName=res['LastEvaluatedTableName']
            )
            table_names = table_names + res['TableNames']
        except Exception as e:
            sys.exit(e.response['ResponseMetadata'])

    # Get List of Tables and Current Table Size in Bytes
    current_size = get_size(table_names)
    # Publish Tables Sizes to CloudWatch
    publish_metrics(current_size)

    # Exit
    return {
        'statusCode': 200,
        'body': json.dumps('Metrics Stored')
    }
