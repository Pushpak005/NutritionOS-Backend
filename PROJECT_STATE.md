# NutritionOS — Project State

## Project
NutritionOS Backend

## Repository
C:\Users\Admin\NutritionOS-Backend

## Current Branch
main

## Git Status
- Working tree clean
- GitHub is up to date
- Latest checkpoint has been committed and pushed
- Current code is safely backed up in GitHub

---

# Current Architecture

## Core Context System

Current active context architecture:

app/core/context/
- context_factory.py
- models.py
- time_context.py

Context model:

Context(
    user_id,
    goal,
    meal_window,
    remaining_calories,
    remaining_protein,
    remaining_carbs,
    remaining_fat,
    remaining_fiber,
    steps,
    calories_burned,
    workout_today,
    breakfast_logged,
    lunch_logged,
    dinner_logged,
    health_connected
)

ContextFactory is the active builder.

CoreService uses ContextFactory:

CoreService().get_context(user_id)

Nutrition state:

app/core/state/nutrition_state.py

NutritionState currently contains:

- remaining_calories
- remaining_protein
- remaining_carbs
- remaining_fat
- remaining_fiber
- meal_window
- goal

build_nutrition_state(context) converts Context → NutritionState.

---

# Providers

Current manual provider:

app/core/providers/manual_provider.py

ManualProvider currently retrieves nutrition data from the database.

Health provider exists:

app/core/providers/health_connect_provider.py

HealthConnectProvider is currently not the primary active source.

Provider contract:

app/core/contracts/provider_contract.py

---

# Legacy Context

Old context pipeline was found at:

app/core/context/pipeline

It referenced the obsolete:

app.context.builder

That builder does not exist.

The old pipeline was moved to:

app/legacy/context_pipeline_legacy.py

Do not restore the old app.context architecture unless explicitly required.

Current active context path is:

app.core.context

---

# Verified Core Tests

User ID tested:

23

ContextFactory test passed.

Example:

Context(
    user_id=23,
    goal='Maintain',
    meal_window='Snack',
    remaining_calories=1897.0,
    remaining_protein=92.0,
    remaining_carbs=263.0,
    remaining_fat=53.0,
    remaining_fiber=30.0,
    steps=0,
    calories_burned=0.0,
    workout_today=False,
    breakfast_logged=False,
    lunch_logged=False,
    dinner_logged=False,
    health_connected=False
)

NutritionState test passed.

ManualProvider test passed.

CoreService → ContextFactory → NutritionState flow passed.

DashboardService import passed.

DashboardService test passed.

Core Context remaining nutrition values matched DashboardService remaining values:

Calories: TRUE
Protein: TRUE
Carbs: TRUE
Fat: TRUE
Fiber: TRUE

---

# Recommendation System

Main recommendation engine:

app/services/recommendation_engine.py

Current scoring components:

Calories Fit       = 20
Protein Fit        = 25
Goal Fit           = 20
Healthy Score      = 15
Macro / Fiber Fit  = 10
Budget Fit         = 5
Restaurant Rating  = 5

Total:

100 points

Additional small contextual nutrition-gap adjustment is applied.

Final score is bounded:

0–100

The recommendation engine uses continuous scoring rather than many hard thresholds.

Main functions:

calculate_nutrition_score()

get_recommendation_reasons()

---

# Recommendation Service

Main file:

app/services/recommendation_service.py

Current flow:

user
→ meal target calories
→ nutrition completion guard
→ load available dishes
→ veg filtering
→ calculate_nutrition_score()
→ get_recommendation_reasons()
→ ranked recommendations

Current Dashboard AI Pick is currently calculated using:

meal_target_calories = get_meal_target_calories(
    user["daily_calories"],
    "Lunch"
)

Top recommendations are sorted by score descending.

---

# Verified Recommendation Output

For user 23:

Remaining:

Calories = 1897
Protein = 92
Carbs = 263
Fat = 53
Fiber = 30

Current best recommendation observed:

Tofu Teriyaki Bowl 134

Score:

89

Other observed top recommendations:

Paneer Burrito = 86
Grilled Tofu Wrap = 86
Vegan Energy Bowl = 86

Example recommendation explanation includes:

- Fits your protein gap
- Fits your remaining calories
- Fits your maintenance goal
- Good healthy score
- Good fiber contribution
- Within your budget
- Highly rated restaurant

---

# Current Backend Structure

Important active areas:

app/main.py

app/core/
app/routers/
app/services/
app/utils/
app/asset/

Important services include:

- dashboard_service.py
- recommendation_engine.py
- recommendation_service.py
- meal_service.py
- menu_service.py
- my_meals_service.py
- score_service.py
- analytics_service.py
- ai_service.py

Important routers include:

- dashboard.py
- meal_logs.py
- recommendations.py
- users.py
- dish.py
- restaurant_details.py

---

# Development Workflow

IMPORTANT:

Do NOT paste entire large source files into ChatGPT unless the entire file genuinely needs review.

Preferred debugging workflow:

1. User runs command in VS Code terminal.
2. User sends command output/error.
3. ChatGPT identifies relevant file.
4. ChatGPT asks for only the relevant section if required.
5. Modify/test.
6. Run verification command.
7. Commit checkpoint when a meaningful milestone is completed.

Use PowerShell commands such as:

Get-Content <file>

or:

Get-Content <file> |
Select-Object -Skip <N> -First <N>

Use Git as the source of truth for code.

Use VS Code as the primary development/testing environment.

Use ChatGPT primarily for:
- architecture
- reasoning
- debugging
- implementation guidance
- code review
- test planning
- project continuity

---

# Chat Continuation Rule

When a ChatGPT conversation becomes large or slow:

Start a new chat inside the same NutritionOS project.

First provide:

"Continue NutritionOS from PROJECT_STATE.md.
Use the project state as the current source of truth.
Do not ask me to paste the entire codebase.
Work one step at a time."

Then attach/provide PROJECT_STATE.md if needed.

The goal is to keep conversations lightweight while preserving project continuity.

---

# Current Milestone

Completed:

1. Core Context architecture established.
2. ContextFactory working.
3. Context model updated with remaining nutrition fields.
4. ManualProvider working.
5. CoreService working.
6. NutritionState working.
7. Legacy context pipeline isolated.
8. DashboardService working.
9. Dashboard remaining nutrition values verified against Core Context.
10. Recommendation engine working.
11. Recommendation scoring and explanations verified.
12. Git checkpoint created.
13. GitHub checkpoint pushed.
14. Working tree clean.

---

# Immediate Next Goal

Continue integrating the new Core Context / NutritionState architecture into the broader NutritionOS application without breaking existing dashboard, recommendation, meal logging, and AI functionality.

Work incrementally.

Do not refactor large portions of the application without first testing the current flow.

---

# Important Rule

Whenever modifying a project file:

Provide the COMPLETE replacement file when code needs to be changed.

Do not provide only a partial snippet when the user is expected to replace a file.

Always give the exact PowerShell command needed to verify the change.

Always verify before moving to the next architectural step.