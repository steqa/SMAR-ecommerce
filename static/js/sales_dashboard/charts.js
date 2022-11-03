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

buildSalesChart()
buildRevenueChart()

const chartSalesDiv = document.getElementById('chartSales')
const chartRevenueDiv = document.getElementById('chartRevenue')

window.onload = getChartData('all_years', null, null, 'sales');
window.onload = getChartData('all_years', null, null, 'revenue');

function updateChartDataBtnClick(element) {
    const chartType = element.dataset.chart
    let period = element.dataset.period
    let selectedYear = null
    let selectedMonth = null

    if (period == 'month') {
        selectedYear = document.querySelector(`[data-chart=${chartType}][data-period="year"].active`)
        if (selectedYear) {
            selectedYear = selectedYear.dataset.value
            selectedMonth = element.dataset.value
        } else {
            period = 'all_years'
            selectedYear = null
            selectedMonth = null
        }
        if (element.classList.contains('active')) {
            period = 'year'
            selectedMonth = null
        }
    } else if (period == 'year') {
        selectedMonth = document.querySelector(`[data-chart=${chartType}][data-period="month"].active`)
        if (selectedMonth) {
            period = 'month'
            selectedYear = element.dataset.value
            selectedMonth = selectedMonth.dataset.value
        } else {
            selectedYear = element.dataset.value
            selectedMonth = null
        }
        if (element.classList.contains('active')) {
            period = 'all_years'
            selectedYear = null
            selectedMonth = null
        }
    }
    getChartData(period, selectedYear, selectedMonth, chartType)
}

function getChartData(period, selectedYear, selectedMonth, chartType) {
    let url = '/dashboard/' +
        '?get_chart_data=' + true +
        '&chart_type=' + chartType
    if (period) {
        url += '&period=' + period +
            '&selected_year=' + selectedYear +
            '&selected_month=' + selectedMonth
    }

    fetch(url, {
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            const chartData = extractChartData(data['chart_data'], data['period'])[0]
            const chartLabels = extractChartData(data['chart_data'], data['period'])[1]

            if (data['chart_data']['type'] == 'sales') {
                chartSalesDiv.innerHTML = data['html']
                buildSalesChart(data = chartData, labels = chartLabels)
            } else if (data['chart_data']['type'] == 'revenue') {
                chartRevenueDiv.innerHTML = data['html']
                buildRevenueChart(data = chartData, labels = chartLabels)
            }
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

function buildSalesChart(data = null, labels = null) {
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

function buildRevenueChart(data = null, labels = null) {
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