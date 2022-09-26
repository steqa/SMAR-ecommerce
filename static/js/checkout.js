console.log(totalOrderPrice)

const paymentBtn = document.getElementById('paymentBtn')
const shippingForm = document.getElementById('shippingForm')
console.log(paymentBtn)

paymentBtn.addEventListener('click', function (e) {
    submitFormData()
})

function submitFormData() {
    console.log('Payment btn clicked')
    const shippingInfo = {
        'firstName': null,
        'lastName': null,
        'email': null,
        'address': null,
        'city': null,
        'country': null,
        'postcode': null,
        'totalOrderPrice': totalOrderPrice,
    }

    shippingInfo.firstName = shippingForm.firstName.value
    shippingInfo.lastName = shippingForm.lastName.value
    shippingInfo.email = shippingForm.email.value
    shippingInfo.address = shippingForm.address.value
    shippingInfo.city = shippingForm.city.value
    shippingInfo.country = shippingForm.country.value
    shippingInfo.postcode = shippingForm.postcode.value


    const url = '/place-order/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            shippingInfo
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            console.log('Success:', data)
            alert('Payment complete!')
            window.location.href = storeUrl
        })
}