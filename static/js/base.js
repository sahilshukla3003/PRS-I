const navToggle = document.querySelector('.nav-toggle');
const navList = document.querySelector('.nav-list');
const navOverlay = document.querySelector('.nav-overlay');

navToggle.addEventListener('click', () => {
    navToggle.classList.toggle('active');
    navList.classList.toggle('active');
    navOverlay.classList.toggle('active');
});