function fillRatingBar(rating) {
    let segments = document.querySelectorAll('.rating-segment');

    segments.forEach((segment, index) => {
        setTimeout(() => {
            if (index < rating) {
                segment.classList.add("filled");
            } else {
                segment.classList.remove("filled");
            }
        }, index * 300); // Delays filling each box
    });
}

function highlightSegment(rating) {
    let segment = document.querySelector(`.rating-segment:nth-child(${rating})`);
    segment.classList.add("flash");

    setTimeout(() => {
        segment.classList.remove("flash");
    }, 500);
}
