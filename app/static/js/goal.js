

const name = localStorage.getItem("name");

document.querySelector("h1").innerText =
    "Welcome " + name + " 👋";
document.querySelectorAll("button").forEach(button => {

    button.addEventListener("click", function () {

        localStorage.setItem("goal", button.innerText);

        window.location.href = "/diet";

    });

});