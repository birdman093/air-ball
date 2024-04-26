import { ReactElement, useState } from 'react';
import type { GetServerSidePropsContext, InferGetServerSidePropsType } from 'next';
import Layout from '../components/layout';
import { nbaGame } from '@/datatypes/apigame';
import { yesterdayDate } from '@/util/date';
import '../styles/today.css';
import { PastNbaGamesByDate } from '@/services/NbaGamesByDate';
import { pastGameTable } from '@/components/gameTable';
import { NextPageWithLayout } from './_app';
import { useRouter } from 'next/router';

const MINDATE = "2024-04-02";
const MAXDATE = "2024-06-15";

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const pastDate = context.query.date as string || yesterdayDate(MAXDATE);
  const pastGames: nbaGame[] = await PastNbaGamesByDate(pastDate);
  return { props: { pastGames } };
}

type GameProps = InferGetServerSidePropsType<typeof getServerSideProps>;

const PastPicks: NextPageWithLayout<GameProps> = ({ pastGames }) => {
  const router = useRouter();
  const [date, setDate] = useState(yesterdayDate(MAXDATE));

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newDate = e.target.value;
    setDate(newDate);
    router.push(`/record?date=${newDate}`);
  };

  return (
    <div className='scrollableContainer'>
      <input
        type="date"
        className="yesterday-date"
        min={MINDATE}
        max={MAXDATE}
        value={date}
        onChange={handleDateChange}
      />
      {pastGameTable(pastGames)}
    </div>
  );
};

PastPicks.getLayout = function getLayout(page: ReactElement) {
  return <Layout>{page}</Layout>;
};

export default PastPicks;
