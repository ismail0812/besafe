let head = document.querySelectorAll('nav ul li a')
head.forEach(function (el) {
    
    el.onclick = function () {
        head.forEach(function(el) {
            el.classList.remove("active");
        })
        this.classList.add("active");
    }
})



