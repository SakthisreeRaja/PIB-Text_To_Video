import { useState } from 'react';
import './App.css'
import PressList from './components/PressList.jsx';
function App() {

  const [category, setCategory] = useState('All');
  const [language, setLanguage] = useState('English');
  const [fromYear, setFromYear] = useState('');
  const [toYear, setToYear] = useState('');

  return (
    <div>
      <div className='header'>
        < img src="/emblem.png" alt="Emblem" id='leftimg' />
        <div className="titles">
          <h1 id='title'>Press Information Bureau</h1>
          <h2 id='title2'>Info to video</h2></div>
        <a
          href='https://www.pib.gov.in/indexd.aspx'
          target="_blank"
          rel="noopener noreferrer"
        >
          <img src="/pib.jpg" alt="PIB logo" id='rightimg' />
        </a>
      </div>
      <div className='page-layout'>
        <PressList
          category={category}
          language={language}
          fromYear={fromYear}
          toYear={toYear} />
        <aside className='sidebar'>
          <div className='filter-panel'>
            <div className='filter-group'>
              <label className='filter-label'>Year Range</label>
              <div className='year-inputs'>
                <input
                  type='number'
                  placeholder='From'
                  className='filter-input'
                  min='1950'
                  max='2050'
                  value={fromYear}
                  onChange={(e) => setFromYear(e.target.value)}
                />
                <span className='to-text'>to</span>
                <input
                  type='number'
                  placeholder='To'
                  className='filter-input'
                  min='1950'
                  max='2050'
                  value={toYear}
                  onChange={(e) => setToYear(e.target.value)}
                />
              </div>
              <label className='filter-label'>Category</label>
              <select
                className='filter-input'
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                <option>All</option>
                <option>Agriculture</option>
                <option>Technology</option>
                <option>Governance</option>
                <option>Defence</option>
                <option>Environment</option>
                <option>Science</option>
                <option value="President's Secretariat">President's Secretariat</option>
                <option value="Prime Minister's Office">Prime Minister's Office</option>
              </select>
              <label className='filter-label'>Language</label>
              <select className='filter-input'
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                >
                <option>English</option>
                <option>Hindi</option>
                <option>Urdu</option>
                <option>Punjabi</option>
                <option>Gujarati</option>
                <option>Marathi</option>
                <option>Telugu</option>
                <option>Kannada</option>
                <option>Malayalam</option>
                <option>Tamil</option>
                <option>Odia</option>
                <option>Bengali</option>
                <option>Assamese</option>
                <option>Manipuri</option>
              </select>
              <div className='filter-buttons'>
                <button className='apply-btn'>Apply</button>
                <button
                  className='clear-btn'
                  onClick={() => {
                    setCategory('All');
                    setLanguage('English');
                    setFromYear('');
                    setToYear('');
                  }}
                >
                  Clear
                </button>
              </div>
            </div>
          </div>
          <section className='highlights'>
            <h3>Quick Highlights</h3>
            <ul>
              <li>Latest AI mission launched by Govt of India</li>
              <li>PM addressed the Global Science Congress</li>
              <li>Agriculture growth report indicates 6% rise</li>
            </ul>
          </section>
        </aside>
      </div>
      <footer className='footer'>
        <p>&copy;  Press Information Bureau | Ministry of Information and Broadcasting, Government of India.</p>
      </footer>
    </div>
  )
}

export default App
