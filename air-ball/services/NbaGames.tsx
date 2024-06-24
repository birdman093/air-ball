import { nbaGame, createNbaGame } from "@/datatypes/apigame";
import { convertUTCtoPSTString, nbaGamesNextDayDate } from "@/util/date";

export const NbaGames = async (gameDate: string) => {   
    const results1 = await NbaGamesRequest(gameDate);
    const results2 = await NbaGamesRequest(nbaGamesNextDayDate(gameDate));
    const nbaGamesResults = results1.concat(results2);

    let games: nbaGame[] = []
    for (const game of nbaGamesResults) {
        const pstDate = convertUTCtoPSTString(game.date.start)
        
        if (pstDate == gameDate){
            const newGame = createNbaGame({
                hometeam: game.teams.home.name,
                awayteam: game.teams.visitors.name,
                hometeam_abbr: game.teams.home.code,
                awayteam_abbr: game.teams.visitors.code,
                hometeamimageurl: game.teams.home.logo,
                awayteamimageurl: game.teams.visitors.logo,
                gametime: new Date(game.date.start).toISOString()
            })
            games.push(newGame);
        }
    }  
    return games;
}

const NbaGamesRequest = async (gameDate: string) => {
    const url = `https://api-nba-v1.p.rapidapi.com/games?date=${gameDate}`;
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
        return nbagamesresults.response ?? [];
    } catch (error) {
        console.error(error);
        return []
    }
}

