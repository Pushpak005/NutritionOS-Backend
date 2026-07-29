// ===========================================
// NutritionOS - Diet Page
// ===========================================

let selectedDiet = "";

// -------------------------------
// Diet Selection
// -------------------------------
document.querySelectorAll("button").forEach(button => {

    if (button.id !== "recommendBtn") {

        button.addEventListener("click", function () {

            selectedDiet = button.innerText;

            localStorage.setItem("diet", selectedDiet);

            alert("Selected Diet : " + selectedDiet);

        });

    }

});

// -------------------------------
// Get Recommendations
// -------------------------------
document.getElementById("recommendBtn").addEventListener("click", async function () {

    const budget = document.getElementById("budget").value;

    if (selectedDiet === "") {

        alert("Please select your diet.");

        return;

    }

    if (budget === "") {

        alert("Please enter your budget.");

        return;

    }

    localStorage.setItem("budget", budget);

    const requestData = {

        goal: localStorage.getItem("goal"),

        diet: localStorage.getItem("diet"),

        budget: Number(budget)

    };

    try {

        const response = await fetch("/recommend", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(requestData)

        });

        if (!response.ok) {

            throw new Error("API request failed");

        }

        const data = await response.json();

        console.log(data);

        // Save recommendations
        localStorage.setItem(
            "recommendations",
            JSON.stringify(data.recommended_dishes)
        );

        // Go to results page
        window.location.href = "/results";

    }

    catch (error) {

        console.error(error);

        alert("Something went wrong!");

    }

});