document.querySelector("button").addEventListener("click", function () {

    const name = document.querySelector('input[type="text"]').value;

    const age = document.querySelector('input[type="number"]').value;

    localStorage.setItem("name", name);

    localStorage.setItem("age", age);

    window.location.href = "/goal";

});