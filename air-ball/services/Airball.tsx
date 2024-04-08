import { createNbaGame, nbaGame } from "@/datatypes/apigame";
import AWS from 'aws-sdk';


export const AirBall = async (gameDate : string) => {
    const predictions = await getPredictionData(gameDate);
    if (predictions?.length === 0 || !predictions) {return [];}
    let games: nbaGame[] = (predictions[0].data).map((prediction: any) => {
        const json = JSON.parse(prediction);
        return createNbaGame({
            hometeam: json.hometeamname,
            awayteam: json.awayteamname,
            hometeamresult: -1 & json.hometeamplusminusresult, // Converts to line
            hometeamline: json.hometeamplusminusodds || 999,
            homeairballline: -1 * json.hometeamplusminusprediction //Converts to line
        });
    });
    return games
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
        return response.Items;
    } catch (error) {
        console.error('Error:', error);
        return []
    }
    
};