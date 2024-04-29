import { nbaGame } from "@/datatypes/apigame";

export const mergeNbaApis = (games: nbaGame[], 
    odds: nbaGame[], airBall: nbaGame[])=> {
        for (const game of games) {
            const hometeam = game.hometeam;
            const awayteam = game.awayteam;

            let oddsMatch = findmatch(hometeam, awayteam, odds);
            let airBallMatch = findmatch(hometeam, awayteam, airBall);

            if (oddsMatch) {
                game.homelineprice = oddsMatch.homelineprice;
                game.awaylineprice = oddsMatch.awaylineprice;
                game.livehometeamline = oddsMatch.hometeamline;
            }

            if (airBallMatch) {
                game.homeairballline = airBallMatch.homeairballline;
                game.hometeamline = airBallMatch.hometeamline;
            }
        }
        return games
}

const findmatch = (hometeam: string, awayteam: string, gamesToMatch: nbaGame[]) => {
    let game = gamesToMatch.find((game) => 
    game.hometeam.trim().toLowerCase() == hometeam.trim().toLowerCase() 
    && game.awayteam.trim().toLowerCase() == awayteam.trim().toLowerCase());
    return game;
}