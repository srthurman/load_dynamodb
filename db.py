import logging
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

def insert_data(table_name, data):
    table = dynamodb.Table(table_name)
    try:
        for row in data:
            table.put_item(Item=row)
    except Exception as e:
        logging.exception('Error inserting data into the database')


def create_table(table_name):
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'ID',
                    'KeyType': 'HASH'  #Partition key
                },
                {
                    'AttributeName': 'Place_Name',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'ID',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Place_Name',
                    'AttributeType': 'S'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

        print('Table "{}" status:'.format(table_name), table.table_status)

    except Exception as e:
        logging.exception('Error creating table "{}"'.format(table_name))