import { ReactElement, useEffect, useState } from 'react'
import Layout from '../components/layout'
import type { NextPageWithLayout } from './_app'
import { apiGame } from '@/datatypes/apigame'
import { nbagames } from '@/services/games/nbagames'
import { todayDate } from '@/util/date'
import '../styles/today.css'
 
const Today: NextPageWithLayout = () => {
  const [games, setGames] = useState<apiGame[]>([])

  const today = todayDate();

  useEffect(() => {
    nbagames(today, setGames);
  }, []);


  return (
  <div>
    <div className="date">
    {today}
    </div>
    <table className="today-games">
      <thead>
        <tr>
          <th>Game</th>
          <th>Time</th>
          <th>Line</th>
          <th>AB Line</th>
        </tr>
      </thead>
      <tbody></tbody>
      {games.map((game, index) => (
      <tr key={index}>
        <td>{game.awayteam}@{game.hometeam}</td>
        <td>{game.gametime.toLocaleTimeString()}</td>
        <td>N/A</td>
        <td>N/A</td>
      </tr>
    ))}
    </table>
  </div>)
}
 
Today.getLayout = function getLayout(page: ReactElement) {
  return (
    <Layout>
      {page}
    </Layout>
  )
}
 
export default Today