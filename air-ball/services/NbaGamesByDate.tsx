import { nbaGame, createNbaGame } from "@/datatypes/apigame";
import { nbaGamesNextDayDate as nbaGamesApiDate } from "@/util/date";
import { NbaOdds } from "./NbaOdds";
import { AirBall } from "./Airball";
import { mergeNbaApis } from "@/util/mergeNbaApis";
import { NbaGames } from "./NbaGames";


export const NbaGamesByDate = async (gameDate: string) => {
    //const nbaGamesWithOdds  = await NbaOdds(gameDate);
    const nbaGamesWithAirBall = await AirBall(gameDate);
    const nbaGames = await NbaGames(gameDate);
    return mergeNbaApis(nbaGames, [], nbaGamesWithAirBall)
}

export const PastNbaGamesByDate = async (gameDate: string) => {
    const nbaGamesWithAirBall = await AirBall(gameDate);
    return nbaGamesWithAirBall;
}

