import { ReactElement, useEffect, useState } from 'react'
import type { InferGetStaticPropsType, GetStaticProps } from 'next'
import Layout from '../components/layout'
import type { NextPageWithLayout } from './_app'

import { nbaGame } from '@/datatypes/apigame'
import { todayDate } from '@/util/date'
import '../styles/today.css'
import { NbaGamesByDate } from '@/services/NbaGamesByDate'
import { lineToString } from '@/util/rounding'

const MINDATE = "2024-04-02"
const MAXDATE = "2024-04-14"

export const getStaticProps = (async (context) => {
  const today = todayDate(MAXDATE)
  const todaygames: nbaGame[] = await NbaGamesByDate(today);
  return { props: { todaygames } }
}) satisfies GetStaticProps<{
  todaygames: nbaGame[]
}>

export default function Today({
  todaygames,
}: InferGetStaticPropsType<typeof getStaticProps>)
{

  const [games, setGames] = useState<nbaGame[]>([])
  const [today, setToday] = useState(todayDate(MAXDATE))

  // Initialize games
  useEffect(() => {
    setGames(todaygames);
  }, []);

  // Update games on change
  // TODO:


  return (
  <div>
    <input
      type="date"
      className="date"
      min={MINDATE}
      max={MAXDATE}
      value={today} // Ensure 'today' is in 'YYYY-MM-DD' format and within the min-max range
      onChange={(e) => setToday(e.target.value)} // Assuming you have a method to update the date
    />

    <table className="today-games">
      <thead>
        <tr>
          <th>Game</th>
          <th>Game Time</th>
          <th>DraftKings</th>
          <th>Air-Ball</th>
        </tr>
      </thead>
      <tbody>
        {games.map((game, index) => (
        <tr key={index}>
          <td>{game.awayteam}@{game.hometeam}</td>
          <td>{new Date(game.gametime).toLocaleTimeString()}</td>
          <td>{lineToString(game.hometeamline, game.hometeam_abbr, 
            game.awayteam_abbr)}</td>
          <td>{lineToString(game.homeairballline, game.hometeam_abbr, 
            game.awayteam_abbr)} </td>
        </tr>
        ))}
    </tbody>
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
