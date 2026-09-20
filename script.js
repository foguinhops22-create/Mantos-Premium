function buy(product){
  const msg = 'Olá, estou interessado em uma camisa.';
  window.open('https://wa.me/5511911321494?text=' + encodeURIComponent(msg), '_blank');
}

document.querySelectorAll('[data-carousel]').forEach((carousel) => {
  const slides = carousel.querySelectorAll('.carousel-slide, .corinthians-slide');
  const dots = carousel.querySelectorAll('.carousel-dot');
  const prev = carousel.querySelector('.carousel-prev');
  const next = carousel.querySelector('.carousel-next');
  let current = 0;
  function show(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => slide.classList.toggle('is-active', i === current));
    dots.forEach((dot, i) => dot.classList.toggle('is-active', i === current));
    carousel.classList.toggle('show-prev', current > 0);
  }
  prev?.addEventListener('click', () => show(current - 1));
  next?.addEventListener('click', () => show(current + 1));
  show(0);
});
