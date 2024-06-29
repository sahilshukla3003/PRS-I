const searchbtn = document.querySelector('.searchbtn');
const spinner = document.querySelector('.spinner');
//on click to show spinner
searchbtn.addEventListener('click', () => {
    spinner.style.display = 'block';
    window.addEventListener('load', () => {
        spinner.style.display = 'none';
    });
});