import React from 'react';
import './AlertModal.css';
import { FaExclamationCircle, FaTimes } from 'react-icons/fa';

function AlertModal({ message, onClose }) {
  return (
    <div className='alert-modal-overlay' onClick={onClose}>
      <div className='alert-modal-content' onClick={(e) => e.stopPropagation()}>
        <button className='alert-modal-close' onClick={onClose}>
          <FaTimes />
        </button>
        <div className='alert-modal-icon'>
          <FaExclamationCircle />
        </div>
        <p className='alert-modal-message'>{message}</p>
        <button className='alert-modal-btn' onClick={onClose}>
          OK
        </button>
      </div>
    </div>
  );
}

export default AlertModal;
