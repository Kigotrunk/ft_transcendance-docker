const short = document.querySelector('.short-menu');
const extanded = document.querySelector('.extanded-menu');
const phone = document.querySelector('.phone-menu');
const blured = document.querySelector('.blured');

extanded.style.display = 'none';

const showMenu = () => {
  if (window.innerWidth < 1224) {
    phone.style.left = 0;
    blured.style.display = 'block';
    document.addEventListener('click', (event) => {
      const menuwidth = phone.offsetWidth;
      if (event.clientX > menuwidth) {
        phone.style.left = '-220px';
        blured.style.display = 'none';
      }
    });
  }
  else {
    if (short.style.display === 'none') {
      short.style.display = 'flex';
      extanded.style.display = 'none';
    }
    else {
      short.style.display = 'none';
      extanded.style.display = 'flex';
    }
  }
}