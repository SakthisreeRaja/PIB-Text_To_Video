import React from 'react'
import useEmblaCarousel from 'embla-carousel-react'
import Autoplay from 'embla-carousel-autoplay'
import './ImageCarousel.css'

export function ImageCarousel() {

  const [emblaRef] = useEmblaCarousel({ loop: true }, [Autoplay({ delay: 3000, stopOnInteraction: false })])

  const photos = [
    { src: "/photos/pm-temp-1.jpg", alt: "PM Photo 1" },
    { src: "/photos/pm-temp-2.jpg", alt: "PM Photo 2" },
    { src: "/photos/pm-temp-3.jpg", alt: "PM Photo 3" },
    { src: "/photos/pm-temp-4.jpg", alt: "PM Photo 4" },
    { src: "/photos/pm-temp-5.jpg", alt: "PM Photo 5" },
    { src: "/photos/pm-temp-6.jpg", alt: "PM Photo 6" },
    { src: "/photos/pm-temp-7.jpg", alt: "PM Photo 7" },
    { src: "/photos/pm-temp-8.jpg", alt: "PM Photo 8" },
    { src: "/photos/pm-temp-9.jpg", alt: "PM Photo 9" },
    { src: "/photos/pm-temp-10.jpg", alt: "PM Photo 10" },
    { src: "/photos/pm-temp-11.jpg", alt: "PM Photo 11" },
    { src: "/photos/pm-temp-12.jpg", alt: "PM Photo 12" },
    { src: "/photos/pm-temp-13.jpg", alt: "PM Photo 13" },
    { src: "/photos/pm-temp-14.jpg", alt: "PM Photo 14" },
    { src: "/photos/pm-temp-15.jpg", alt: "PM Photo 15" },
  ];

  return (
    <div className="embla" ref={emblaRef}>
      <div className="embla__container">
        {photos.map((photo, index) => (
          <div className="embla__slide" key={index}>
            <img
              src={photo.src}
              alt={photo.alt}
              className="carousel-image"
            />
          </div>
        ))}
      </div>
    </div>
  )
}


export default ImageCarousel