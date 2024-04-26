import { ReactElement, useEffect, useState } from 'react'
import type { InferGetStaticPropsType, GetStaticProps } from 'next'
import Layout from '../components/layout'
import type { NextPageWithLayout } from './_app'

import { nbaGame } from '@/datatypes/apigame'
import { todayDate } from '@/util/date'
import '../styles/today.css'
import { NbaGamesByDate } from '@/services/NbaGamesByDate'
import { gameTable } from '@/components/gameTable'

const MAXDATE = "2024-06-15"

export const getStaticProps = (async (context) => {
  const today = todayDate(MAXDATE)
  const todaygames: nbaGame[] = await NbaGamesByDate(today);
  console.log(todaygames)
  return { props: { todaygames } }
}) satisfies GetStaticProps<{
  todaygames: nbaGame[]
}>

export default function Daily({
  todaygames,
}: InferGetStaticPropsType<typeof getStaticProps>)
{
  const [games, setGames] = useState<nbaGame[]>([]);
  const today = todayDate(MAXDATE);

  useEffect(() => {
    setGames(todaygames);
  }, []);

  return (
  <div className='scrollableContainer'>
    <h2 className='date'>{today}</h2>
    {gameTable(games)}
  </div>)
}
 
Daily.getLayout = function getLayout(page: ReactElement) {
  return (
    <Layout>
      {page}
    </Layout>
  )
}
