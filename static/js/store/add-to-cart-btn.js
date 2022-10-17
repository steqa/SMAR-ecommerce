let btn = document.querySelectorAll(".add-to-cart-btn")


btn.forEach(function (item) {
    item.addEventListener("click", active)

    function active() {
        item.classList.toggle("is_active")
        item.disabled = 'disabled'
        setTimeout(function () {
            item.classList.toggle("is_active")
            setTimeout(function () {item.removeAttribute('disabled')}, 350)
        }, 1000)
    }
})