import { nbaGame } from "@/datatypes/apigame";

export const roundLine = (line: number) => {
    return Math.round(line * 4) / 4;
}

export const lineToString = (hometeamline: number, 
    hometeam_aabr: string, awayteam_aabr: string) => {
    if (Math.abs(hometeamline) > 100){
        return `N/A`
    } else {
        const homelinevalue = roundLine(hometeamline);
        if (homelinevalue === 0){
            return `Even`
        } else if (homelinevalue > 0) {
            return `${awayteam_aabr} ${-1 * homelinevalue}`
        } else {
            return `${hometeam_aabr} ${homelinevalue}`
        }
    }  
  }

export const lineToImg = (hometeamline: number, 
    hometeam_url: string, awayteam_url: string) => {
    if (Math.abs(hometeamline) > 100){
        return <></>
    } else {
        const homelinevalue = roundLine(hometeamline);
        if (homelinevalue === 0){
            return <></>
        } else if (homelinevalue > 0) {
            return <img className="team-image" src={awayteam_url}/>
        } else {
            return <img className="team-image" src={hometeam_url}/>
        }
    }  
}

export const lineToImgAirBall = (difference: number) => {
    if (difference >= 10){
        return <img className="team-image" src='./air-ball.png'></img>
    } else if (difference >= 7) {
        return <img className="team-image" src='./half-air-ball.png'></img>
    } else {
        return <></>
    }
    
}

  