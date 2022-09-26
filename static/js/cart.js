const updateBtns = document.querySelectorAll('[data-action]')

updateBtns.forEach(function (item) {
    item.addEventListener('click', function () {
        const productID = this.dataset.product
        const action = this.dataset.action

        if (user == 'AnonymousUser') {
            console.log('Not logged in')
        } else {
            updateOrder(productID, action)
        }
    })
})

function updateOrder(productID, action) {
    const url = '/update-order/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productID': productID,
            'action': action,
        }),
    })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            const product = document.getElementById(productID)
            if (product) {
                if (data['productQuantity'] <= 0) {
                    product.remove()
                } else {
                    product.querySelector('.productQuantity').innerHTML = data['productQuantity']
                    product.querySelector('.productTotalPrice').innerHTML = data['productTotalPrice']
                }

                document.querySelector('.totalOrderPrice').innerHTML = data['totalOrderPrice']
                document.querySelector('.totalOrderQuantity').innerHTML = data['totalOrderQuantity']
            }

            if (data['cartItems']) {
                document.querySelector('.cart').innerHTML = data['cartItems']
            } else {
                document.querySelector('.cart').remove()
            }
        })
}