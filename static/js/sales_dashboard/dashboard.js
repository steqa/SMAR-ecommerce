const monthsLabels = [
    'Янв',
    'Фев',
    'Мар',
    'Апр',
    'Май',
    'Июн',
    'Июл',
    'Авг',
    'Сен',
    'Окт',
    'Ноя',
    'Дек',
];

const optionsElements = {
    point: {
        radius: 5,
        hitRadius: 10,
        hoverRadius: 10,
    },
    line: {
        tension: 0.2,
        borderWidth: 4,
    }
}

updateSalesChartData()
updateRevenueChartData()
window.onload = getChartData();

const chartsDiv = document.getElementById('charts')
const updateSalesChartDataBtn = document.querySelectorAll('.updateSalesChartDataBtn')
const updateRevenueChartDataBtn = document.querySelectorAll('.updateRevenueChartDataBtn')

updateSalesChartDataBtn.forEach((element) => {
    element.addEventListener('click', function (e) {
        const period = element.dataset['period']
        if (period == 'month') {
            
        }
        // getChartData(period)
    })
})

function getChartData(period) {
    let url = '/dashboard/render-chart-data/'

    fetch(url, {
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            chartsDiv.innerHTML = data['html']

            const salesData = extractChartData(data['sales_chart_data'], data['period'])[0]
            const salesLabels = extractChartData(data['sales_chart_data'], data['period'])[1]
            const revenueData = extractChartData(data['revenue_chart_data'], data['period'])[0]
            const revenueLabels = extractChartData(data['revenue_chart_data'], data['period'])[1]
            updateSalesChartData(data = salesData, labels = salesLabels)
            updateRevenueChartData(data = revenueData, labels = revenueLabels)
        })
}

function extractChartData(data, period) {
    const quantityData = data['data']
    let labelsData = []
    if (period == 'year') {
        for (label in data['labels']) {
            labelsData.push(monthsLabels[label])
        }
    }
    else {
        labelsData = data['labels']
    }
    return [quantityData, labelsData]
}

function updateSalesChartData(data = null, labels = monthsLabels) {
    const salesData = {
        labels: labels,
        datasets: [{
            label: 'Продаж',
            backgroundColor: 'rgb(13, 110, 253)',
            borderColor: 'rgb(13, 110, 253)',
            data: data,
        }]
    };

    const salesConfig = {
        type: 'line',
        data: salesData,
        options: {
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    displayColors: false,
                },
            },
            elements: optionsElements
        }
    };

    const sales = new Chart(
        document.getElementById('sales'),
        salesConfig
    );
}

function updateRevenueChartData(data = null, labels = monthsLabels) {
    const revenueData = {
        labels: labels,
        datasets: [{
            label: 'Выручка:',
            backgroundColor: 'rgb(13, 110, 253)',
            borderColor: 'rgb(13, 110, 253)',
            data: data,
        }]
    };

    const revenueConfig = {
        type: 'line',
        data: revenueData,
        options: {
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.dataset.label || '';

                            if (label) {
                                label += ' ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('ru', { style: 'currency', currency: 'RUB' }).format(context.parsed.y);
                            }
                            return label;
                        },
                    },
                    displayColors: false,
                },
            },
            elements: optionsElements
        }
    };

    const revenue = new Chart(
        document.getElementById('revenue'),
        revenueConfig
    );
}