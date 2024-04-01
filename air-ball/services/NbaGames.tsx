import { nbaGame, createNbaGame } from "@/datatypes/apigame";
import { nbaGamesDate as nbaGamesApiDate } from "@/util/date";

export const NbaGames = async (gameDate: string) => {
    let games: nbaGame[] = []
    const todayAPIDate = nbaGamesApiDate(gameDate);

    const url = `https://api-nba-v1.p.rapidapi.com/games?date=${todayAPIDate}`;
    const options: RequestInit = {
        method: 'GET',
        headers: {
        'X-RapidAPI-Key': process.env.NEXT_PUBLIC_RAPIDAPI_KEY,
        'X-RapidAPI-Host': process.env.NEXT_PUBLIC_RAPIDAPI_NBA_HOST
        } as HeadersInit
    };

    try {
        const response = await fetch(url, options)
        const nbagamesresults = await response.json();
        
        for (const game of nbagamesresults.response) {
            const hometeam = game.teams.home.name;
            const awayteam = game.teams.visitors.name;
            const newGame = createNbaGame({
                hometeam: game.teams.home.name,
                awayteam: game.teams.visitors.name,
                gametime: new Date(game.date.start).toISOString()
            })
            games.push(newGame);
        }  
    } catch (error) {
        console.error(error);
    }
    return games;
}

