import { useState } from 'react';
import './PressList.css'
import SearchBar from './Searchbar.jsx';
import { FaRegPlayCircle } from 'react-icons/fa';

function PressList() {
    const pressReleases = [
        { id: 1, title: 'PM addresses Global Science Congress', date: '01 Nov 2025' },
        { id: 2, title: 'Government launches new AI Mission', date: '31 Oct 2025' },
        { id: 3, title: 'Agriculture sector growth report released', date: '29 Oct 2025' },
        { id: 4, title: 'Digital India achieves new milestone', date: '27 Oct 2025' },
    ];

    const [SearchTerm, setSearchTerm] = useState('');
    const filteredReleases = pressReleases.filter((release) =>
        release.title.toLowerCase().includes(SearchTerm.toLowerCase())
    );

    return (
        <section className='press-list'>
            <div className='press-header'>
                <h2 className='press-title'>PIB Press Release</h2>
                <SearchBar setSearchTerm={setSearchTerm} />
            </div>
            <div className='cards'>
                {filteredReleases.length > 0 ? (
                    filteredReleases.map((release) => (
                        <div key={release.id} className="card">
                            <h3>{release.title}</h3>
                            <p>{release.date}</p>
                            <button className='video-btn'>
                                <FaRegPlayCircle className='video-icon' />
                                Watch
                            </button>
                        </div>
                    ))
                ) : (
                    <div className='no-results'><p>No press release found.</p></div>
                )}
            </div>
        </section>
    );


}

export default PressList;