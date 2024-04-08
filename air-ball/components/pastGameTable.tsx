import { nbaGame } from '@/datatypes/apigame'
import { lineToString } from '@/util/rounding'
import { getTeamAbbreviation } from '@/util/getTeamAbbreviation'

export function pastGameTable(games: nbaGame[]) {
    return (
    <table className="today-games">
      <thead>
        <tr>
          <th>Game</th>
          <th>DraftKings</th>
          <th>Air-Ball</th>
          <th>Result</th>
        </tr>
      </thead>
      <tbody>
        {games.map((game, index) => (
        <tr key={index}>
          <td>{game.awayteam}@{game.hometeam}</td>
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