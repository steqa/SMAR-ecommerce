const updateBtns = document.querySelectorAll('[data-action]');

updateBtns.forEach(function (item) {
    item.addEventListener('click', function () {
        const productId = this.dataset.product
        const action = this.dataset.action
        console.log('productID:', productId, 'action:', action)
        console.log('user:', user)
    });
});