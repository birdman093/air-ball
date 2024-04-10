import { nbaGame } from '@/datatypes/apigame'
import { lineToString, lineToImg, lineToImgAirBall } from '@/util/rounding'
import { getTeamAbbreviation, getTeamImage } from '@/util/getTeamAbbreviation'
import { TeamDisplay } from './teamDisplay'
import { calculateGradientColor } from '@/util/conditional'
import '../styles/teams.css';
import '../styles/today.css';

export function gameTable(games: nbaGame[]) {

    return (
    <table className="games">
      <thead>
        <tr>
          <th></th>
          <th></th>
          <th></th>
          <th>Game Time</th>
          <th colSpan={2}>DraftKings</th>
          <th colSpan={2}>Project Air Ball</th>
          <th>A-B Index</th>
        </tr>
      </thead>
      <tbody className="games-row">
        {games.map((game, index) => { 
          let difference = 0
          if (game.hometeamline < 100 && game.homeairballline < 100) {
            difference = Math.abs(game.hometeamline - game.homeairballline);
          }

          let borderColor = 'transparent';
          if (difference >= 10) {
            borderColor = 'red';
          } else if (difference >= 7){
            borderColor = '#FA8320';
          } 
          else if (difference >= 5 ){
            borderColor = 'yellow';
          }    
          
          let trStyle;
          if (borderColor == 'transparent'){
            trStyle = {}

          } else {
            trStyle = {
              margin: '2px',
              outline: `2px solid ${borderColor}`
            };
          }
          

          return ( 
          <tr key={index} style={trStyle}>
            <td className='td-img' >
              <TeamDisplay imageUrl={game.hometeamimageurl} abbreviation={game.hometeam_abbr} />
            </td>
            <td className='td-img'>
              {'@'}
            </td>
            <td className='td-img'>
              <TeamDisplay imageUrl={game.awayteamimageurl} abbreviation={game.awayteam_abbr} />
            </td>
            <td>{new Date(game.gametime).toLocaleTimeString()}</td>
            <td className='img-line-left'>
              {lineToImg(game.hometeamline, game.hometeamimageurl, game.awayteamimageurl)}
            </td>
            <td className='img-line-right'>
              {lineToString(game.hometeamline, game.hometeam_abbr, game.awayteam_abbr)}
            </td>
            <td className='img-line-left'>
              {lineToImg(game.homeairballline, game.hometeamimageurl, 
              game.awayteamimageurl)}
            </td>
            <td className='img-line-right'>
              {lineToString(game.homeairballline, game.hometeam_abbr, 
                game.awayteam_abbr)} 
            </td>
            <td className='td-img'>
              {lineToImgAirBall(difference)}
            </td>
          </tr>
      )})}
    </tbody>
    </table>)
}

export function pastGameTable(games: nbaGame[]) {
  return (
  <table className="games">
    <thead>
      <tr>
        <th></th>
        <th></th>
        <th></th>
        <th>DraftKings</th>
        <th>Air-Ball</th>
        <th>Result</th>
      </tr>
    </thead>
    <tbody className="games-row">
      {games.map((game, index) => (
      <tr key={index}>
        <td className='td-img'>
            <TeamDisplay imageUrl={getTeamImage(game.hometeam)} 
              abbreviation={getTeamAbbreviation(game.hometeam)} />
          </td>
          <td className='td-img'>
            {'@'}
          </td>
          <td className='td-img'>
            <TeamDisplay imageUrl={getTeamImage(game.awayteam)} 
            abbreviation={getTeamAbbreviation(game.awayteam)} />
          </td>
          <td>{lineToString(game.hometeamline, 
            getTeamAbbreviation(game.hometeam), 
            getTeamAbbreviation(game.awayteam))}</td>
          <td>{lineToString(game.homeairballline, 
          getTeamAbbreviation(game.hometeam), 
            getTeamAbbreviation(game.awayteam))}</td>
          <td>{lineToString(game.hometeamresult, 
          getTeamAbbreviation(game.hometeam), 
            getTeamAbbreviation(game.awayteam))}</td>
      </tr>
      ))}
  </tbody>
  </table>)
}