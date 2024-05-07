<div align="center">
<img max-height='200px' src='air-ball/public/air-ball.png'>
</div>

# Project Air Ball
Project Air Ball is a machine learning model, seasonal data aggregation, and 
frontend built using data from the NBA API

<img max-height='400px' src='air-ball/public/dailypicks.png'>

## Website
https://air-ball.vercel.app

## Technology, Deployment, and Architecture

### Frontend (air-ball)
```
Next.js with TypeScript
Hosted: Vercel
```

### Data and Prediction Backend (air-ball-stats)
```
Python with Type Hints
Hosted: Docker Container on AWS Lambda
Logging: EventBridge, CloudWatch, SMS
```

### Season Data and Air-Ball Predictions Database
```
DynamoDB on AWS
``````

### APIs
```
NBA API Python Module
Live Sports Odds on RapidAPI 
API-NBA on RapidAPI
Air-Ball API hosted on EC2 
```

### Architecture:

<img max-height='200px' src='air-ball/public/architecture.png'>

## Project Air Ball ML Model
https://github.com/ryan-t-mitchell/nba_predictions

## Screenshots
### Full Website
<img max-height='200px' src='air-ball/public/fullsite.png'>

### Daily Picks
<img max-height='200px' src='air-ball/public/dailypicks2.png'>

### Record Picks
<img max-height='200px' src='air-ball/public/recordpicks.png'>
