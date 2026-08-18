# NutritionOS — PROJECT SOURCE OF TRUTH

**Baseline:** 18 August 2026  
**Status:** Active Development  
**Product:** Autonomous Nutrition Operating System

---

## 1. WHAT NUTRITIONOS IS

NutritionOS is a state-aware nutrition decision system.

It should understand:

**User → Targets → Meals → Current Nutrition State → Context → Policy → Recommendation → User Action → Updated State**

The recommendation must be based on the user's current nutrition state and constraints, not popularity alone.

The long-term objective is to evolve this into an autonomous nutrition operating system that continuously updates its understanding of the user and makes increasingly context-aware nutrition decisions.

---

# 2. SOURCE-OF-TRUTH RULE

When reasoning about NutritionOS, use this priority:

1. Actual source code + verified runtime tests
2. Current database state
3. This PROJECT_STATE.md
4. Historical project documents
5. Future roadmap / ideas

If documentation and code disagree:

**Inspect the code and runtime first.**

Never silently invent an implementation.

Never describe planned functionality as implemented.

---

# 3. CURRENT STACK

## Frontend

Primary frontend:

`C:\Users\Admin\NutritionOS-Frontend`

Technology:

- React
- Vite
- React Router
- Axios

Important service areas include:

- dashboard service
- meal service
- my meals service
- API client

---

## Backend

Primary backend:

`C:\Users\Admin\NutritionOS-Backend`

Technology:

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL / Supabase

Important areas:

- `app/core`
- `app/services`
- `app/routers`
- `app/database`
- `app/utils`

---

# 4. CURRENT ARCHITECTURE

The intended decision pipeline is:

**Database / Nutrition Events**
→ **Context**
→ **NutritionState**
→ **Policy**
→ **Ranking**
→ **Explanation**
→ **User Action**
→ **New Nutrition Event**
→ **Updated State**

### Context / State

Answers:

> What is true about the user right now?

### Policy

Answers:

> What is allowed or appropriate?

### Ranking

Answers:

> Which available food option is best for the current state?

### Explanation

Answers:

> Why was this recommendation selected?

Deterministic nutrition logic remains authoritative.

LLMs must not override deterministic nutrition constraints.

---

# 5. CURRENTLY WORKING / VERIFIED

The following capabilities are implemented and have been exercised through runtime/database tests:

- User/profile nutrition data
- Daily nutrition targets
- Meal logging / nutrition events
- Today's consumed nutrition
- Remaining nutrition
- ContextFactory
- Core Context model
- NutritionState
- NutritionState builder
- Meal-window calculation
- Nutrition completion policy
- Diet preference filtering
- Recommendation scoring
- Dynamic recommendation reasons
- Dashboard AI Pick
- Dashboard Top AI Picks
- Menu and restaurant data
- Meal-type-aware menu filtering
- Continuous calorie-fit scoring
- Breakfast / Lunch / Dinner / Snack menu data

The live recommendation path now uses the centralized nutrition state for important nutrition decisions.

---

# 6. CURRENT CORE CONTEXT

Current Context implementation:

`app/core/context/models.py`

Current Context carries:

- user_id
- goal
- meal_window
- remaining_calories
- remaining_protein
- remaining_carbs
- remaining_fat
- remaining_fiber
- steps
- calories_burned
- workout_today
- breakfast_logged
- lunch_logged
- dinner_logged
- health_connected

The Context is the central representation of the user's current state.

---

# 7. CURRENT NUTRITION STATE

Current implementation:

`app/core/state/nutrition_state.py`

`NutritionState` represents:

- remaining_calories
- remaining_protein
- remaining_carbs
- remaining_fat
- remaining_fiber
- meal_window
- goal

It is constructed from the Core `Context`.

Current direction:

**Context → NutritionState → Policy / Recommendation**

The recommendation layer receives this centralized state instead of independently reconstructing nutrition gaps.

---

# 8. CURRENT NUTRITION CALCULATION

Today's nutrition state is derived from:

- user's daily nutrition targets
- today's `meal_logs`

Conceptually:

```text
remaining_calories =
    daily_calories - consumed_calories

remaining_protein =
    daily_protein - consumed_protein

remaining_carbs =
    daily_carbs - consumed_carbs

remaining_fat =
    daily_fat - consumed_fat

remaining_fiber =
    daily_fiber - consumed_fiber