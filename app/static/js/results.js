// ======================================================
// NutritionOS
// Results Page
// Version 3.0
// ======================================================


// ------------------------------------------------------
// Load Recommendations
// ------------------------------------------------------

const dishes =
    JSON.parse(
        localStorage.getItem("recommendations")
    ) || [];


// ------------------------------------------------------
// DOM Elements
// ------------------------------------------------------

const resultsDiv =
    document.getElementById("results");


// ------------------------------------------------------
// Nutrition Goals
// ------------------------------------------------------

const GOALS = {

    protein: 50,

    calories: 2200,

    fat: 60,

    fiber: 30

};


// ------------------------------------------------------
// Dashboard Totals
// ------------------------------------------------------

let totalProtein = 0;

let totalCalories = 0;

let totalFat = 0;

let totalFiber = 0;


// ------------------------------------------------------
// Clear Previous Cards
// ------------------------------------------------------

resultsDiv.innerHTML = "";


// ------------------------------------------------------
// No Recommendation
// ------------------------------------------------------

if (dishes.length === 0) {

    resultsDiv.innerHTML = `

        <div class="food-card">

            <h2>
                😔 No Recommendations Found
            </h2>

            <p>
                Please go back and select your preferences.
            </p>

        </div>

    `;

}


// ------------------------------------------------------
// Dashboard Totals
// ------------------------------------------------------

dishes.forEach(dish => {

    totalProtein += Number(dish.protein || 0);

    totalCalories += Number(dish.calories || 0);

    totalFat += Number(dish.fat || 0);

    totalFiber += Number(dish.fiber || 0);

});


// ------------------------------------------------------
// Update Dashboard
// ------------------------------------------------------

updateProgress(

    "proteinProgress",

    "proteinText",

    totalProtein,

    GOALS.protein,

    "g"

);

updateProgress(

    "calorieProgress",

    "calorieText",

    totalCalories,

    GOALS.calories,

    "kcal"

);

updateProgress(

    "fatProgress",

    "fatText",

    totalFat,

    GOALS.fat,

    "g"

);

updateProgress(

    "fiberProgress",

    "fiberText",

    totalFiber,

    GOALS.fiber,

    "g"

);


// ------------------------------------------------------
// Render Recommendation Cards
// ------------------------------------------------------

dishes.forEach((dish, index) => {

    const vegBadge =
        dish.is_veg
            ? "🟢 Veg"
            : "🔴 Non Veg";

    const rating =
        dish.rating ?? "N/A";

    const area =
        dish.area ?? "Location Not Available";

    const delivery =
        dish.delivery_time ?? "--";

    const score =
        dish.nutrition_score ?? 0;

    const reason =
        dish.recommendation_reason ?? "Nutrition information unavailable";

    let scoreColor = "#f39c12";

    if (score >= 90) {

        scoreColor = "#27ae60";

    }
    else if (score >= 75) {

        scoreColor = "#2ecc71";

    }
    else if (score >= 60) {

        scoreColor = "#f1c40f";

    }
    else {

        scoreColor = "#e74c3c";

    }

    resultsDiv.innerHTML += `

    <div class="food-card">

        <div class="card-top">

            <span class="rank-badge">

                #${index + 1}

            </span>

            <span class="veg-chip">

                ${vegBadge}

            </span>

        </div>

        <h2 class="dish-title">

            🥗 ${dish.dish_name}

        </h2>

        <p class="restaurant-name">

            🏪 ${dish.restaurant_name}

        </p>

        <div class="nutrition-score-box">

            <h3>

                ⭐ Nutrition Score

            </h3>

            <div
                class="nutrition-score"
                style="color:${scoreColor};">

                ${score}/100

            </div>

            <p class="nutrition-reason">

                💡 ${reason}

            </p>

        </div>

        <div class="info-row">

            <span>

                ⭐ ${rating}

            </span>

            <span>

                🛵 ${delivery} mins

            </span>

        </div>

        <div class="info-row">

            <span>

                📍 ${area}

            </span>

        </div>

        <div class="nutrition-grid">

            <div class="nutrition-box">

                💪

                <strong>

                    ${dish.protein} g

                </strong>

                <small>

                    Protein

                </small>

            </div>

            <div class="nutrition-box">

                🔥

                <strong>

                    ${dish.calories}

                </strong>

                <small>

                    Calories

                </small>

            </div>

            <div class="nutrition-box">

                🥑

                <strong>

                    ${dish.fat} g

                </strong>

                <small>

                    Fat

                </small>

            </div>

            <div class="nutrition-box">

                🌾

                <strong>

                    ${dish.fiber} g

                </strong>

                <small>

                    Fiber

                </small>

            </div>

        </div>

        <div class="price-row">

            <h3>

                ₹${dish.price}

            </h3>

        </div>

        <button

            class="order-btn"

            onclick="viewRestaurant(${dish.restaurant_id})">

            🛒 Order Now

        </button>

    </div>

    `;

});


// ------------------------------------------------------
// Progress Bar
// ------------------------------------------------------

function updateProgress(

    progressId,

    textId,

    current,

    goal,

    unit

) {

    const progressBar =
        document.getElementById(progressId);

    const text =
        document.getElementById(textId);

    if (!progressBar || !text) {

        return;

    }

    const percentage =

        Math.min(

            (current / goal) * 100,

            100

        );

    progressBar.style.width =

        percentage + "%";

    text.innerHTML =

        current.toFixed(1)

        + " / "

        + goal

        + " "

        + unit;

}


// ------------------------------------------------------
// Restaurant Navigation
// ------------------------------------------------------

function viewRestaurant(restaurantId) {

    window.location.href =

        `/restaurant/${restaurantId}`;

}


// ------------------------------------------------------
// Console
// ------------------------------------------------------

console.log(

    "NutritionOS Results Loaded Successfully 🚀"

);