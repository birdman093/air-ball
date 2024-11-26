import React, { ReactElement, useState } from 'react';
import type { GetServerSidePropsContext, InferGetServerSidePropsType } from 'next';
import Layout from '../components/layout';
import { NextPageWithLayout } from './_app';
import '../styles/today.css';
import { BarChart } from '@mui/x-charts/BarChart';

import { AirBallPerformance } from '@/services/Airball';

const BETTING_MAP = "betting_diff_map";
const OVERALL_MAP = "overall_map";
const WIN_ID_SERIES = "auto-generated-id-0";
const WIN = "win";
const LOSS = "loss";
const TIE = "tie";
const EMPTY_RECORD = {
  "win": 0,
  "loss": 0,
  "tie": 0
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const performanceMap = await AirBallPerformance("2024-25")
  return { props: { performanceMap } };
}

type GameProps = InferGetServerSidePropsType<typeof getServerSideProps>;

const SeasonStats: NextPageWithLayout<GameProps> = ({ performanceMap }) => {
  // Many better optimizations but...
  const dictionary: any = JSON.parse(performanceMap);
  const bettingEntries: Record<string, Record<string, number>> = dictionary[BETTING_MAP];
  const keys: number[] = Object.keys(bettingEntries)
    .map(Number)
  const maxKey = Number(Math.max(...keys));
  const minKey = Number(Math.min(...keys));

  const negIncrements: string[] = [];
  for (let i = minKey; i <= -0.5; i += 0.5) { 
    negIncrements.push(i.toFixed(1));
  }
  
  const posIncrements: string[] = [];
  for (let i = 0.5; i <= maxKey; i += 0.5) {
    posIncrements.push(i.toFixed(1));
  }

  // calculate negative values
  let negWinEntries = [0];
  let negLossEntries = [0];
  for (const negKey of negIncrements) {
    const record: Record<string, number> = bettingEntries[negKey] ?? EMPTY_RECORD;
    negWinEntries.push(negWinEntries[negWinEntries.length-1] + record[WIN]);
    negLossEntries.push(negLossEntries[negLossEntries.length-1] + record[LOSS]);
  }
  negWinEntries.shift();
  negLossEntries.shift();

  // calculate positive values
  let posWinEntries = [0];
  let posLossEntries = [0];
  for (const posKey of posIncrements.slice().reverse()) {
    const record: Record<string, number> = bettingEntries[posKey] ?? EMPTY_RECORD;
    posWinEntries.push(posWinEntries[posWinEntries.length-1] + record[WIN]);
    posLossEntries.push(posLossEntries[posLossEntries.length-1] + record[LOSS]);
  }
  posWinEntries.shift();
  posWinEntries.reverse();
  posLossEntries.shift();
  posLossEntries.reverse();

  const zeroWinData: number[] = [dictionary[OVERALL_MAP][WIN]]
  const zeroLossData: number[] = [dictionary[OVERALL_MAP][LOSS]]

  const winData = negWinEntries.concat(zeroWinData).concat(posWinEntries);
  const lossData = negLossEntries.concat(zeroLossData).concat(posLossEntries);
  const keyData = negIncrements.concat(["0"]).concat(posIncrements.map(val => "+" + val));
  
  const series = [
    { data: winData, stack: 'A', label: 'Wins', valueFormatter: (v: any, { dataIndex }: any) => {
      const wins = winData[dataIndex];
      const losses = lossData[dataIndex];
      if (wins === 0 && losses == 0){ return '0  -  (0%)';}
      const winPercentage = ((wins / (wins+losses)) * 100).toFixed(2) + '%';
      return `${wins}    (${winPercentage})`;
    } },
    { data: lossData, stack: 'A', label: 'Losses', valueFormatter: (v: any, { dataIndex }: any) => {
      return `${v}`; }},
  ];

  return (
    <div style={{
      background: 'white', 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      width: '80%', 
      height: '60vh',
      margin: '0 auto'
    }}>
      <BarChart
        series={series}
        xAxis={[
          {
            scaleType: 'band',
            data: keyData,
            label: 'Difference: Air Ball Line Prediction Minus Fanduel Game Line'
          },
        ]}
        yAxis={[{label: 'Predictions Made'}]}
        barLabel={(item, _) => {
          /*
          const { seriesId, dataIndex } = item;
          if (seriesId === WIN_ID_SERIES) {
            const wins = series[0].data[dataIndex];
            const losses = series[1].data[dataIndex];
            if (wins === 0 && losses == 0){ return '';}
            const winPercentage = ((wins / (wins+losses)) * 100).toFixed(2) + '%';
            return winPercentage;
          }
          */
          return null;
        }}
      />
    </div>
  );
};

SeasonStats.getLayout = function getLayout(page: ReactElement) {
  return <Layout>{page}</Layout>;
};

export default SeasonStats;
