import { nbaGame } from '@/datatypes/apigame'
import { lineToString, lineToImg, lineToImgAirBall, roundLine } from '@/util/rounding'
import { getTeamAbbreviation, getTeamImage } from '@/util/getTeamAbbreviation'
import { TeamDisplay } from './teamDisplay'
import { calculateGradientColor } from '@/util/conditional'
//import Slider from '@mui/base/Slider';
import { CustomSlider } from './customSlider'
import '../styles/teams.css';
import '../styles/today.css';
import { Tooltip } from '@mui/material'

const INVALID_BET = 999;
const MIN_SLIDER = -15;
const MAX_SLIDER = 15;

export function gameTable(games: nbaGame[]) {
    return (
    <table className="games">
      <thead>
        <tr>
          <th></th>
          <th></th>
          <th></th>
          <th>Game Time</th>
          <th colSpan={2}>GameLine</th>
          <th colSpan={2}>Air Ball</th>
          <th colSpan={1}>Air Ball Slider</th>
          <th>Differential</th>
          <th>A-B Favorite</th>
        </tr>
      </thead>
      <tbody className="games-row">
        {games.map((game, index) => { 
          const difference = Math.abs(game.homeairballline) === INVALID_BET ? 
          0 : Math.abs(game.hometeamline - game.homeairballline);

          let borderColor = 'transparent';
          if (difference >= 10) {
            borderColor = 'red';
          } else if (difference >= 7){
            borderColor = '#FA8320';
          } else if (difference >= 5 ){
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

          const marks = [ 
            { value: -1*game.hometeamline, image: "./fan-duel.png" },
            { value: -1*roundLine(game.homeairballline), image: "./air-ball.png" }
          ];

          return ( 
          <tr key={index} style={trStyle}>   
            <td className='td-img'>
              <TeamDisplay imageUrl={getTeamImage(game.awayteam)} abbreviation={game.awayteam_abbr} />
            </td>
            <td className='td-img'>
              {'@'}
            </td>
            <td className='td-img' >
              <TeamDisplay imageUrl={getTeamImage(game.hometeam)} abbreviation={game.hometeam_abbr} />
            </td>
            <td>{new Date(game.gametime).toLocaleTimeString()}</td>
            <td className='img-line-left'>
              {lineToImg(game.hometeamline, getTeamImage(game.hometeam), 
              getTeamImage(game.awayteam))}
            </td>
            <td className='img-line-right'>
              {lineToString(game.hometeamline, game.hometeam_abbr, game.awayteam_abbr)}
            </td>
            <td className='img-line-left'>
              {lineToImg(game.homeairballline, getTeamImage(game.hometeam), 
              getTeamImage(game.awayteam))}
            </td>
            <td className='img-line-right'>
              {lineToString(game.homeairballline, game.hometeam_abbr, 
                game.awayteam_abbr)} 
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
              <div style={{ flexGrow: 1, padding: "0", textAlign: "center" }}>

              
              <CustomSlider
                contentEditable={false}
                marks={marks}
                step={0.5}
                min={Math.min(MIN_SLIDER, marks.reduce((min, obj) => Math.min(min, obj.value), Infinity))}
                max={Math.max(MAX_SLIDER, marks.reduce((min, obj) => Math.min(min, obj.value), Infinity))}
                slots={{
                  mark: ({ className, style, 'data-index': index }) => {
                    const mark = marks[index];
                    return (
                      <Tooltip title={mark?.value}>
                        <div
                          className={className}
                          style={{
                            ...style,
                            backgroundImage: `url(${mark?.image})`,
                          }}
                        />
                      </Tooltip>
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
            <td>
              {roundLine(-1*game.homeairballline - (-1* game.hometeamline))}
            </td>
            <td className='td-img'>
              {game.homeairballline === game.hometeamline ? 
              null : <img className="team-image" 
              src={getTeamImage(game.homeairballline < game.hometeamline 
                ? game.hometeam : game.awayteam)}/>
              }
            </td>
          </tr>
      )})}
    </tbody>
    </table>)
}
