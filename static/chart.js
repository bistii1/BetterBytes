document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('ingredientChart').getContext('2d');

    const data = {
        labels: ["High Fructose Corn Syrup", "Trans Fats", "MSG", "Aspartame", "Artificial Colors", "Sodium Nitrate"],
        datasets: [{
            label: "Occurrences in Food Products",
            data: [120, 95, 80, 75, 70, 60], // Example data
            backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: true
                }
            }
        }
    };

    new Chart(ctx, config);
});
