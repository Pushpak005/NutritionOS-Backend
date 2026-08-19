# NutritionOS — PROJECT STATE

**Last Updated:** 19 August 2026  
**Status:** Prototype — Finalization Phase  
**Product:** Autonomous Nutrition Operating System

---

# 1. PRODUCT GOAL

NutritionOS is a state-aware nutrition decision system.

The core product loop is:

User
→ Nutrition Targets
→ Current Nutrition State
→ Current Meal Window
→ Policy
→ Recommendation Ranking
→ Explanation
→ User Action
→ Updated Nutrition State

The prototype must demonstrate that recommendations are based on the user's current nutrition state and constraints rather than popularity alone.

The long-term vision is an autonomous nutrition operating system that continuously understands the user's changing nutrition state and makes increasingly context-aware decisions.

For the prototype, however, the priority is a reliable closed decision loop rather than maximum feature count.

---

# 2. SOURCE-OF-TRUTH RULE

When reasoning about or modifying NutritionOS, use this priority:

1. Actual source code
2. Verified runtime / API behavior
3. Current database state
4. This PROJECT_STATE.md
5. Historical project documents
6. Future ideas / roadmap

If documentation and implementation disagree:

**Inspect the code and runtime first.**

Never silently invent an implementation.

Never describe planned functionality as implemented.

---

# 3. CURRENT REPOSITORIES

## Backend

Path:

`C:\Users\Admin\NutritionOS-Backend`

Repository:

`Pushpak005/NutritionOS-Backend`

Technology:

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL / Supabase

Main areas:

- `app/core`
- `app/services`
- `app/routers`
- `app/database`
- `app/utils`

---

## Frontend

Path:

`C:\Users\Admin\NutritionOS-Frontend`

Technology:

- React
- Vite
- React Router
- Axios

Important areas:

- dashboard
- meal service
- my meals
- API client
- recommendation cards

---

# 4. CURRENT ARCHITECTURE

The intended decision pipeline is:

```text
Database / Nutrition Events
          ↓
       Context
          ↓
   NutritionState
          ↓
        Policy
          ↓
 Recommendation Ranking
          ↓
     Explanation
          ↓
      User Action
          ↓
   Nutrition Event
          ↓
 Updated Nutrition State
