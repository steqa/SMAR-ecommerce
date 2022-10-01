const paymentBtn = document.getElementById('paymentBtn')
const checkoutForm = document.getElementById('checkoutForm')
const formFields = document.querySelectorAll('.form-control')

formFields.forEach((element) => {
    element.addEventListener('input', function (e) {
        const shippingInfo = getFormData()['shippingInfo']
        const userInfo = getFormData()['userInfo']

        const url = '/place-order-form-validation/'
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'userInfo': userInfo,
                'shippingInfo': shippingInfo,
                'totalOrderPrice': totalOrderPrice,
            }),
        })

            .then((response) => {
                return response.json()
            })

            .then((data) => {
                for (error in data['errors']) {
                    if (data['errors'][error] == '&bull;&nbsp;Обязательное поле.') {
                        data['error_fields'].splice(data['error_fields'].indexOf(error), 1)
                    }
                }
                updateFormFieldsStatus(data)
            })
    })
})

paymentBtn.addEventListener('click', function (element) {
    element.preventDefault()
    submitFormData()
})

function submitFormData() {
    const shippingInfo = getFormData()['shippingInfo']
    const userInfo = getFormData()['userInfo']

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
            'totalOrderPrice': totalOrderPrice,
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            updateFormFieldsStatus(data)

            if (data['validation_error'] == false) {
                if (user == 'AnonymousUser') {
                    cart = {}
                    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
                    alert('Payment complete!')
                    window.location.replace(storeUrl)
                } else {
                    alert('Payment complete!')
                    window.location.replace(storeUrl)
                }
            }
        })
}

function getFormData() {
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
    }

    if (user == 'AnonymousUser') {
        userInfo.email = checkoutForm.email.value
        userInfo.first_name = checkoutForm.first_name.value
        userInfo.last_name = checkoutForm.last_name.value
        userInfo.username = checkoutForm.username.value
        userInfo.password1 = checkoutForm.password1.value
        userInfo.password2 = checkoutForm.password2.value
    }

    shippingInfo.address = checkoutForm.address.value
    shippingInfo.city = checkoutForm.city.value
    shippingInfo.country = checkoutForm.country.value
    shippingInfo.postcode = checkoutForm.postcode.value

    return { 'shippingInfo': shippingInfo, 'userInfo': userInfo }
}

function updateFormFieldsStatus(data) {
    formFields.forEach((element) => {
        invalidFeedbackBlock = element.closest('.form-floating').querySelector('.invalid-feedback')

        if (data['error_fields'].includes(element.getAttribute('name'))) {
            element.classList.remove('is-valid')
            element.classList.add('is-invalid')
            invalidFeedbackBlock.innerHTML = data['errors'][element.getAttribute('name')]
        } else if (data['success_fields'].includes(element.getAttribute('name'))) {
            element.classList.remove('is-invalid')
            element.classList.add('is-valid')
            invalidFeedbackBlock.innerHTML = ''
        }
    })
}