import React, { ReactElement, useState } from 'react';
import type { GetServerSidePropsContext, InferGetServerSidePropsType } from 'next';
import Layout from '../components/layout';
import { NextPageWithLayout } from './_app';
import '../styles/today.css';

import { AirBallPerformance } from '@/services/Airball';

const BETTING_MAP = "betting_diff_map";
const OVERALL_MAP = "overall_map";

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const performanceMap = await AirBallPerformance("2024-25")
  return { props: { performanceMap } };
}

type GameProps = InferGetServerSidePropsType<typeof getServerSideProps>;

const SeasonStats: NextPageWithLayout<GameProps> = ({ performanceMap }) => {
  // TODO: library to visualize
  return (
    <div className='scrollableContainer'>
      <>{performanceMap}</>
    </div>
  );
};

SeasonStats.getLayout = function getLayout(page: ReactElement) {
  return <Layout>{page}</Layout>;
};

export default SeasonStats;
