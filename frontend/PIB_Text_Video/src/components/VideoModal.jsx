import React, { useEffect, useRef } from 'react';
import './VideoModal.css';
import { FaTimes } from 'react-icons/fa';


const cleanDateDisplay = (dateStr) => {
    if (!dateStr) return "";
    return dateStr.split(' by ')[0];
};

function VideoModal({ releaseData, videoSrc, onClose }) {

    const videoRef = useRef(null);

    useEffect(() => {
        document.body.style.overflow = 'hidden';

        if (videoRef.current) {
            videoRef.current.play().catch(error => {
                console.error("Autoplay was prevented by browser policy:", error);
            });
        }

        const handleKeyDown = (e) => {
            if (!videoRef.current) return;

            if (e.key === 'ArrowRight') {
                e.preventDefault();
                videoRef.current.currentTime += 5;
            }

            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                videoRef.current.currentTime -= 5;
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => {
            document.body.style.overflow = 'auto';
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, []);

    return (
        <div className='modal-overlay' onClick={onClose}>
            <div className='modal-content' onClick={(event) => event.stopPropagation()}>
                <button className='modal-close-btn' onClick={onClose}>
                    <FaTimes />
                </button>
                <video
                    ref={videoRef}
                    className='modal-video'
                    src={videoSrc}
                    controls
                    muted
                    playsInline
                    disablePictureInPicture />
                <div className="modal-info">
                    <h3 className="modal-title">{releaseData.title}</h3>
                    
                    <p className="modal-date" style={{ marginTop: '10px', color: '#555' }}>
                        {cleanDateDisplay(releaseData.release_date)}
                    </p>
                    
                </div>
            </div>
        </div>
    );
}

export default VideoModal;