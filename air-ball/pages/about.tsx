import type { ReactElement } from 'react'
import Layout from '../components/layout'
import type { NextPageWithLayout } from './_app'
import '../styles/about.css';
 
const About: NextPageWithLayout = () => {
  return (
    <div className='about'>
      <h1>Project Air-Ball</h1>
      <p>Helping the little guy by profiting off the underdogs covering against the giants</p>
      <p>Project Air Ball is a machine learning model, seasonal data aggregation,
        and frontend built using data from the NBA API -- see our public GitHubs</p>
      <a href="https://github.com/birdman093/air-ball" target="_blank" rel="noopener noreferrer" 
      style={{ display: 'block', margin: '10px 0', color: "var(--text-color)" }}>
        Frontend, and Backend
      </a>
      <a href="https://github.com/yourusername/your-repo2" target="_blank" rel="noopener noreferrer" 
      style={{ display: 'block', margin: '10px 0', color: "var(--text-color)" }}>
        ML Modeling
      </a>
    </div>
  )
}
 
About.getLayout = function getLayout(page: ReactElement) {
  return (
    <Layout>
      {page}
    </Layout>
  )
}
 
export default About