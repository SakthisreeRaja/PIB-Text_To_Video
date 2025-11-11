import { useState } from 'react';
import './PressList.css'
import SearchBar from './Searchbar.jsx';
import { FaRegPlayCircle } from 'react-icons/fa';
import ImageCarousel from './ImageCarousel.jsx';
import VideoModal from './VideoModal.jsx';

const SAMPLE_VIDEO_URL = "https://www.w3schools.com/html/mov_bbb.mp4";

function PressList() {
    const pressReleases = [
        { id: 1, title: 'PM addresses Global Science Congress', date: '01 Nov 2025' },
        { id: 2, title: 'Government launches new AI Mission', date: '31 Oct 2025' },
        { id: 3, title: 'Agriculture sector growth report released', date: '29 Oct 2025' },
        { id: 4, title: 'Digital India achieves new milestone', date: '27 Oct 2025' },
    ];

    const [SearchTerm, setSearchTerm] = useState('');

    const [playvideo, setPlayvideo] = useState(null);

    const filteredReleases = pressReleases.filter((release) =>
        release.title.toLowerCase().includes(SearchTerm.toLowerCase())
    );

    const handleWatchVideo = (release) => {
        setPlayvideo(release);
    }

    const handleCloseModal = () => {
        setPlayvideo(null);
    }

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
                            <p>{release.date}</p>
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