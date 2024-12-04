import { nbaGame } from '@/datatypes/apigame'
import { lineToString, lineToImg, lineToImgAirBall, roundLine } from '@/util/rounding'
import { getTeamAbbreviation, getTeamImage } from '@/util/getTeamAbbreviation'
import { TeamDisplay } from './teamDisplay'
import { calculateGradientColor } from '@/util/conditional'
import { CustomSlider } from './customSlider'
import '../styles/teams.css';
import '../styles/today.css';
import { Tooltip } from '@mui/material'

const MIN_SLIDER = -15;
const MAX_SLIDER = 15;

export function pastGameTable(games: nbaGame[]) {
  return (
  <table className="games">
    <thead>
      <tr>
        <th></th>
        <th></th>
        <th></th>
        <th colSpan={2}>GameLine</th>
        <th colSpan={2}>Air-Ball</th>
        <th colSpan={2}>Result</th>
        <th colSpan={1}>Air-Ball Slider</th>
      </tr>
    </thead>
    <tbody className="games-row">
      {games.map((game, index) => {
        const marks = [
        { value: -1*game.hometeamline, image: "./fan-duel.png" },
        { value: -1*roundLine(game.homeairballline), image: "./air-ball.png" },
        { value: -1*game.hometeamresult, 
          image: game.hometeamresult < 0 ? getTeamImage(game.hometeam) : getTeamImage(game.awayteam)}
        ];

        return (
        <tr key={index}>
          <td className='td-img'>
              <TeamDisplay imageUrl={getTeamImage(game.awayteam)} 
                abbreviation={getTeamAbbreviation(game.awayteam)} />
            </td>
            <td className='td-img'>
              {'@'}
            </td>
            <td className='td-img'>
              <TeamDisplay imageUrl={getTeamImage(game.hometeam)} 
              abbreviation={getTeamAbbreviation(game.hometeam)} />
            </td>
            <td className='img-line-left'>
                {lineToImg(game.hometeamline, 
                  getTeamImage(game.hometeam), 
                  getTeamImage(game.awayteam))}
            </td>
            <td className='img-line-right'>
              {lineToString(game.hometeamline, 
                getTeamAbbreviation(game.hometeam), 
                getTeamAbbreviation(game.awayteam))}
            </td>
            <td className='img-line-left'>
                {lineToImg(game.homeairballline, 
                  getTeamImage(game.hometeam), 
                  getTeamImage(game.awayteam))}
            </td>
            <td className='img-line-right'>
              {lineToString(game.homeairballline, 
                getTeamAbbreviation(game.hometeam), 
                getTeamAbbreviation(game.awayteam))}
            </td>
            <td className='img-line-left'>
                {lineToImg(game.hometeamresult, 
                  getTeamImage(game.hometeam), 
                  getTeamImage(game.awayteam))}
            </td>
            <td className='img-line-right'>
              {lineToString(game.hometeamresult, 
                getTeamAbbreviation(game.hometeam), 
                getTeamAbbreviation(game.awayteam))}
            </td>
            <td style={{ width: "400px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                {/* Left Logo */}
                <div style={{ width: "75px", textAlign: "center" }}>
                    <img
                        className="team-image"
                        src={getTeamImage(game.awayteam)}
                        alt="Away Team Logo"
                    />
                </div>

                {/* Slider */}
                <div style={{ flexGrow: 1, padding: "0", textAlign: "center" }}>
                    <CustomSlider
                        contentEditable={false}
                        marks={marks}
                        step={0.5}
                        min={Math.min(
                            MIN_SLIDER,
                            marks.reduce((min, obj) => Math.min(min, obj.value), Infinity)
                        )}
                        max={Math.max(
                            MAX_SLIDER,
                            marks.reduce((min, obj) => Math.max(min, obj.value), -1*Infinity)
                        )}
                        slots={{
                            mark: ({ className, style, "data-index": index }) => {
                                const mark = marks[index];
                                return mark?.image ? (
                                    <Tooltip title={mark?.value}>
                                        <div
                                            className={className}
                                            style={{
                                                ...style,
                                                backgroundImage: `url(${mark?.image})`,
                                            }}
                                        />
                                    </Tooltip>
                                ) : (
                                    <div style={{}} />
                                );
                            },
                        }}
                    />
                </div>

                {/* Right Logo */}
                <div style={{ width: "75px", textAlign: "center" }}>
                    <img
                        className="team-image"
                        style={{ paddingLeft: "5px" }}
                        src={getTeamImage(game.hometeam)}
                        alt="Home Team Logo"
                    />
                </div>
            </td>

        </tr>)
    })}
  </tbody>
  </table>)
}