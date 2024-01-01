const carouselSlides = document.querySelector('.carousel-slides');
const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');
const slides = document.querySelectorAll('.slide');

let counter = 0;
const slideWidth = slides[0].clientWidth;

nextButton.addEventListener('click', () => {
  if (counter < slides.length - 1) {
    counter++;
  } else {
    counter = 0;
  }
  carouselSlides.style.transform = `translateX(${-slideWidth * counter}px)`;
});

prevButton.addEventListener('click', () => {
  if (counter > 0) {
    counter--;
  } else {
    counter = slides.length - 1;
  }
  carouselSlides.style.transform = `translateX(${-slideWidth * counter}px)`;
});
