import React, { ReactElement, useState } from 'react';
import type { GetServerSidePropsContext, InferGetServerSidePropsType } from 'next';
import Layout from '../components/layout';
import { NextPageWithLayout } from './_app';
import { useRouter } from 'next/router';

import { nbaGame } from '@/datatypes/apigame';
import { todayDate } from '@/util/date';
import '../styles/today.css';
import { PastNbaGamesByDate } from '@/services/NbaGamesByDate';
import { pastGameTable } from '@/components/gameTable';
import { endAirBall, beginAirBall } from '@/util/dateRanges';

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const pastDate = context.query.date as string || todayDate();
  console.log(pastDate);
  const pastGames: nbaGame[] = await PastNbaGamesByDate(pastDate);
  return { props: { pastGames } };
}

type GameProps = InferGetServerSidePropsType<typeof getServerSideProps>;

const PastPicks: NextPageWithLayout<GameProps> = ({ pastGames }) => {
  const router = useRouter();
  const [date, setDate] = useState(todayDate());
  const [loading, setLoading] = useState(false);

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLoading(true);
    const newDate = e.target.value;
    setDate(newDate);
    router.push(`/record?date=${newDate}`).then(() => setLoading(false));
  };

  // TODO: list based 
  const isDateAllowed = (date: string) => {
    return date >= beginAirBall && date <= endAirBall;
  };

  return (
    <div className='scrollableContainer'>
      <input
        type="date"
        className={`yesterday-date ${isDateAllowed(date) ? 'allowed' : 'not-allowed'}`}
        min={beginAirBall}
        max={endAirBall}
        value={date}
        onChange={handleDateChange}
      />
      {loading ? (
        <div>Loading...</div>
      ) : (
        pastGameTable(pastGames)
      )}
    </div>
  );
};

PastPicks.getLayout = function getLayout(page: ReactElement) {
  return <Layout>{page}</Layout>;
};

export default PastPicks;
