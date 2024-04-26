import type { ReactElement } from 'react'
import Layout from '../components/layout'
import type { NextPageWithLayout } from './_app'
import '../styles/about.css';
 
const About: NextPageWithLayout = () => {
  return (
    <div className='about'>
      <h1>Project Air-Ball</h1>
      <p>Project Air-Ball predicts the lines and has an estimated 60% success rate when the 
        point differential is 10 or more points. Daily picks are denoted as follows
        <ul>
          <li>{'On Fire - circled in red with one full airball (=< 10)'}</li>
          <li>{'Heating Up - circled in orange with one half airball (=< 7)'}</li>
          <li>{'Warming Up - circled in yellow (=< 5)'}</li>
        </ul> 
      </p>
      <p>The first iteration of this model has shown a strong preference to betting on
        the underdog to cover against a better team. </p>
      <p>For information on the machine learning model, seasonal data aggregation,
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