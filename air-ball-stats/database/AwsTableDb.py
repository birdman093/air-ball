import boto3
import json
from botocore.config import Config

class AwsTableDb:
    def __init__(self):
        self.my_config = Config(
            region_name = 'us-east-2',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        
        self.dynamodb = boto3.client('dynamodb', config=self.my_config)

        # team data
        self.teamtable = 'airBallDb'
        self.partitionkey = 'teamName'
        self.configpartitionvalue = 'Configuration'

        # prediction data
        self.prediction_table = 'predictionDb'
        self.prediction_partitionkey = 'gamedate'


    def addToDb(self, partitionkey: str, serializeddata: str):
        self.dynamodb.put_item(
            TableName=self.teamtable,
            Item={
                self.partitionkey: {'S': partitionkey},
                'data': {'S': serializeddata}
            }
        )

    def addItemsToDbBatch(self, partitionkeys: list[str], serializeddata: list[str]):
        MAX_BATCH_SIZE = 20

        if len(partitionkeys) != len(serializeddata):
            raise ValueError("Partition keys and serialized data lists have non-matching lengths.")

        items = [{'partitionkey': pk, 'serializeddata': sd} for pk, sd in zip(partitionkeys, serializeddata)]
        batches = [items[i:i + MAX_BATCH_SIZE] for i in range(0, len(items), MAX_BATCH_SIZE)]
        for batch in batches:
            request_items = {
                self.teamtable: [
                    {
                        'PutRequest': {
                            'Item': {
                                self.partitionkey: {'S': item['partitionkey']},  # Use the actual partition key attribute name
                                'data': {'S': item['serializeddata']}
                            }
                        }
                    } for item in batch
                ]
            }
            response = self.dynamodb.batch_write_item(RequestItems=request_items)

            unprocessed_items = response.get('UnprocessedItems', {})
            if unprocessed_items:
                # Handle unprocessed items (e.g., by retrying)
                raise Exception(f"Warning: Some items were not processed: {unprocessed_items}")



    def getFromDb(self, partitionkey: str) -> str:
        response = self.dynamodb.get_item(
            TableName=self.teamtable,
            Key={
                'teamName': {'S': self.partitionkey}
            }
        )
        return response.get('Item', None)
    
    def getAllFromDbExceptConfig(self) -> list[str]:
        # Scan operation with a filter expression to exclude the config item
        response = self.dynamodb.scan(
            TableName=self.teamtable,
            FilterExpression=f"{self.partitionkey} <> :configVal",
            ExpressionAttributeValues={
                ':configVal': {'S': self.configpartitionvalue}
            },
            Limit=50
        )
        items = response['Items']
        processedItems = [json.loads(item['data']['S']) for item in items]
        return processedItems

    def getTableConfig(self) -> str:
        response = self.dynamodb.get_item(
            TableName=self.teamtable,
            Key={
                'teamName': {'S': self.configpartitionvalue}
            }
        )
        return response.get('Item', None)
    
    def setTableConfig(self, serializeddata: str):
        self.dynamodb.put_item(
            TableName=self.teamtable,
            Item={
                self.partitionkey: {'S': self.configpartitionvalue},
                'data': {'S': serializeddata}
            }
        )

    def setPrediction(self, date: str, serializeddataList: list[str]):
        self.dynamodb.put_item(
            TableName=self.prediction_table,
            Item = {
                self.prediction_partitionkey: {'S': date},
                'data': {'L': [{'S': item} for item in serializeddataList]}
            }
        )

    