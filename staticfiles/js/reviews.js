reviews = document.querySelectorAll('.review-card');
var i = 1;
// iterate through each review
reviews.forEach((review) => {
    if(i == 1)
        review.style.backgroundColor = '#3fbafe';
    else if(i == 2)
        review.style.backgroundColor = '#f7a976';
    else if(i == 3)
        review.style.backgroundColor = '#b69efe';
    else if(i == 4)
        review.style.backgroundColor = '#60efbc';
    else if(i == 5)
        review.style.backgroundColor = '#f588d8';
    else
        i = 1;
    i++;
});

function myFunction() {
    // Declare variables
    var input, filter, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    reviews = document.querySelectorAll('.card');
    // Loop through all list items, and hide those who don't match the search query
    reviews.forEach((review) => {
        txtValue = review.textContent || review.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            review.style.display = "";
        } else {
            review.style.display = "none";
        }
    });
}