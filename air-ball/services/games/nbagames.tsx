import { apiGame } from "@/datatypes/apigame";
import { nbaAPIDate } from "@/util/date";
import { nbaodds } from "../odds/odds";
import { Dispatch, SetStateAction } from "react";

export const nbagames = async (todayDate: string, setGames: Dispatch<SetStateAction<apiGame[]>>) => {
    let games: apiGame[] = []

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
        const nbagamesresults = await response.json();

        let oddsgames: apiGame[] = []
        oddsgames = await nbaodds()

        //console.log("nbaodds");
        //oddsgames.forEach( (game) => console.log(`${game.awayteam} vs ${game.hometeam}`))
        console.log(nbagamesresults.response);
        for (const game of nbagamesresults.response) {
            console.log(game)
            const hometeam = game.teams.home.name;
            const awayteam = game.teams.visitors.name;
            let match = findmatch(hometeam, awayteam, oddsgames)
            if(match == null){
                console.error(`odds api data not available for 
                ${awayteam} vs. ${hometeam}`)
                continue;
            }
            match.gametime = new Date(game.date.start);
            games.push(match);
        }  
    } catch (error) {
        console.error(error);
    }
    console.log(games)
    setGames(games)
}

const findmatch = (hometeam: string, awayteam: string, odds: apiGame[]) => {
    let game = odds.find((game) => 
    game.hometeam.trim().toLowerCase() == hometeam.trim().toLowerCase() 
    && game.awayteam.trim().toLowerCase() == awayteam.trim().toLowerCase());

    return game;
}