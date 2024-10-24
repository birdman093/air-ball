import boto3, json, os
from dotenv import load_dotenv
from botocore.config import Config

class AwsTableDb:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, '../credentials', '.env.local')
        load_dotenv(env_path)
        self.my_config = Config(
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        self.dynamodb = boto3.client('dynamodb', 
            aws_access_key_id=os.getenv('AWS_IAM_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_IAM_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION'),
            config=self.my_config)

        # team data
        self.teamtable = 'airBallDb_24_25' #Yearly Table
        self.partitionkey = 'teamName'
        self.configpartitionvalue = 'Configuration'
        self.performance_partition_value = 'Performance'

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
                raise Exception(f"ERROR: Following items were not batch added: {unprocessed_items}")



    def getFromDb(self, partitionkey: str) -> str:
        response = self.dynamodb.get_item(
            TableName=self.teamtable,
            Key={
                self.partitionkey: {'S': partitionkey}
            }
        )
        response = response.get('Item', None)
        if response and 'data' in response and 'S' in response['data']:
            return json.loads(response['data']['S'])
        else:
            return ""
    
    def getAllFromDbExceptConfig(self) -> list[str]:
        # Scan operation with a filter expression to exclude the config item
        response = self.dynamodb.scan(
            TableName=self.teamtable,
        FilterExpression=f"{self.partitionkey} <> :configVal AND {self.partitionkey} <> :performanceVal",
        ExpressionAttributeValues={
            ':configVal': {'S': self.configpartitionvalue},
            ':performanceVal': {'S': self.performance_partition_value}
        },
        Limit=50
        )
        items = response['Items']
        processedItems = [json.loads(item['data']['S']) for item in items]
        return processedItems

    def getTableConfig(self) -> dict:
        response = self.dynamodb.get_item(
            TableName=self.teamtable,
            Key={
                self.partitionkey: {'S': self.configpartitionvalue}
            }
        )
        response = response.get('Item', None)
        if response and 'data' in response and 'S' in response['data']:
            return json.loads(response['data']['S'])
        else:
            return {}
    
    def setTableConfig(self, serializeddata: str):
        self.dynamodb.put_item(
            TableName=self.teamtable,
            Item={
                self.partitionkey: {'S': self.configpartitionvalue},
                'data': {'S': serializeddata}
            }
        )

    def getTablePerformance(self) -> dict:
        response = self.dynamodb.get_item(
            TableName=self.teamtable,
            Key={
                self.partitionkey: {'S': self.performance_partition_value}
            }
        )
        response = response.get('Item', None)
        if response and 'data' in response and 'S' in response['data']:
            return json.loads(response['data']['S'])
        else:
            return {}
    
    def setTablePerformance(self, serializeddata: str):
        self.dynamodb.put_item(
            TableName=self.teamtable,
            Item={
                self.partitionkey: {'S': self.performance_partition_value},
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

    def getPredictions(self, dateDashes: str) -> list[str]:
        print(dateDashes)
        response = self.dynamodb.get_item(
            TableName=self.prediction_table,
            Key={
                self.prediction_partitionkey: {'S': dateDashes}
            }
        )
        response = response.get('Item', None)
        if response and 'data' in response and 'L' in response['data']:
            return [ result['S'] for result in response['data']['L']]
        else:
            return []

    