import { apiGame } from "@/datatypes/apigame";

export const nbaodds = async () => {
    const nbakey = "basketball_nba";

    const url = `https://odds.p.rapidapi.com/v4/sports/${nbakey}/odds?regions=us&oddsFormat=decimal&markets=spreads&dateFormat=iso`;
    const options: RequestInit = {
        method: 'GET',
        headers: {
        'X-RapidAPI-Key': process.env.NEXT_PUBLIC_RAPIDAPI_KEY,
        'X-RapidAPI-Host': process.env.NEXT_PUBLIC_RAPIDAPI_ODDS_HOST
         } as HeadersInit
    };

    let result;
    try {
        const response = await fetch(url, options);
        result = await response.json();
    } catch (error) {
        console.error(error);
    }

    let apiGames: apiGame[] = []
    result.forEach(function(game: any) {
        let homelineprice = -1; let awaylineprice = -1; let spread = -1; let favorite = "";
        try {
            const draftkings = game.bookmakers.find((booker: any) => booker['key'] === 'draftkings');
            const spreads = draftkings.markets[0]['outcomes'];

            console.log(game.home_team == spreads[0].name)

            if (spreads[0].name == game.home_team) {
                homelineprice = spreads[0].price
                awaylineprice = spreads[1].price
            } else {
                homelineprice = spreads[1].price
                awaylineprice = spreads[0].price
            }
            spread = Math.min(spreads[0].point, spreads[1].point)
            if (spread == spreads[0].point) {
                favorite = spreads[0].name;
            } else {
                favorite = spreads[1].name;
            }
        }
        catch {
            console.error(`odds api data not available for 
            ${game.away_team} vs. ${game.home_team}`)
            return;
        }

        let newGame: apiGame = {
            hometeam: game.home_team,
            awayteam: game.away_team,
            gametime: game.commence_time,
            line: spread,
            favorite: favorite,
            homelineprice: homelineprice, 
            awaylineprice: awaylineprice
            };
        
        apiGames.push(newGame)
    });
    
    return apiGames
}