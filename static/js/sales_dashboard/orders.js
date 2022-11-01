const filterForm = document.getElementById('filterForm')
const sortForm = document.getElementById('sortForm')

const filterFields = document.querySelectorAll('.form-control')
const sortFields = document.querySelectorAll('.sort-checkbox')
const pageBtn = document.querySelectorAll('.page-link')

const orders = document.getElementById('orders')

const displayedOrders = document.getElementById('displayedOrders')
const totalOrders = document.getElementById('totalOrders')

let onscrollFunction = true
window.onscroll = function () {
    if (onscrollFunction === true) {
        let posTop = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;
        if (posTop + window.innerHeight === document.documentElement.scrollHeight) {
            submitFormData(paginate = true)
        }
    }
}

filterFields.forEach((element) => {
    element.addEventListener('input', function (e) {
        e.preventDefault()
        submitFormData()
    })
})

sortFields.forEach((element) => {
    element.addEventListener('input', function (e) {
        e.preventDefault()

        sortFields.forEach((field) => {
            if (field != element) {
                field.dataset.checkbox = 0
                label = document.querySelector(`[for="${field.id}"]`)
                label.querySelector('.checkDown').classList.add('hide')
                label.querySelector('.checkUp').classList.add('hide')
            }
        })

        label = document.querySelector(`[for="${element.id}"]`)
        if (element.dataset.checkbox == '0') {
            element.dataset.checkbox = 1
            label.querySelector('.checkDown').classList.toggle('hide')
        } else if (element.dataset.checkbox == '1') {
            element.dataset.checkbox = 2
            label.querySelector('.checkDown').classList.toggle('hide')
            label.querySelector('.checkUp').classList.toggle('hide')
        } else if (element.dataset.checkbox == '2') {
            element.dataset.checkbox = 1
            label.querySelector('.checkDown').classList.toggle('hide')
            label.querySelector('.checkUp').classList.toggle('hide')
        }

        submitFormData()
    })
})

pageBtn.forEach((element) => {
    element.addEventListener('click', function (e) {
        e.preventDefault()
        submitFormData(element)
    })
})

function submitFormData(paginate) {
    let url = '/dashboard/orders/' +
        '?sort=' + true +
        '?&ransaction_id=' + filterForm.transaction_id.value +
        '&email=' + filterForm.email.value +
        '&date_ordered_min=' + filterForm.date_ordered_min.value +
        '&date_ordered_max=' + filterForm.date_ordered_max.value +
        '&status=' + filterForm.status.value +
        '&sort_transaction_id=' + sortForm.sort_transaction_id.dataset.checkbox +
        '&sort_email=' + sortForm.sort_email.dataset.checkbox +
        '&sort_date_ordered=' + sortForm.sort_date_ordered.dataset.checkbox +
        '&sort_status=' + sortForm.sort_status.dataset.checkbox
    if (paginate) { url += '&page=' + (Number(document.getElementById('page').innerHTML) + 1) }
    
    fetch(url, {
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            if (data['show_next_page'] === null) {
                orders.innerHTML = data['html']
                page.innerHTML = 1
                onscrollFunction = true
            } else {
                orders.insertAdjacentHTML('beforeend', data['html'])
                page.innerHTML = Number(page.innerHTML) + 1
                if (data['show_next_page'] === false) {
                    onscrollFunction = false
                }
            }
            displayedOrders.innerHTML = data['displayed_orders']
            totalOrders.innerHTML = data['total_orders']
        })
}