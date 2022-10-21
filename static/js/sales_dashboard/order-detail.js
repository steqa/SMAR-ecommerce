const statusSelect = document.getElementById('status')
const dateUpdated = document.getElementById('dateUpdated')

statusSelect.addEventListener('input', function (element) {
    element.preventDefault()
    submitFormData()
})

function submitFormData() {
    const url = '/dashboard/order/' + orderID + '/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'status': statusSelect.value,
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            statusSelect.removeAttribute('class')
            if (data['status'] == '1') {
                statusSelect.classList.add('form-control')
                statusSelect.classList.add('form-select')
                statusSelect.classList.add('danger-input')
            } else if (data['status'] == '2') {
                statusSelect.classList.add('form-control')
                statusSelect.classList.add('form-select')
                statusSelect.classList.add('warning-input')
            } else if (data['status'] == '3') {
                statusSelect.classList.add('form-control')
                statusSelect.classList.add('form-select')
                statusSelect.classList.add('success-input')
            }
            dateUpdated.innerHTML=data['date_updated']
        })
}