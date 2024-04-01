import { nbaGame } from "@/datatypes/apigame";
import AWS from 'aws-sdk';


export const AirBall = async (gameDate : string) => {
    getPredictionData(gameDate);

}

const getPredictionData = async (gameDate: string) => {
    AWS.config.update({ region: 'us-east-2' });
    const dynamoDb = new AWS.DynamoDB.DocumentClient();

    const params = {
        TableName: 'predictionDb',
        KeyConditionExpression: 'gamedate = :gamedate',
        ExpressionAttributeValues: {
            ':gamedate': gameDate,
        },
    };

    try {
        const response = await dynamoDb.query(params).promise();
        console.log('Success:', response.Items);
        return response.Items;
    } catch (error) {
        console.error('Error:', error);
    }
    
};