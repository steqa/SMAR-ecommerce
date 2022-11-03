const updateStatusStatBtn = document.querySelectorAll('.updateStatusStatBtn')

updateStatusStatBtn.forEach(function (element) {
    element.addEventListener('click', function () {
        document.querySelector(`.updateStatusStatBtn.active[data-status="${element.dataset.status}"]`).classList.remove('active')
        element.classList.add('active')

        document.querySelector(`[data-status-btn="${element.dataset.status}"]`).innerHTML = element.innerHTML
        getStatusStat(element)
    })
})

function getStatusStat(element) {
    const url = '/dashboard/' +
        '?get_order_status_stat=' + true +
        '&period=' + element.dataset.period +
        '&status=' + element.dataset.status

    fetch(url, {
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            document.querySelector(`[data-status-value="${element.dataset.status}"]`).innerHTML = data['orders']
        })
}