import { apiGame } from "@/datatypes/apigame";
import { nbaAPIDate } from "@/util/date";
import { Dispatch, SetStateAction } from "react";

export const nbagames = async (todayDate: string, setGames: Dispatch<SetStateAction<apiGame[]>>) => {
    const games: apiGame[] = []

    // date must be modified by 1 day
    const todayAPIDate = nbaAPIDate(todayDate);

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
        const result = await response.json();
        console.log(result);
        console.log(result.response[0].teams.home.code)
        
        const games: apiGame[] = []
        for (const game of result.response) {
            const newGame: apiGame = {
            hometeam: game.teams.home.code,
            awayteam: game.teams.visitors.code,
            gametime: new Date(game.date.start)
            };
            games.push(newGame);
        }

        
        
    } catch (error) {
        console.error(error);
    }

    //TODO: Call odds and modify games object

    setGames(games)
}