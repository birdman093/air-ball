import { ReactElement, useEffect, useState } from 'react'
import type { InferGetStaticPropsType, GetStaticProps } from 'next'
import Layout from '../components/layout'
import type { NextPageWithLayout } from './_app'
import { apiGame } from '@/datatypes/apigame'
import { nbagames } from '@/services/games/nbagames'
import { todayDate } from '@/util/date'
import '../styles/today.css'

export const getStaticProps = (async (context) => {
  const today = todayDate();
  const todaygames: apiGame[] = await nbagames(today);
  return { props: { todaygames } }
}) satisfies GetStaticProps<{
  todaygames: apiGame[]
}>

export default function Today({
  todaygames,
}: InferGetStaticPropsType<typeof getStaticProps>)
{
  
  const [games, setGames] = useState<apiGame[]>([])
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
          <td>{game.favorite} {game.line}</td>
          <td>N/A</td>
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
