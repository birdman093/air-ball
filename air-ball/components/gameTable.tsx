import { nbaGame } from '@/datatypes/apigame'
import { lineToString, lineToImg, lineToImgAirBall } from '@/util/rounding'
import { getTeamAbbreviation, getTeamImage } from '@/util/getTeamAbbreviation'
import { TeamDisplay } from './teamDisplay'
import { calculateGradientColor } from '@/util/conditional'
//import Slider from '@mui/base/Slider';
import Slider from '@mui/material/Slider';
import { styled } from '@mui/system';
import '../styles/teams.css';
import '../styles/today.css';

const INVALID_BET = 999;
const MIN_SLIDER = -20;
const MAX_SLIDER = 20;

const CustomSlider = styled(Slider)`
  width: 80%;
  margin: 40px auto;
  position: relative;
  margin: 20px auto; /* Adjust margin if needed */
  padding: 0; /* Remove extra padding around the slider */

  & .MuiSlider-root {
    display: none; /* Hide the slider */
  }

  /* Optional: If specific elements need explicit hiding */
  & .MuiSlider-track,
  & .MuiSlider-thumb {
    display: none; /* Explicitly hide all slider components */
  }

  & .MuiSlider-mark {
    width: 36px; /* Adjust image size */
    height: 36px;
    border-radius: 50%;
    background-size: cover;
    background-position: center;
    position: absolute;
    top: 50%; /* Align vertically over the slider */
    transform: translate(-50%, -50%); /* Center on the mark position */
    background-color: #ccc;
  }

  & .MuiSlider-track {
    position: relative;
    height: 8px; /* Adjust height of the slider track */
    background-color: #ccc; /* Blue slider color */
  }

  & .MuiSlider-rail {
    height: 8px; /* Same as track height for consistency */
    background-color: #ccc; /* Grey color for inactive part */
  }
`;

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
          <th colSpan={2}>Project Air Ball</th>
          <th>A-B Index</th>
          <th colSpan={1}>A-B Slider</th>
          <th>A-B Favorite</th>
        </tr>
      </thead>
      <tbody className="games-row">
        {games.map((game, index) => { 
          console.log(game.homeairballline)
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
            { value: game.hometeamline, image: "./fan-duel.png" },
            { value: game.homeairballline, image: "./air-ball.png" }
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
            <td className='td-img'>
              {lineToImgAirBall(difference)}
            </td>
            <td style={{width: "400px"}}>
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
                      <div
                        className={className}
                        style={{
                          ...style,
                          backgroundImage: `url(${mark?.image})`,
                        }}
                      />
                    );
                  },
                }}
              />
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
        <th colSpan={1}></th>
      </tr>
    </thead>
    <tbody className="games-row">
      {games.map((game, index) => {
        const marks = [
        { value: game.hometeamline, image: "./fan-duel.png" },
        { value: game.homeairballline, image: "./air-ball.png" },
        { value: game.hometeamresult, 
          image: game.hometeamresult < 0 ? getTeamImage(game.hometeam) : getTeamImage(game.awayteam)},
        ];

        return (
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
            <td style={{width: "400px"}}>
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
                        <div
                          className={className}
                          style={{
                            ...style,
                            backgroundImage: `url(${mark?.image})`,
                          }}
                        />
                      );
                    },
                  }}
                />
              </td>
        </tr>)
    })}
  </tbody>
  </table>)
}