const filterBtn = document.getElementById("filterBtn")
const filterForm = document.getElementById('filterForm')
const orders = document.getElementById('orders')

filterBtn.addEventListener("click", function (element) {
    element.preventDefault()
    submitFormData()
})

function submitFormData() {
    const url = '/dashboard/orders-filter/' + 
    '?transaction_id=' + filterForm.transaction_id.value + 
    '&email=' + filterForm.email.value +
    '&date_ordered_start=' + filterForm.date_ordered_start.value + 
    '&date_ordered_end=' + filterForm.date_ordered_end.value + 
    '&status=' + filterForm.status.value
    fetch(url, {
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log(data)
            orders.innerHTML=data
            // updateFormFieldsStatus(data)
        })
}