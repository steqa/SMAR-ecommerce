const registerBtn = document.getElementById('registerBtn')
const registrationForm = document.getElementById('registrationForm')
const formFields = document.querySelectorAll('.form-control')

formFields.forEach((element) => {
    element.addEventListener('input', function (e) {
        const reload = false
        submitFormData(reload)
    })
})

registerBtn.addEventListener('click', function (element) {
    element.preventDefault()
    const reload = true
    submitFormData(reload)
})

function submitFormData(reload) {
    const registrationInfo = getFormData()['registrationInfo']

    const url = '/user/registration/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'registrationInfo': registrationInfo,
            'reload': reload
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            if (data['reload'] == true) {
                alert('Registered!')
                window.location.replace(storeUrl)
            }
            updateFormFieldsStatus(data)
        })
}

function getFormData() {
    const registrationInfo = {
        'fio': null,
        'email': null,
        'username': null,
        'password1': null,
        'password2': null,
    }

    registrationInfo.fio = registrationForm.fio.value
    registrationInfo.email = registrationForm.email.value
    registrationInfo.username = registrationForm.email.value
    registrationInfo.password1 = registrationForm.password1.value
    registrationInfo.password2 = registrationForm.password2.value

    return { 'registrationInfo': registrationInfo }
}

function updateFormFieldsStatus(data) {
    for (error in data['errors']) {
        if (data['errors'][error] == '&bull;&nbsp;Обязательное поле.') {
            data['error_fields'].splice(data['error_fields'].indexOf(error), 1)
        }
    }

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
        } else {
            element.classList.remove('is-valid')
            element.classList.remove('is-invalid')
        }
    })
}