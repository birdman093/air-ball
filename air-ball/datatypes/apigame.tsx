export type nbaGame = {
    hometeam: string,
    awayteam: string,
    hometeam_abbr: string,
    awayteam_abbr: string,
    hometeamimageurl: string,
    awayteamimageurl: string, 
    gametime: string,
    hometeamline: number,
    hometeamresult: number,
    homelineprice: number,
    awaylineprice: number,
    homeairballline: number
}

export function createNbaGame(gameData: Partial<nbaGame>): nbaGame {
    // Default values
    const defaultValues: Partial<nbaGame> = {
      hometeam: "Home Team",
      awayteam: "Away Team",
      hometeam_abbr: "home",
      awayteam_abbr: "away",
      hometeamimageurl: "N/A",
      awayteamimageurl: "N/A",
      gametime: "00:00",
      hometeamline: 9999,
      hometeamresult: 9999,
      homelineprice: 0,
      awaylineprice: 0,
      homeairballline: 9999
    };
  
    return { ...defaultValues, ...gameData } as nbaGame;
  }
