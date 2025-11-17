import { useState } from 'react';
import './App.css'
import PressList from './components/PressList.jsx';
function App() {

  const [category, setCategory] = useState('All Ministry');
  const [language, setLanguage] = useState('English');
  const [day, setDay] = useState('');
  const [month, setMonth] = useState('');
  const [year, setYear] = useState('');

  const [tempCategory, setTempCategory] = useState('All Ministry');
  const [tempLanguage, setTempLanguage] = useState('English');
  const [tempDay, setTempDay] = useState('');
  const [tempMonth, setTempMonth] = useState('');
  const [tempYear, setTempYear] = useState('');

  const handleApply = () => {
    setCategory(tempCategory);
    setLanguage(tempLanguage);
    setDay(tempDay);
    setMonth(tempMonth);
    setYear(tempYear);
  };

  const handleClear = () => {
    setCategory('All Ministry'); setLanguage('English'); setDay(''); setMonth(''); setYear('');
    setTempCategory('All Ministry'); setTempLanguage('English'); setTempDay(''); setTempMonth(''); setTempYear('');
  };

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
          day={day}
          month={month}
          year={year}
        />
        <aside className='sidebar'>
          <div className='filter-panel'>
            <div className='filter-group'>
              <label className='filter-label'>Date</label>

              <div className='date-row'>
                <input
                  type='number'
                  placeholder='Date'
                  min='1'
                  max='31'
                  value={tempDay}
                  onChange={(e) => setTempDay(e.target.value)}
                  className='filter-input'
                />

                <select
                  value={tempMonth}
                  onChange={(e) => setTempMonth(e.target.value)}
                  className='filter-input'
                >
                  <option value=''>Mon</option>

                  <option value="January">Jan</option>
                  <option value="February">Feb</option>
                  <option value="March">Mar</option>
                  <option value="April">Apr</option>
                  <option value="May">May</option>
                  <option value="June">Jun</option>
                  <option value="July">Jul</option>
                  <option value="August">Aug</option>
                  <option value="September">Sep</option>
                  <option value="October">Oct</option>
                  <option value="November">Nov</option>
                  <option value="December">Dec</option>
                </select>


                <input
                  type='number'
                  placeholder='Year'
                  min='1950'
                  max='2050'
                  value={tempYear}
                  onChange={(e) => setTempYear(e.target.value)}
                  className='filter-input'
                />
              </div>

              <label className='filter-label'>Ministry</label>
              <select
                className='filter-input'
                value={tempCategory}
                onChange={(e) => setTempCategory(e.target.value)}
              >
                <option>All Ministry</option>
                <option>President's Secretariat</option>
                <option>Vice President's Secretariat</option>
                <option>Prime Minister's Office</option>

                <option>Lok Sabha Secretariat</option>
                <option>Rajya Sabha Secretariat</option>

                <option>Cabinet</option>
                <option>Cabinet Committee Decisions</option>
                <option>Cabinet Committee on Economic Affairs (CCEA)</option>
                <option>Cabinet Secretariat</option>
                <option>Cabinet Committee on Infrastructure</option>
                <option>Cabinet Committee on Price</option>
                <option>Cabinet Committee on Investment</option>
                <option>Other Cabinet Committees</option>

                <option>AYUSH</option>
                <option>Department of Space</option>
                <option>Department of Ocean Development</option>
                <option>Department of Atomic Energy</option>
                <option>Election Commission</option>
                <option>Finance Commission</option>

                <option>Ministry of Agriculture & Farmers Welfare</option>
                <option>Ministry of Agro & Rural Industries</option>
                <option>Ministry of Chemicals and Fertilizers</option>
                <option>Department of Pharmaceuticals</option>
                <option>Department of Fertilizers</option>
                <option>Department of Chemicals and Petrochemicals</option>

                <option>Ministry of Civil Aviation</option>
                <option>Ministry of Coal</option>
                <option>Ministry of Commerce & Industry</option>
                <option>Ministry of Communications</option>
                <option>Ministry of Company Affairs</option>
                <option>Ministry of Consumer Affairs, Food & Public Distribution</option>
                <option>Ministry of Cooperation</option>
                <option>Ministry of Corporate Affairs</option>
                <option>Ministry of Culture</option>
                <option>Ministry of Defence</option>
                <option>Ministry of Development of North-East Region</option>
                <option>Ministry of Disinvestment</option>
                <option>Ministry of Drinking Water & Sanitation</option>
                <option>Ministry of Earth Sciences</option>
                <option>Ministry of Education</option>
                <option>Ministry of Electronics & IT</option>
                <option>Ministry of Environment, Forest and Climate Change</option>
                <option>Ministry of External Affairs</option>
                <option>Ministry of Finance</option>
                <option>Ministry of Fisheries, Animal Husbandry & Dairying</option>
                <option>Ministry of Food Processing Industries</option>
                <option>Ministry of Health and Family Welfare</option>
                <option>Ministry of Heavy Industries</option>
                <option>Ministry of Home Affairs</option>
                <option>Ministry of Housing & Urban Affairs</option>
                <option>Ministry of Information & Broadcasting</option>
                <option>Ministry of Jal Shakti</option>
                <option>Ministry of Labour & Employment</option>
                <option>Ministry of Law and Justice</option>
                <option>Ministry of Micro,Small & Medium Enterprises</option>
                <option>Ministry of Mines</option>
                <option>Ministry of Minority Affairs</option>
                <option>Ministry of New and Renewable Energy</option>
                <option>Ministry of Overseas Indian Affairs</option>
                <option>Ministry of Panchayati Raj</option>
                <option>Ministry of Parliamentary Affairs</option>
                <option>Ministry of Personnel, Public Grievances & Pensions</option>
                <option>Ministry of Petroleum & Natural Gas</option>
                <option>Ministry of Planning</option>
                <option>Ministry of Power</option>
                <option>Ministry of Railways</option>
                <option>Ministry of Road Transport & Highways</option>
                <option>Ministry of Rural Development</option>
                <option>Ministry of Science & Technology</option>
                <option>Ministry of Ports, Shipping and Waterways</option>
                <option>Ministry of Skill Development and Entrepreneurship</option>
                <option>Ministry of Social Justice & Empowerment</option>
                <option>Ministry of Statistics & Programme Implementation</option>
                <option>Ministry of Steel</option>
                <option>Ministry of Surface Transport</option>
                <option>Ministry of Textiles</option>
                <option>Ministry of Tourism</option>
                <option>Ministry of Tribal Affairs</option>
                <option>Ministry of Urban Development</option>
                <option>Ministry of Water Resources, River Development and Ganga Rejuvenatior</option>
                <option>Ministry of Women and Child Development</option>
                <option>Ministry of Youth Affairs and Sports</option>
                <option>NITI Aayog</option>
                <option>PM Speech</option>
                <option>EAC-PM</option>
                <option>UPSC</option>
                <option>Special Service and Features</option>
                <option>PIB Headquarters</option>
                <option>Office of Principal Scientific Advisor to Gol</option>
                <option>National Financial Reporting Authority</option>
                <option>Competition Commission of India</option>
                <option>IFSC Authority</option>
                <option>National Security Council Secretariat</option>
                <option>National Human Rights Commission</option>
                <option>Lokpal of India</option>
                <option>home</option>
                <option>ministry of parliamentary affairs</option>
              </select>
              <label className='filter-label'>Language</label>
              <select className='filter-input'
                value={tempLanguage}
                onChange={(e) => setTempLanguage(e.target.value)}
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
                <button className='apply-btn' onClick={handleApply}>Apply</button>
                <button
                  className='clear-btn'
                  onClick={handleClear}
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
