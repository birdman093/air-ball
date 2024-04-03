import { nbaGame } from "@/datatypes/apigame";

export const lineToString = (hometeamline: number, 
    hometeam_aabr: string, awayteam_aabr: string) => {
    if (Math.abs(hometeamline) > 100){
        return `N/A - Not Found`
    } else {
        const homelinevalue = Math.round(hometeamline * 4) / 4
        if (homelinevalue === 0){
            return `Even`
        } else if (homelinevalue > 0) {
            return `${awayteam_aabr} ${-1 * homelinevalue}`
        } else {
            return `${hometeam_aabr} ${homelinevalue}`
        }
    }
    
  }
  