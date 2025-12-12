import { useEffect, useState } from 'react';
import './PressList.css';
import SearchBar from './Searchbar.jsx';
import { FaRegPlayCircle, FaChevronLeft, FaChevronRight, FaSpinner } from 'react-icons/fa';
import ImageCarousel from './ImageCarousel.jsx';
import VideoModal from './VideoModal.jsx';
import AlertModal from './AlertModal.jsx';
import { useTranslation } from 'react-i18next';

const API_BASE_URL = ""; 
const ITEMS_PER_PAGE = 9;

function parseDate(d) {
  if (!d) return 0;
  const clean = d.split(" by ")[0].trim().split(" ");
  const day = parseInt(clean[0]) || 1;
  const mon = (clean[1] || "JAN").toUpperCase();
  const monthMapShort = { JAN: 0, FEB: 1, MAR: 2, APR: 3, MAY: 4, JUN: 5, JUL: 6, AUG: 7, SEP: 8, OCT: 9, NOV: 10, DEC: 11 };
  const month = monthMapShort[mon] ?? 0;
  const year = parseInt(clean[2]) || 1970;
  const timeStr = clean[3] || "12:00AM";
  const isPM = /PM/i.test(timeStr);
  const timeOnly = timeStr.replace(/AM|PM/i, "");
  const [hStr = "12", mStr = "00"] = timeOnly.split(":");
  let h = parseInt(hStr) || 0;
  const m = parseInt(mStr) || 0;
  if (isPM && h !== 12) h += 12;
  if (!isPM && h === 12) h = 0;
  return new Date(year, month, day, h, m).getTime();
}

const cleanDateDisplay = (dateStr) => {
  if (!dateStr) return "";
  return dateStr.split(' by ')[0];
};

function PressList({ category, language, day, month, year, onSortedData }) {
  const { t } = useTranslation();

  const [pressReleases, setPressReleases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [SearchTerm, setSearchTerm] = useState('');
  const [playvideo, setPlayvideo] = useState(null);
  const [fetchingId, setFetchingId] = useState(null);
  const [showAlert, setShowAlert] = useState(false); 

  const getContent = (item) => {
    if (!language || language === 'en') {
      return { title: item.title }; 
    }
    const titleKey = `title_${language}`;
    return {
      title: item[titleKey] || item.title,
    };
  };
  useEffect(() => {
    let cancelled = false;
    const fetchData = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/releases`);
        const data = await res.json();
        const arr = Array.isArray(data) ? data : [];

        const globallySorted = [...arr].sort((a, b) => parseDate(b.release_date) - parseDate(a.release_date));

        if (!cancelled) {
          if (typeof onSortedData === "function") onSortedData(globallySorted);
          setPressReleases(globallySorted);
          setLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(t('error_load_releases'));
          setLoading(false);
        }
      }
    };
    fetchData();
    return () => { cancelled = true; };
  }, []);

  const handleWatchClick = async (releaseId) => {
    setFetchingId(releaseId); 
    try {
      const res = await fetch(`${API_BASE_URL}/api/releases/${releaseId}`);
      if (!res.ok) throw new Error("Failed to fetch details");
      
      const fullData = await res.json();
      const videoLinks = fullData.video_links || {};
      const currentLang = language || 'en';
      const videoUrl = videoLinks[currentLang];
      
      if (!videoUrl) {
        setShowAlert(true);
        return;
      }
      setPlayvideo({
        ...fullData,
        video_url: videoUrl
      }); 
    } catch (err) {
      console.error(err);
      alert("Could not load video. Please try again later.");
    } finally {
      setFetchingId(null); 
    }
  };

  const monthMap = {
    January: "JAN", February: "FEB", March: "MAR", April: "APR",
    May: "MAY", June: "JUN", July: "JUL", August: "AUG",
    September: "SEP", October: "OCT", November: "NOV", December: "DEC"
  };

  const filteredReleases = Array.isArray(pressReleases)
    ? pressReleases.filter((release) => {
      const { title: displayTitle } = getContent(release);

      const matchesCategory = category === 'All Ministry' || release.ministry_name === category;
      const parts = (release.release_date || "").split(" ");
      const releaseDay = parseInt(parts[0]) || null;
      const releaseMonth = (parts[1] || "").toUpperCase();
      const releaseYear = release.release_year;
      const matchesDay = !day || releaseDay === parseInt(day);
      const matchesMonth = !month || releaseMonth === monthMap[month];
      const matchesYear = !year || releaseYear === parseInt(year);
      const matchesSearch = (displayTitle || "").toLowerCase().includes(SearchTerm.toLowerCase());

      return matchesCategory && matchesDay && matchesMonth && matchesYear && matchesSearch;
    })
    : [];

  const sortedReleases = [...filteredReleases].sort((a, b) => parseDate(b.release_date) - parseDate(a.release_date));

  useEffect(() => { setCurrentPage(1); }, [category, language, day, month, year, SearchTerm]);

  const indexOfLastItem = currentPage * ITEMS_PER_PAGE;
  const indexOfFirstItem = indexOfLastItem - ITEMS_PER_PAGE;
  const currentItems = sortedReleases.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.max(1, Math.ceil(sortedReleases.length / ITEMS_PER_PAGE));

  const paginate = (pageNumber) => {
    if (pageNumber < 1 || pageNumber > totalPages) return;
    setCurrentPage(pageNumber);
    window.scrollTo({ top: 400, behavior: 'smooth' });
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>{t('loading')}</p>
        </div>
      </div>
    );
  }

  if (error) return <div className="error-message">{t('error_load_releases')}</div>;

  return (
    <section className='press-list'>
      <div className='press-header'>
        <h2 className='press-title'>{t('app_title')}</h2>
      </div>

      <ImageCarousel />

      <div className='cards-header'>
        <h3 className='cards-title'>{t('latest_releases')}</h3>
        <SearchBar setSearchTerm={setSearchTerm} />
      </div>

      <div className='cards'>
        {currentItems.length > 0 ? (
          currentItems.map((release) => {
            const { title } = getContent(release);
            const isFetching = fetchingId === release.id;

            return (
              <div key={release.id} className="card">
                <h3>{title}</h3>

                <p>{cleanDateDisplay(release.release_date)}</p>

                <button 
                    className='video-btn' 
                    onClick={() => handleWatchClick(release.id)}
                    disabled={isFetching}
                    style={{ opacity: isFetching ? 0.7 : 1, cursor: isFetching ? 'wait' : 'pointer' }}
                >
                  {isFetching ? (
                     <FaSpinner className='video-icon fa-spin' style={{ animation: 'spin 1s linear infinite' }} />
                  ) : (
                     <FaRegPlayCircle className='video-icon' />
                  )}
                  <span style={{ marginLeft: '8px' }}>
                    {isFetching ? t('card_loading') : t('watch_btn')}
                  </span>
                </button>
              </div>
            );
          })
        ) : (
          <div className='no-results'>
            <p>{t('no_results')}</p>
          </div>
        )}
      </div>

      {sortedReleases.length > ITEMS_PER_PAGE && (
        <div className="pagination">
          <button onClick={() => paginate(currentPage - 1)} disabled={currentPage === 1} className="page-btn">
            <FaChevronLeft /> {t('prev_btn')}
          </button>

          <span className="page-info">
            {t('page_info', { current: currentPage, total: totalPages })}
          </span>

          <button onClick={() => paginate(currentPage + 1)} disabled={currentPage === totalPages} className="page-btn">
            {t('next_btn')} <FaChevronRight />
          </button>
        </div>
      )}

      {playvideo && (
        <VideoModal 
          releaseData={playvideo}
          videoSrc={playvideo.video_url}
          onClose={() => setPlayvideo(null)}
          language={language}
        />
      )}

      {showAlert && (
        <AlertModal 
          message={t('video_not_available')}
          onClose={() => setShowAlert(false)}
        />
      )}
    </section>
  );
}

export const getTopHighlights = (sortedReleases) => {
  if (!Array.isArray(sortedReleases)) return [];
  return sortedReleases.slice(0, 10).map(item => item.title);
};

export default PressList;