const statusFilterBtn = document.querySelectorAll(".statusFilterBtn")

console.log(statusFilterBtn)
statusFilterBtn.forEach(function (element) {
    element.addEventListener("click", function (e) {
        statusFilterBtn.forEach(function (item) {
            item.classList.remove('btn-primary')
            item.classList.add('btn-outline-primary')
        })
        element.classList.remove('btn-outline-primary')
        element.classList.add('btn-primary')
    })
})