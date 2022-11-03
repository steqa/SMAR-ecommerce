const updateDifferenceStatBtn = document.querySelectorAll('.updateDifferenceStatBtn')

getDifferenceStat('month')

updateDifferenceStatBtn.forEach(function (element) {
    element.addEventListener('click', function () {
        document.querySelector('.updateDifferenceStatBtn.active').classList.remove('active')
        element.classList.add('active')

        document.querySelector('[data-difference-btn]').innerHTML = element.innerHTML
        getDifferenceStat(period = element.dataset.period)
    })
})

function getDifferenceStat(period) {
    const url = '/dashboard/' +
        '?get_difference_stat=' + true +
        '&period=' + period

    fetch(url, {
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log(data)
            document.querySelector('[data-sales-difference]').innerHTML = data['sales_difference']
            document.querySelector('[data-revenue-difference]').innerHTML = data['revenue_difference']

            const salesSignPlus = document.querySelector('[data-sales-difference-sign="+"]')
            const salesSignMinus = document.querySelector('[data-sales-difference-sign="-"]')
            if (data['sales_sign'] == '+') {
                salesSignPlus.classList.remove('hide')
                salesSignMinus.classList.add('hide')
            } else if (data['sales_sign'] == '-') {
                salesSignPlus.classList.add('hide')
                salesSignMinus.classList.remove('hide')
            } else if (data['sales_sign'] == '0') {
                salesSignPlus.classList.add('hide')
                salesSignMinus.classList.add('hide')
            }

            const revenueSignPlus = document.querySelector('[data-revenue-difference-sign="+"]')
            const revenueSignMinus = document.querySelector('[data-revenue-difference-sign="-"]')
            if (data['revenue_sign'] == '+') {
                revenueSignPlus.classList.remove('hide')
                revenueSignMinus.classList.add('hide')
            } else if (data['revenue_sign'] == '-') {
                revenueSignPlus.classList.add('hide')
                revenueSignMinus.classList.remove('hide')
            } else if (data['revenue_sign'] == '0') {
                revenueSignPlus.classList.add('hide')
                revenueSignMinus.classList.add('hide')
            }
        })
}