import { useEffect, useState } from "react";
import "./HighlightCarousel.css";
import { useTranslation } from 'react-i18next';

function HighlightCarousel({ items = [] }) {
  const { t } = useTranslation();
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (items.length === 0) return;

    const timer = setInterval(() => {
      setIndex(prev => (prev + 1) % items.length);
    }, 6000);

    return () => clearInterval(timer);
  }, [items.length]);

  return (
    <div className="highlight-box">
      <h3 className="highlight-title">{t('quick_highlights')}</h3>

      <div className="highlight-slide">
        <p key={index} className="highlight-text">{items[index]}</p>
      </div>

      <div className="highlight-dots">
        {items.map((_, i) => (
          <span
            key={i}
            className={`dot ${i === index ? "active" : ""}`}
            onClick={() => setIndex(i)}
          ></span>
        ))}
      </div>
    </div>
  );
}

export default HighlightCarousel;