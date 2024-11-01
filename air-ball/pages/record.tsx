import React, { ReactElement, useState } from 'react';
import type { GetServerSidePropsContext, InferGetServerSidePropsType } from 'next';
import Layout from '../components/layout';
import { NextPageWithLayout } from './_app';
import { useRouter } from 'next/router';

import { nbaGame } from '@/datatypes/apigame';
import { todayDate, yesterdayDate, dateWithinAllowableDateRanges } from '@/util/date';
import '../styles/today.css';
import { PastNbaGamesByDate } from '@/services/NbaGamesByDate';
import { pastGameTable } from '@/components/gameTable';
import { END_AIR_BALL, BEGIN_AIR_BALL } from '@/season_config/dateRanges';

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const pastDate = context.query.date as string || yesterdayDate(END_AIR_BALL);
  console.log(pastDate);
  const pastGames: nbaGame[] = await PastNbaGamesByDate(pastDate);
  return { props: { pastGames } };
}

type GameProps = InferGetServerSidePropsType<typeof getServerSideProps>;

const PastPicks: NextPageWithLayout<GameProps> = ({ pastGames }) => {
  const router = useRouter();
  const [date, setDate] = useState(yesterdayDate(END_AIR_BALL));
  const [loading, setLoading] = useState(false);

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLoading(true);
    const newDate = e.target.value;
    setDate(newDate);
    router.push(`/record?date=${newDate}`).then(() => setLoading(false));
  };

  const isDateAllowed = (date: string) => {
    return dateWithinAllowableDateRanges(date);
  };

  return (
    <div className='scrollableContainer'>
      <input
        type="date"
        className={`yesterday-date ${isDateAllowed(date) ? 'allowed' : 'not-allowed'}`}
        min={BEGIN_AIR_BALL}
        max={END_AIR_BALL}
        value={date}
        onChange={handleDateChange}
      />
      {loading ? (
        <div>Loading...</div>
      ) : (
        isDateAllowed(date) ? pastGameTable(pastGames) : <div>Invalid Time Range - No Air Ball Data</div>
      )}
    </div>
  );
};

PastPicks.getLayout = function getLayout(page: ReactElement) {
  return <Layout>{page}</Layout>;
};

export default PastPicks;
