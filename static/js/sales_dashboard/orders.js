const filterBtn = document.getElementById("filterBtn")
const filterForm = document.getElementById('filterForm')
const formFields = document.querySelectorAll('.form-control')
const orders = document.getElementById('orders')

formFields.forEach((element) => {
    element.addEventListener('input', function (e) {
        e.preventDefault()
        submitFormData()
    })
})

filterBtn.addEventListener("click", function (element) {
    element.preventDefault()
    submitFormData()
})

function submitFormData() {
    const url = '/dashboard/orders-filter/' + 
    '?transaction_id=' + filterForm.transaction_id.value + 
    '&email=' + filterForm.email.value +
    '&date_ordered_min=' + filterForm.date_ordered_min.value + 
    '&date_ordered_max=' + filterForm.date_ordered_max.value + 
    '&status=' + filterForm.status.value
    fetch(url, {
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            orders.innerHTML=data['html']
        })
}