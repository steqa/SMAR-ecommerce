const updateBtns = document.querySelectorAll('[data-action]')

updateBtns.forEach(function (item) {
    item.addEventListener('click', function () {
        const productID = this.dataset.product
        const action = this.dataset.action

        if (user == 'AnonymousUser') {
            addCoockieItem(productID, action)
        } else {
            updateOrder(productID, action)
        }
    })
})

function addCoockieItem(productID, action) {
    if (action == 'add') {
        if (cart[productID] == undefined) {
            cart[productID] = { 'quantity': 1 }
        } else {
            cart[productID]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productID]['quantity'] -= 1
        if (cart[productID]['quantity'] <= 0) {
            delete cart[productID]
        }
    }

    updateOrder(productID, action)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
}

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
                    product.querySelector('.productPrice').innerHTML = data['productPrice']
                }

                document.querySelector('.cartTotalPrice').innerHTML = data['cartTotalPrice']
                document.querySelector('.cartTotalQuantity').innerHTML = data['cartTotalQuantity']
            }

            if (data['cartTotalQuantity']) {
                document.querySelector('.cart').innerHTML = data['cartTotalQuantity']
            } else {
                document.querySelector('.cart').remove()
            }
        })
}