import { useEffect, useState } from 'react';
import './PressList.css'
import SearchBar from './Searchbar.jsx';
import { FaRegPlayCircle, FaChevronLeft, FaChevronRight } from 'react-icons/fa';
import ImageCarousel from './ImageCarousel.jsx';
import VideoModal from './VideoModal.jsx';

const SAMPLE_VIDEO_URL = "https://www.w3schools.com/html/mov_bbb.mp4";
const API_BASE_URL = "http://127.0.0.1:8000";
const ITEMS_PER_PAGE = 9;

function PressList({ category, language, day, month, year }) {
    const [pressReleases, setPressReleases] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [currentPage, setCurrentPage] = useState(1);
    const [SearchTerm, setSearchTerm] = useState('');
    const [playvideo, setPlayvideo] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/releases`);
                if (!response.ok) {
                    throw new Error(`Failed to connect to the backend API`);
                }
                const data = await response.json();
                if (Array.isArray(data)) {
                    setPressReleases(data);
                } else {
                    console.error("Backend Error:", data);
                    setError(data.error || "Invalid data received.");
                }
                setLoading(false);
            } catch (err) {
                console.error("Error fetching data:", err);
                setError("Could not load press releases. Is the backend server running?");
                setLoading(false);
            }
        };

        fetchData();
    }, []); 

    const monthMap = {
        "January": "JAN", "February": "FEB", "March": "MAR", "April": "APR",
        "May": "MAY", "June": "JUN", "July": "JUL", "August": "AUG",
        "September": "SEP", "October": "OCT", "November": "NOV", "December": "DEC"
    };

    const filteredReleases = Array.isArray(pressReleases) ? pressReleases.filter((release) => {
        const matchesCategory = (category === 'All Ministry') || (release.ministry_name === category);

        const dateParts = release.release_date ? release.release_date.split(" ") : [];
        const releaseDay = dateParts.length > 0 ? parseInt(dateParts[0]) : null;
        const releaseMonth = dateParts.length > 1 ? dateParts[1].toUpperCase() : "";
        const releaseYear = release.release_year;

        const matchesDay = !day || (releaseDay === parseInt(day));
        const matchesMonth = !month || (releaseMonth === monthMap[month]);
        const matchesYear = !year || (releaseYear === parseInt(year));

        const title = release.title || "";
        const matchesSearch = title.toLowerCase().includes(SearchTerm.toLowerCase());

        return matchesCategory && matchesDay && matchesMonth && matchesYear && matchesSearch;
    }) : [];

    const sortedReleases = filteredReleases.sort((a, b) => {
        return new Date(b.release_date) - new Date(a.release_date);
    });

    useEffect(() => {
        setCurrentPage(1);
    }, [category, language, day, month, year, SearchTerm]);

    const indexOfLastItem = currentPage * ITEMS_PER_PAGE;
    const indexOfFirstItem = indexOfLastItem - ITEMS_PER_PAGE;

    const currentItems = sortedReleases.slice(indexOfFirstItem, indexOfLastItem);
    const totalPages = Math.ceil(sortedReleases.length / ITEMS_PER_PAGE);

    const handleWatchVideo = (release) => {
        setPlayvideo(release);
    }

    const handleCloseModal = () => {
        setPlayvideo(null);
    }

    const paginate = (pageNumber) => {
        setCurrentPage(pageNumber);
        window.scrollTo({ top: 400, behavior: 'smooth' });
    };

    if (loading) {
        return (
            <div className="loading-container">
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Loading Press Releases...</p>
                </div>
            </div>
        );
    }

    if (error) return <div className="error-message">{error}</div>;

    return (
        <section className='press-list'>
            <div className='press-header'>
                <h2 className='press-title'>PIB Press Release</h2>
            </div>
            <ImageCarousel />
            <div className='cards-header'>
                <h3 className='cards-title'>Latest Releases</h3>
                <SearchBar setSearchTerm={setSearchTerm} />
            </div>
            <div className='cards'>
                {currentItems.length > 0 ? (
                    currentItems.map((release) => (
                        <div key={release.id} className="card">
                            <h3>{release.title}</h3>
                            <p>{release.release_date}</p>
                            <button className='video-btn' onClick={() => handleWatchVideo(release)}>
                                <FaRegPlayCircle className='video-icon' />
                                Watch
                            </button>
                        </div>
                    ))
                ) : (
                    <div className='no-results'><p>No press release found.</p></div>
                )}
            </div>
            {sortedReleases.length > ITEMS_PER_PAGE && (
                <div className="pagination">
                    <button
                        onClick={() => paginate(currentPage - 1)}
                        disabled={currentPage === 1}
                        className="page-btn"
                    >
                        <FaChevronLeft /> Prev
                    </button>

                    <span className="page-info">
                        Page {currentPage} of {totalPages}
                    </span>

                    <button
                        onClick={() => paginate(currentPage + 1)}
                        disabled={currentPage === totalPages}
                        className="page-btn"
                    >
                        Next <FaChevronRight />
                    </button>
                </div>
            )}
            {playvideo && (
                <VideoModal
                    releaseData={playvideo}
                    videoSrc={SAMPLE_VIDEO_URL}
                    onClose={handleCloseModal}
                />
            )}
        </section>
    );
}

export default PressList;