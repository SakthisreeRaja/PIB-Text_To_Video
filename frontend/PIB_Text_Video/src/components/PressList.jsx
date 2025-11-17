import { useEffect, useState } from 'react';
import './PressList.css'
import SearchBar from './Searchbar.jsx';
import { FaRegPlayCircle } from 'react-icons/fa';
import ImageCarousel from './ImageCarousel.jsx';
import VideoModal from './VideoModal.jsx';

const SAMPLE_VIDEO_URL = "https://www.w3schools.com/html/mov_bbb.mp4";
const API_BASE_URL = "http://127.0.0.1:8000";

function PressList({ category, language, fromYear, toYear }) {
    const [pressReleases, setPressReleases] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


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
                setPressReleases(data);
                setLoading(false);
            } catch (err) {
                console.error("Erroe fetching data:", err);
                setError("Could not load press releases. Is the backend server running?");
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const filteredReleases = pressReleases.filter((release) => {
        const title = release.title || "";
        const releaseCategory = release.ministry_name || "General";
        const releaseYear = release.release_year || 0;

        const matchesSearch = title.toLowerCase().includes(SearchTerm.toLowerCase());
        const matchesCategory = (category === 'All') || (releaseCategory === category);

        const from = fromYear ? parseInt(fromYear) : 0;
        const to = toYear ? parseInt(toYear) : 9999;
        const matchesYear = releaseYear >= from && releaseYear <= to;

        return matchesSearch && matchesCategory && matchesYear;
    });

    const handleWatchVideo = (release) => {
        setPlayvideo(release);
    }

    const handleCloseModal = () => {
        setPlayvideo(null);
    }
    if (loading) return <div className="loading">Loading Press Releases...</div>;
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
                {filteredReleases.length > 0 ? (
                    filteredReleases.map((release) => (
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