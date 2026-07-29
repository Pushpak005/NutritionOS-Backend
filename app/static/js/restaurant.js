// ======================================================
// NutritionOS
// Restaurant Page
// ======================================================


// ======================================================
// DOM Elements
// ======================================================

const restaurantInfo =
    document.getElementById("restaurant-info");

const menuItems =
    document.getElementById("menu-items");


// ======================================================
// Global Data
// ======================================================

let allMenuItems = [];

let currentMenu = [];


// ======================================================
// Initial Load
// ======================================================

loadRestaurant();

loadMenu();


// ======================================================
// Load Restaurant Details
// ======================================================

async function loadRestaurant(){

    try{

        const response =
            await fetch(
                `/restaurants/${RESTAURANT_ID}`
            );

        const restaurant =
            await response.json();

        restaurantInfo.innerHTML = `

            <h1>

                🏪 ${restaurant.restaurant_name}

            </h1>

            <div class="restaurant-meta">

                <span>

                    ⭐ ${restaurant.rating}

                </span>

                <span>

                    🛵 ${restaurant.delivery_time} mins

                </span>

                <span>

                    📍 ${restaurant.area}

                </span>

            </div>

            <p>

                ${restaurant.address}

            </p>

        `;

    }

    catch(error){

        restaurantInfo.innerHTML = `

            <h2>

                Unable to load restaurant.

            </h2>

        `;

        console.error(error);

    }

}


// ======================================================
// Load Menu
// ======================================================

async function loadMenu(){

    try{

        const response =
            await fetch(
                `/restaurants/${RESTAURANT_ID}/menu`
            );

        allMenuItems =
            await response.json();

        currentMenu =
            [...allMenuItems];

        renderMenu(currentMenu);

        initializeToolbar();

    }

    catch(error){

        menuItems.innerHTML =

        `

        <div class="food-card">

            <h2>

                Unable to load menu.

            </h2>

        </div>

        `;

        console.error(error);

    }

}



// ======================================================
// Initialize Toolbar
// ======================================================

function initializeToolbar(){

    document

        .getElementById("searchInput")

        .addEventListener(

            "keyup",

            searchDish

        );


    document

        .getElementById("allBtn")

        .addEventListener(

            "click",

            showAll

        );


    document

        .getElementById("vegBtn")

        .addEventListener(

            "click",

            showVeg

        );


    document

        .getElementById("nonVegBtn")

        .addEventListener(

            "click",

            showNonVeg

        );


    document

        .getElementById("proteinBtn")

        .addEventListener(

            "click",

            sortProtein

        );


    document

        .getElementById("calorieBtn")

        .addEventListener(

            "click",

            sortCalories

        );


    document

        .getElementById("priceBtn")

        .addEventListener(

            "click",

            sortPrice

        );

}



// ======================================================
// Render Menu
// ======================================================

function renderMenu(menu){

    menuItems.innerHTML = "";

    if(menu.length===0){

        menuItems.innerHTML =

        `

        <div class="food-card">

            <h2>

                😔 No Dishes Found

            </h2>

        </div>

        `;

        return;

    }

    menu.forEach(item=>{

        const vegBadge =

            item.is_veg

            ? "🟢 Veg"

            : "🔴 Non Veg";

        menuItems.innerHTML += `

        <div class="food-card">

            <div class="card-top">

                <span class="veg-chip">

                    ${vegBadge}

                </span>

            </div>

            <h2>

                🥗 ${item.dish_name}

            </h2>

            <p>

                ${item.category}

            </p>

            <div class="nutrition-grid">

                <div class="nutrition-box">

                    💪

                    <strong>

                        ${item.protein}g

                    </strong>

                    <small>

                        Protein

                    </small>

                </div>

                <div class="nutrition-box">

                    🔥

                    <strong>

                        ${item.calories}

                    </strong>

                    <small>

                        Calories

                    </small>

                </div>
                                <div class="nutrition-box">

                    🥑

                    <strong>

                        ${item.fat}g

                    </strong>

                    <small>

                        Fat

                    </small>

                </div>

                <div class="nutrition-box">

                    🌾

                    <strong>

                        ${item.fiber}g

                    </strong>

                    <small>

                        Fiber

                    </small>

                </div>

            </div>

            <div class="price-row">

                <h3>

                    ₹${item.price}

                </h3>

            </div>

            <button

                class="order-btn"

                onclick="orderDish('${item.dish_name}')">

                🛒 Order Now

            </button>

        </div>

        `;

    });

}



// ======================================================
// Search
// ======================================================

function searchDish(){

    const keyword =

        document

        .getElementById("searchInput")

        .value

        .toLowerCase()

        .trim();

    currentMenu =

        allMenuItems.filter(item =>

            item.dish_name

                .toLowerCase()

                .includes(keyword)

        );

    renderMenu(currentMenu);

}



// ======================================================
// Filters
// ======================================================

function showAll(){

    currentMenu =

        [...allMenuItems];

    renderMenu(currentMenu);

}


function showVeg(){

    currentMenu =

        allMenuItems.filter(

            item => item.is_veg

        );

    renderMenu(currentMenu);

}


function showNonVeg(){

    currentMenu =

        allMenuItems.filter(

            item => !item.is_veg

        );

    renderMenu(currentMenu);

}



// ======================================================
// Sorting
// ======================================================

function sortProtein(){

    currentMenu.sort(

        (a,b)=>

        b.protein-a.protein

    );

    renderMenu(currentMenu);

}


function sortCalories(){

    currentMenu.sort(

        (a,b)=>

        a.calories-b.calories

    );

    renderMenu(currentMenu);

}


function sortPrice(){

    currentMenu.sort(

        (a,b)=>

        a.price-b.price

    );

    renderMenu(currentMenu);

}



// ======================================================
// Order
// ======================================================

function orderDish(dishName){

    alert(

`🍽 Order Placed

Dish:
${dishName}

✅ Online ordering will be available in the next version of NutritionOS.`

    );

}



// ======================================================
// Page Loaded
// ======================================================

console.log(

    "NutritionOS Restaurant Page Loaded 🚀"

);