import type { ReactElement } from 'react'
import Layout from '../components/layout'
import type { NextPageWithLayout } from './_app'
 
const About: NextPageWithLayout = () => {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Project Air-Ball</h1>
      <p>Helping the little guy by profiting off the underdogs covering against the giants</p>
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