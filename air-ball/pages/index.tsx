import { ReactElement, useEffect, useState } from 'react'
import type { InferGetStaticPropsType, GetStaticProps } from 'next'
import Layout from '../components/layout'
import type { NextPageWithLayout } from './_app'
import { nbaGame } from '@/datatypes/apigame'
import { todayDate } from '@/util/date'
import '../styles/today.css'
import { NbaGamesByDate } from '@/services/NbaGamesByDate'

export const getStaticProps = (async (context) => {
  const today = todayDate();
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
  const today = todayDate();

  useEffect(() => {
    setGames(todaygames);
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
          <th>Draftkings</th>
          <th>Air-Ball</th>
        </tr>
      </thead>
      <tbody>
        {games.map((game, index) => (
        <tr key={index}>
          <td>{game.awayteam}@{game.hometeam}</td>
          <td>{new Date(game.gametime).toLocaleTimeString()}</td>
          <td>{game.hometeam} {game.hometeamline}</td>
          <td>{game.hometeam} {game.homeairballline} </td>
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
