var ctx = document.getElementById('lineChart').getContext('2d');

        // 初始化图表
        var lineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Wcoins',
                    data: [],
                    borderColor: 'blue',
                    fill: false
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Price/Value'
                        }
                    }
                }
            }
        });
setInterval(function() {
            fetch("{{ url_for('data')}}")
                .then(response => response.json())
                .then(data => {
                    // 更新图表数据
                    lineChart.data.labels = data.map(entry => entry.date);
                    lineChart.data.datasets[0].data = data.map(entry => entry.price);
                    lineChart.update();
                });
        }, 1000);
