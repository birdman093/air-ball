import { nbaGame } from '@/datatypes/apigame'
import { lineToString } from '@/util/rounding'
import '../styles/teams.css';

export function gameTable(games: nbaGame[]) {

    return (
    <table className="today-games">
      <thead>
        <tr>
          <th></th>
          <th></th>
          <th></th>
          <th>Time</th>
          <th>DraftKings</th>
          <th>Air Ball</th>
        </tr>
      </thead>
      <tbody>
        {games.map((game, index) => (
        <tr key={index}>
          <td className='td-img'>
            {game.hometeamimageurl ? (
              <img className="team-image" src={game.hometeamimageurl} alt={game.hometeam_abbr} />
            ) : (
              game.hometeam_abbr
            )}
          </td>
          <td className='td-img'>
            {'@'}
          </td>
          <td className='td-img'>
            {game.awayteamimageurl ? (
              <img className="team-image" src={game.awayteamimageurl} alt={game.awayteam_abbr} />
            ) : (
              game.awayteam_abbr
            )}
          </td>
          <td>{new Date(game.gametime).toLocaleTimeString()}</td>
          <td>{lineToString(game.hometeamline, game.hometeam_abbr, 
            game.awayteam_abbr)}</td>
          <td>{lineToString(game.homeairballline, game.hometeam_abbr, 
            game.awayteam_abbr)} </td>
        </tr>
        ))}
    </tbody>
    </table>)

}