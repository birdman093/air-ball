import { createNbaGame, nbaGame } from "@/datatypes/apigame";
import AWS from 'aws-sdk';

export const AirBall = async (gameDate : string) => {
    const predictions = await getPredictionData(gameDate);
    if (predictions?.length === 0 || !predictions) {return [];}
    let games: nbaGame[] = (predictions[0].data).map((prediction: any) => {
        const json = JSON.parse(prediction);
        console.log(json)
        return createNbaGame({
            hometeam: json.hometeamname,
            awayteam: json.awayteamname,
            hometeamresult: -1 * json.hometeamplusminusresult,
            hometeamline: json.hometeamlineodds || 999,
            homeairballline: -1 * json.hometeamplusminusprediction //Converts to line
        });
    });
    return games
}

export const AirBallPerformance = async(season: string) => {
    updateAWSConfig();
    const dynamoDb = new AWS.DynamoDB.DocumentClient();

    const params = {
        TableName: 'airBallDb_24_25',
        KeyConditionExpression: 'teamName = :teamName',
        ExpressionAttributeValues: {
            ':teamName': "Performance",
        },
    };

    try {
        const response = await dynamoDb.query(params).promise();
        if (response.Items == undefined) {return []}
        return response.Items[0].data;
    } catch (error) {
        console.error('Error:', error);
        return []
    }
}

const getPredictionData = async (gameDate: string) => {
    updateAWSConfig();
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

const updateAWSConfig = () => {
    AWS.config.update({
        accessKeyId: process.env.AWS_IAM_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_IAM_SECRET_ACCESS_KEY,
        region: process.env.AWS_REGION
    });
}
