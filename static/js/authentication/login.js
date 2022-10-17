const loginBtn = document.getElementById('loginBtn')
const loginForm = document.getElementById('loginForm')
const formFields = document.querySelectorAll('.form-control')

formFields.forEach((element) => {
    element.addEventListener('input', function (e) {
        const reload = false
        submitFormData(reload)
    })
})

loginBtn.addEventListener('click', function (element) {
    element.preventDefault()
    const reload = true
    submitFormData(reload)
})

function submitFormData(reload) {
    const loginInfo = getFormData()['loginInfo']

    const url = '/user/login/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'loginInfo': loginInfo,
            'reload': reload
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            if (data['reload'] == true) {
                alert('Logged in!')
                window.location.replace(storeUrl)
            }
            updateFormFieldsStatus(data)
        })
}

function getFormData() {
    const loginInfo = {
        'email': null,
        'password': null,
    }
    loginInfo.email = loginForm.email.value
    loginInfo.password = loginForm.password.value

    return { 'loginInfo': loginInfo }
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