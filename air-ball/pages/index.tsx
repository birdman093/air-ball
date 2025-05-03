import { ReactElement, useEffect, useState } from 'react'
//import type { InferGetStaticPropsType, GetStaticProps } from 'next'
import { GetServerSideProps, InferGetServerSidePropsType } from 'next';
import Layout from '../components/layout'
import type { NextPageWithLayout } from './_app'

import { nbaGame } from '@/datatypes/apigame'
import { todayDate } from '@/util/date'
import '../styles/today.css'
import { NbaGamesByDate } from '@/services/NbaGamesByDate'
import { gameTable } from '@/components/gameTable'

export const getServerSideProps: GetServerSideProps<{
  todaygames: nbaGame[],
  today: string
}> = async (context) => {
  const today = todayDate();
  const todaygames: nbaGame[] = await NbaGamesByDate(today);
  return { props: { todaygames, today} };
};

export default function Daily({
  todaygames, today,
}: InferGetServerSidePropsType<typeof getServerSideProps>) {
  const [games, setGames] = useState<nbaGame[]>([]);
  
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
