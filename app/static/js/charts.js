function createLineChart(ctx, label, data, color) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: label,
                data: data,
                borderColor: color,
                backgroundColor: color + "33",
                fill: false,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            animation: false,
            scales: {
                y: { beginAtZero: true }
            },
            plugins: {
                legend: { display: true }
            }
        }
    });
}
