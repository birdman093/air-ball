import { nbaGame, createNbaGame } from "@/datatypes/apigame";
import { isDateToday } from "@/util/date";
import { create } from "domain";

export const NbaOdds = async (gameDate: string) => {
    // Currently odds only work on current day
    if (!isDateToday(gameDate)) {
        return []
    }

    const nbakey = "basketball_nba";
    const url = `https://odds.p.rapidapi.com/v4/sports/${nbakey}/odds?regions=us&oddsFormat=decimal&markets=spreads&dateFormat=iso`;
    const options: RequestInit = {
        method: 'GET',
        headers: {
        'X-RapidAPI-Key': process.env.NEXT_PUBLIC_RAPIDAPI_KEY,
        'X-RapidAPI-Host': process.env.NEXT_PUBLIC_RAPIDAPI_ODDS_HOST
         } as HeadersInit
    };

    try {
        const response = await fetch(url, options);
        const result = await response.json();
        return ProcessNbaOdds(result)
    } catch (error) {
        console.error(error);
        return ProcessNbaOdds([])
    } 
}

const ProcessNbaOdds = (result: any) => {
    let nbaGamesWithOdds: nbaGame[] = []
    result.forEach(function(game: any) {
        let homelineprice = -1; let awaylineprice = -1; let spread = -1; let favorite = "";
        try {
            const draftkings = game.bookmakers.find((booker: any) => booker['key'] === 'draftkings');
            const spreads = draftkings.markets[0]['outcomes'];

            if (spreads[0].name == game.home_team) {
                homelineprice = spreads[0].price
                awaylineprice = spreads[1].price
                spread = spreads[0].point
            } else {
                homelineprice = spreads[1].price
                awaylineprice = spreads[0].price
            }
        }
        catch {
            console.error(`odds api data not available for 
            ${game.away_team} vs. ${game.home_team}`)
            return;
        }

        const newGame: nbaGame = createNbaGame({
            hometeam: game.home_team,
            awayteam: game.away_team,
            gametime: game.commence_time,
            hometeamline: spread,
            homelineprice: homelineprice, 
            awaylineprice: awaylineprice
            });
        
        nbaGamesWithOdds.push(newGame)
    });
    
    return nbaGamesWithOdds
}