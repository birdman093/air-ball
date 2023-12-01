import { apiGame } from "@/datatypes/apigame";

export const nbaodds = async () => {
    // TODO: get odds
    const url = 'https://odds.p.rapidapi.com/v4/sports?all=true';
    const options: RequestInit = {
      method: 'GET',
      headers: {
        'X-RapidAPI-Key': process.env.NEXT_PUBLIC_RAPIDAPI_KEY,
        'X-RapidAPI-Host': process.env.NEXT_PUBLIC_RAPIDAPI_ODDS_HOST
      } as HeadersInit
    };

    try {
      const response = await fetch(url, options);
      const result = await response.text();
      console.log(result);
    } catch (error) {
      console.error(error);
    }
}