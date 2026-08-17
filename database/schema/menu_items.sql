DROP TABLE IF EXISTS menu_items CASCADE;

CREATE TABLE menu_items (

    -- =========================================
    -- Primary Information
    -- =========================================

    id SERIAL PRIMARY KEY,

    restaurant_id INT NOT NULL REFERENCES restaurants(restaurant_id),

    dish_name VARCHAR(200) NOT NULL,

    dish_slug VARCHAR(250) UNIQUE,

    description TEXT,

    -- =========================================
    -- Classification
    -- =========================================

    category VARCHAR(100),

    meal_type VARCHAR(50),

    cuisine VARCHAR(100),

    food_type VARCHAR(50),

    -- =========================================
    -- Nutrition
    -- =========================================

    calories DECIMAL(8,2),

    protein DECIMAL(8,2),

    carbs DECIMAL(8,2),

    fat DECIMAL(8,2),

    fiber DECIMAL(8,2),

    sugar DECIMAL(8,2),

    sodium DECIMAL(8,2),

    cholesterol DECIMAL(8,2),

    potassium DECIMAL(8,2),

    calcium DECIMAL(8,2),

    iron DECIMAL(8,2),

    vitamin_c DECIMAL(8,2),

    vitamin_d DECIMAL(8,2),

    -- =========================================
    -- Serving
    -- =========================================

    serving_size DECIMAL(8,2),

    serving_unit VARCHAR(30),

    weight_grams DECIMAL(8,2),

    -- =========================================
    -- Pricing
    -- =========================================

    price DECIMAL(10,2),

    discount_price DECIMAL(10,2),

    currency VARCHAR(10) DEFAULT 'INR',

    -- =========================================
    -- Images
    -- =========================================

    image_url TEXT,

    thumbnail_url TEXT,

    -- =========================================
    -- Dietary Tags
    -- =========================================

    is_veg BOOLEAN DEFAULT FALSE,

    is_vegan BOOLEAN DEFAULT FALSE,

    is_jain BOOLEAN DEFAULT FALSE,

    is_gluten_free BOOLEAN DEFAULT FALSE,

    is_keto BOOLEAN DEFAULT FALSE,

    is_high_protein BOOLEAN DEFAULT FALSE,

    -- =========================================
    -- Popularity
    -- =========================================

    healthy_score INT,

    popularity_score INT,

    times_ordered INT DEFAULT 0,

    average_rating DECIMAL(3,2),

    total_reviews INT DEFAULT 0,

    -- =========================================
    -- Cooking
    -- =========================================

    prep_time INT,

    spice_level VARCHAR(20),

    difficulty VARCHAR(20),

    -- =========================================
    -- AI
    -- =========================================

    ingredients JSONB,

    allergens JSONB,

    nutrition_tags JSONB,

    ai_summary TEXT,

    -- =========================================
    -- Availability
    -- =========================================

    available BOOLEAN DEFAULT TRUE,

    seasonal BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);