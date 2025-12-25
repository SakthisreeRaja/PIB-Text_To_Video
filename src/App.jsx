import { useState, useEffect } from 'react';
import './App.css';
import PressList from './components/PressList.jsx';
import HighlightCarousel from './components/HighlightCarousel.jsx';
import { useTranslation } from 'react-i18next';

function App() {
  const { t, i18n } = useTranslation();
  const [category, setCategory] = useState('All Ministry');
  const [language, setLanguage] = useState(i18n.resolvedLanguage || 'en');
  const [day, setDay] = useState('');
  const [month, setMonth] = useState('');
  const [year, setYear] = useState('');
  const [tempCategory, setTempCategory] = useState('All Ministry');
  const [tempLanguage, setTempLanguage] = useState(i18n.resolvedLanguage || 'en');
  const [tempDay, setTempDay] = useState('');
  const [tempMonth, setTempMonth] = useState('');
  const [tempYear, setTempYear] = useState('');
  const [allReleases, setAllReleases] = useState([]);
  const [highlightItems, setHighlightItems] = useState([]);
  const handleSortedData = (sortedList) => {
    setAllReleases(sortedList);
  };
  useEffect(() => {
    if (Array.isArray(allReleases) && allReleases.length > 0) {
      const top10 = allReleases.slice(0, 10).map(item => {
        if (!language || language === 'en') {
          return item.title;
        }

        const key = `title_${language}`;
        return item[key] || item.title;
      });

      setHighlightItems(top10);
    }
  }, [allReleases, language]);

  const handleApply = () => {
    setCategory(tempCategory);
    setLanguage(tempLanguage);
    setDay(tempDay);
    setMonth(tempMonth);
    setYear(tempYear);
    i18n.changeLanguage(tempLanguage);
  };

  const handleClear = () => {
    setCategory('All Ministry');
    setDay('');
    setMonth('');
    setYear('');

    setTempCategory('All Ministry');
    setTempDay('');
    setTempMonth('');
    setTempYear('');
  };

  return (
    <div>
      <div className='header'>
        <img src="/header.png" id='leftimg' alt="header" />

        <div className="titles">
          <h1 id='title'>{t('app_title')}</h1>
          <h2 id='title2'>{t('subtitle')}</h2>
        </div>

        <a href='https://www.pib.gov.in/indexd.aspx' target="_blank" rel="noreferrer">
          <img src="/pib.jpg" id='rightimg' alt="pib-logo" />
        </a>
      </div>

      <div className="desktop-only">
        Please open this website on a laptop or desktop for the best experience.
      </div>


      <div className='page-layout'>
        <PressList
          category={category}
          language={language}
          day={day}
          month={month}
          year={year}
          onSortedData={handleSortedData}
        />

        <aside className='sidebar'>
          <div className='filter-panel'>
            <div className='filter-group'>
              <label className='filter-label'>{t('date_label')}</label>

              <div className='date-row'>
                <input
                  type='number'
                  placeholder={t('date_placeholder')}
                  value={tempDay}
                  onChange={(e) => setTempDay(e.target.value)}
                  className='filter-input'
                />

                <select
                  value={tempMonth}
                  onChange={(e) => setTempMonth(e.target.value)}
                  className='filter-input'
                >
                  <option value=''>{t('month_placeholder')}</option>
                  <option value="January">{t('month_jan')}</option>
                  <option value="February">{t('month_feb')}</option>
                  <option value="March">{t('month_mar')}</option>
                  <option value="April">{t('month_apr')}</option>
                  <option value="May">{t('month_may')}</option>
                  <option value="June">{t('month_jun')}</option>
                  <option value="July">{t('month_jul')}</option>
                  <option value="August">{t('month_aug')}</option>
                  <option value="September">{t('month_sep')}</option>
                  <option value="October">{t('month_oct')}</option>
                  <option value="November">{t('month_nov')}</option>
                  <option value="December">{t('month_dec')}</option>
                </select>

                <input
                  type='number'
                  placeholder={t('year_placeholder')}
                  value={tempYear}
                  onChange={(e) => setTempYear(e.target.value)}
                  className='filter-input'
                />
              </div>

              <label className='filter-label'>{t('ministry_label')}</label>

              <select
                className='filter-input'
                value={tempCategory}
                onChange={(e) => setTempCategory(e.target.value)}
              >
                <option value="All Ministry">{t('all_ministry')}</option>
                <option value="President's Secretariat">{t('min_president_sec')}</option>
                <option value="Vice President's Secretariat">{t('min_vp_sec')}</option>
                <option value="Prime Minister's Office">{t('min_pm_office')}</option>
                <option value="Lok Sabha Secretariat">{t('min_lok_sabha')}</option>
                <option value="Rajya Sabha Secretariat">{t('min_rajya_sabha')}</option>
                <option value="Cabinet">{t('min_cabinet')}</option>
                <option value="Cabinet Committee Decisions">{t('min_cabinet_decisions')}</option>
                <option value="Cabinet Committee on Economic Affairs (CCEA)">{t('min_ccea')}</option>
                <option value="Cabinet Secretariat">{t('min_cabinet_sec')}</option>
                <option value="Cabinet Committee on Infrastructure">{t('min_cabinet_infra')}</option>
                <option value="Cabinet Committee on Price">{t('min_cabinet_price')}</option>
                <option value="Cabinet Committee on Investment">{t('min_cabinet_invest')}</option>
                <option value="AYUSH">{t('min_ayush')}</option>
                <option value="Other Cabinet Committees">{t('min_other_cabinet')}</option>
                <option value="Department of Space">{t('min_space')}</option>
                <option value="Department of Ocean Development">{t('min_ocean')}</option>
                <option value="Department of Atomic Energy">{t('min_atomic')}</option>
                <option value="Election Commission">{t('min_election')}</option>
                <option value="Finance Commission">{t('min_finance_comm')}</option>
                <option value="Ministry of Agriculture & Farmers Welfare">{t('min_agriculture')}</option>
                <option value="Ministry of Agro & Rural Industries">{t('min_agro')}</option>
                <option value="Ministry of Chemicals and Fertilizers">{t('min_chemicals')}</option>
                <option value="Department of Pharmaceuticals">{t('min_pharma')}</option>
                <option value="Department of Fertilizers">{t('min_fertilizers')}</option>
                <option value="Department of Chemicals and Petrochemicals">{t('min_petrochem')}</option>
                <option value="Ministry of Civil Aviation">{t('min_aviation')}</option>
                <option value="Ministry of Coal">{t('min_coal')}</option>
                <option value="Ministry of Commerce & Industry">{t('min_commerce')}</option>
                <option value="Ministry of Communications">{t('min_comms')}</option>
                <option value="Ministry of Company Affairs">{t('min_company')}</option>
                <option value="Ministry of Consumer Affairs, Food & Public Distribution">{t('min_consumer')}</option>
                <option value="Ministry of Cooperation">{t('min_cooperation')}</option>
                <option value="Ministry of Corporate Affairs">{t('min_corporate')}</option>
                <option value="Ministry of Culture">{t('min_culture')}</option>
                <option value="Ministry of Defence">{t('min_defence')}</option>
                <option value="Ministry of Development of North-East Region">{t('min_doner')}</option>
                <option value="Ministry of Disinvestment">{t('min_disinvest')}</option>
                <option value="Ministry of Drinking Water & Sanitation">{t('min_drinking')}</option>
                <option value="Ministry of Earth Sciences">{t('min_earth')}</option>
                <option value="Ministry of Education">{t('min_education')}</option>
                <option value="Ministry of Electronics & IT">{t('min_electronics')}</option>
                <option value="Ministry of Environment, Forest and Climate Change">{t('min_environment')}</option>
                <option value="Ministry of External Affairs">{t('min_external')}</option>
                <option value="Ministry of Finance">{t('min_finance')}</option>
                <option value="Ministry of Fisheries, Animal Husbandry & Dairying">{t('min_fisheries')}</option>
                <option value="Ministry of Food Processing Industries">{t('min_food_process')}</option>
                <option value="Ministry of Health and Family Welfare">{t('min_health')}</option>
                <option value="Ministry of Heavy Industries">{t('min_heavy_ind')}</option>
                <option value="Ministry of Home Affairs">{t('min_home')}</option>
                <option value="Ministry of Housing & Urban Affairs">{t('min_housing')}</option>
                <option value="Ministry of Information & Broadcasting">{t('min_ib')}</option>
                <option value="Ministry of Jal Shakti">{t('min_jal_shakti')}</option>
                <option value="Ministry of Labour & Employment">{t('min_labour')}</option>
                <option value="Ministry of Law and Justice">{t('min_law')}</option>
                <option value="Ministry of Micro,Small & Medium Enterprises">{t('min_msme')}</option>
                <option value="Ministry of Mines">{t('min_mines')}</option>
                <option value="Ministry of Minority Affairs">{t('min_minority')}</option>
                <option value="Ministry of New and Renewable Energy">{t('min_new_renewable')}</option>
                <option value="Ministry of Overseas Indian Affairs">{t('min_overseas')}</option>
                <option value="Ministry of Panchayati Raj">{t('min_panchayati')}</option>
                <option value="Ministry of Parliamentary Affairs">{t('min_parliament')}</option>
                <option value="Ministry of Personnel, Public Grievances & Pensions">{t('min_personnel')}</option>
                <option value="Ministry of Petroleum & Natural Gas">{t('min_petroleum')}</option>
                <option value="Ministry of Planning">{t('min_planning')}</option>
                <option value="Ministry of Power">{t('min_power')}</option>
                <option value="Ministry of Railways">{t('min_railways')}</option>
                <option value="Ministry of Road Transport & Highways">{t('min_road')}</option>
                <option value="Ministry of Rural Development">{t('min_rural')}</option>
                <option value="Ministry of Science & Technology">{t('min_science')}</option>
                <option value="Ministry of Ports, Shipping and Waterways">{t('min_shipping')}</option>
                <option value="Ministry of Skill Development and Entrepreneurship">{t('min_skill')}</option>
                <option value="Ministry of Social Justice & Empowerment">{t('min_social')}</option>
                <option value="Ministry of Statistics & Programme Implementation">{t('min_stats')}</option>
                <option value="Ministry of Steel">{t('min_steel')}</option>
                <option value="Ministry of Surface Transport">{t('min_surface')}</option>
                <option value="Ministry of Textiles">{t('min_textiles')}</option>
                <option value="Ministry of Tourism">{t('min_tourism')}</option>
                <option value="Ministry of Tribal Affairs">{t('min_tribal')}</option>
                <option value="Ministry of Urban Development">{t('min_urban')}</option>
                <option value="Ministry of Water Resources, River Development and Ganga Rejuvenation">{t('min_water')}</option>
                <option value="Ministry of Women and Child Development">{t('min_women')}</option>
                <option value="Ministry of Youth Affairs and Sports">{t('min_youth')}</option>
                <option value="NITI Aayog">{t('min_niti')}</option>
                <option value="PM Speech">{t('min_pm_speech')}</option>
                <option value="EAC-PM">{t('min_eac_pm')}</option>
                <option value="UPSC">{t('min_upsc')}</option>
                <option value="Special Service and Features">{t('min_special')}</option>
                <option value="PIB Headquarters">{t('min_pib_hq')}</option>
                <option value="Office of Principal Scientific Advisor to Gol">{t('min_psa')}</option>
                <option value="National Financial Reporting Authority">{t('min_nfra')}</option>
                <option value="Competition Commission of India">{t('min_cci')}</option>
                <option value="IFSC Authority">{t('min_ifsc')}</option>
                <option value="National Security Council Secretariat">{t('min_nscs')}</option>
                <option value="National Human Rights Commission">{t('min_nhrc')}</option>
                <option value="Lokpal of India">{t('min_lokpal')}</option>
                <option value="home">{t('home')}</option>
                <option value="ministry of parliamentary affairs">{t('ministry_of_parliamentary_affairs')}</option>
              </select>

              <label className='filter-label'>{t('language_label')}</label>

              <select
                className='filter-input'
                value={tempLanguage}
                onChange={(e) => setTempLanguage(e.target.value)}
              >
                <option value="en">English</option>
                <option value="hi">Hindi (हिंदी)</option>
                <option value="ur">Urdu (اردو)</option>
                <option value="pa">Punjabi (ਪੰਜਾਬੀ)</option>
                <option value="gu">Gujarati (ગુજરાતી)</option>
                <option value="mr">Marathi (मराठी)</option>
                <option value="te">Telugu (తెలుగు)</option>
                <option value="kn">Kannada (कन्नड़)</option>
                <option value="ml">Malayalam (मलयालम)</option>
                <option value="ta">Tamil (தமிழ்)</option>
                <option value="or">Odia (ओडिया)</option>
                <option value="bn">Bengali (बंगाली)</option>
                <option value="as">Assamese (असमिया)</option>
                <option value="mni">Manipuri (मणिपुरी)</option>
              </select>

              <div className='filter-buttons'>
                <button className='apply-btn' onClick={handleApply}>{t('apply_btn')}</button>
                <button className='clear-btn' onClick={handleClear}>{t('clear_btn')}</button>
              </div>
            </div>
          </div>
          <HighlightCarousel items={highlightItems} />
        </aside>
      </div>

      <footer className='footer'>
        <p>{t('footer_text')}</p>
      </footer>
    </div>
  );
}

export default App;