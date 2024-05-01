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
```
Frontend/Backend (air-ball) - Next.js w/ TypeScript
Data and Prediction (air-ball-stats) - Docker Container - Python w/ Type Hints
Database - DynamoDB
APIs - NBA API, Live Sports Odds, API-NBA, Air-Ball API
```
```
Next.js Static Content - Vercel
Data and Prediction - AWS Lambda, ECR, EventBridge, CloudWatch, SMS
Database - AWS DynamoDB
```
```
NOTE: Lambda/EventBridge tested but not fully set up due to nba api blocking AWS requests
```
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
