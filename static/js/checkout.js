const paymentBtn = document.getElementById('paymentBtn')
const checkoutForm = document.getElementById('checkoutForm')
const formFields = document.querySelectorAll('.form-control')

paymentBtn.addEventListener('click', function (element) {
    element.preventDefault()
    submitFormData()
})

function submitFormData() {
    const userInfo = {
        'email': null,
        'first_name': null,
        'last_name': null,
        'username': null,
        'password1': null,
        'password2': null,
    }
    const shippingInfo = {
        'address': null,
        'city': null,
        'country': null,
        'postcode': null,
        'totalOrderPrice': totalOrderPrice,
    }

    userInfo.email = checkoutForm.email.value
    userInfo.first_name = checkoutForm.first_name.value
    userInfo.last_name = checkoutForm.last_name.value
    if (user == 'AnonymousUser') {
        userInfo.username = checkoutForm.username.value
        userInfo.password1 = checkoutForm.password1.value
        userInfo.password2 = checkoutForm.password2.value
    }

    shippingInfo.address = checkoutForm.address.value
    shippingInfo.city = checkoutForm.city.value
    shippingInfo.country = checkoutForm.country.value
    shippingInfo.postcode = checkoutForm.postcode.value

    const url = '/place-order/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'userInfo': userInfo,
            'shippingInfo': shippingInfo,
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            // alert('Payment complete!')
            formFields.forEach((element) => {
                invalidFeedbackBlock = element.closest('.form-floating').querySelector('.invalid-feedback')

                if (data['error_fields'].includes(element.getAttribute('name'))) {
                    element.classList.remove('is-valid')
                    element.classList.add('is-invalid')
                    invalidFeedbackBlock.textContent = data['errors'][element.getAttribute('name')]
                } else if (data['success_fields'].includes(element.getAttribute('name'))) {
                    element.classList.remove('is-invalid')
                    element.classList.add('is-valid')
                    invalidFeedbackBlock.textContent = ''
                }
            })

            if (user == 'AnonymousUser') {
                cart = {}
                document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
                // window.location.replace(storeUrl)
            } else {
                // window.location.replace(storeUrl)
            }
        })
}