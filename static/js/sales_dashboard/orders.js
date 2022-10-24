const filterForm = document.getElementById('filterForm')
const sortForm = document.getElementById('sortForm')
const filterFields = document.querySelectorAll('.form-control')
const sortFields = document.querySelectorAll('.sort-checkbox')
const orders = document.getElementById('orders')

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

function submitFormData() {
    const url = '/dashboard/orders-filter/' +
        '?transaction_id=' + filterForm.transaction_id.value +
        '&email=' + filterForm.email.value +
        '&date_ordered_min=' + filterForm.date_ordered_min.value +
        '&date_ordered_max=' + filterForm.date_ordered_max.value +
        '&status=' + filterForm.status.value +
        '&sort_transaction_id=' + sortForm.sort_transaction_id.dataset.checkbox +
        '&sort_email=' + sortForm.sort_email.dataset.checkbox +
        '&sort_date_ordered=' + sortForm.sort_date_ordered.dataset.checkbox +
        '&sort_status=' + sortForm.sort_status.dataset.checkbox
    fetch(url, {
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            orders.innerHTML = data['html']
        })
}