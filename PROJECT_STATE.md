# NutritionOS — PROJECT SOURCE OF TRUTH

**Baseline:** 17 August 2026  
**Status:** Active Development  
**Product:** Autonomous Nutrition Operating System

---

## 1. WHAT NUTRITIONOS IS

NutritionOS is a state-aware nutrition system.

It should understand:

**User → Targets → Meals → Current Nutrition State → Decision → Recommendation → User Action → Updated State**

The recommendation must be based on the user's current nutrition state, not popularity alone.

---

## 2. CURRENT STACK

### Frontend
- React
- Vite
- React Router
- Axios
- `C:\Users\Admin\NutritionOS-Frontend`

### Backend
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL / Supabase
- `C:\Users\Admin\NutritionOS-Backend`

### Core backend areas
- `app/core`
- `app/services`
- `app/routers`
- `app/database`

---

## 3. CURRENTLY WORKING

- User/profile nutrition targets
- Meal logging and nutrition events
- Today's consumed/remaining nutrition
- `ContextFactory`
- `NutritionState`
- Meal-window calculation
- Recommendation scoring
- Nutrition completion guard
- Diet filtering
- Recommendation explanations
- Dashboard AI Pick / Top AI Picks
- Frontend dashboard
- Menu/restaurant data
- `meal_type` data including Breakfast, Lunch, Dinner and Snack

The dashboard has been runtime-tested and is currently rendering correctly.

---

## 4. CURRENT ARCHITECTURE

The intended decision flow is:

**Database / Events**
→ **Context**
→ **NutritionState**
→ **Policy**
→ **Ranking**
→ **Explanation**
→ **User Action**
→ **New Event**

### Responsibilities

**Context / State**
- What is true about the user right now?

**Policy**
- What is allowed / appropriate?

**Ranking**
- Which available dish is best?

**Explanation**
- Why was it selected?

Deterministic nutrition logic remains authoritative. LLMs must not override nutrition constraints.

---

## 5. CURRENT DEVELOPMENT FOCUS

### A. Core Nutrition Decision System — CURRENT
Unify:
- Context
- NutritionState
- Meal Window
- Policy
- Recommendation

Make the live recommendation path use **one authoritative nutrition state**.

### B. Nutrition Intelligence
After A:
- better macro balancing
- meal timing
- adaptive nutrition targets

### C. Activity + Health
After B:
- steps
- workouts
- calories burned
- Health Connect / other providers

### D. Autonomous System
After C:
- continuous state updates
- adaptive recommendations
- event-driven actions
- proactive nutrition decisions

### E. Conversational AI
After D:
- natural-language nutrition assistant
- explanations
- planning
- adaptive interaction

---

## 6. IMMEDIATE NEXT TASK

**Complete meal-window-aware recommendation decisions.**

Make the live recommendation flow correctly use:

Breakfast / Lunch / Snack / Dinner

The meal window must influence:
- meal calorie target
- eligible dishes
- recommendation ranking

Then verify that one centralized NutritionState is used throughout policy and recommendation scoring.

Do not add unnecessary database fields.

After completion:
Verify → update this file → commit → push GitHub.

---

## 7. TEST CHECKPOINT

Every major change should verify:

1. Under target → recommendations appear
2. Near target → appropriate options
3. Completed target → no normal full-meal recommendation
4. Protein deficient → protein-rich options rank higher
5. Vegetarian → non-veg filtered
6. Breakfast/Lunch/Snack/Dinner → correct meal-window behavior

---

## 8. NON-NEGOTIABLES

- Do not hard-code dish recommendations.
- Do not use popularity as the primary nutrition decision.
- Do not let LLMs override deterministic nutrition rules.
- Do not duplicate nutrition calculations unnecessarily.
- Keep nutrition events state-changing.
- Keep policy deterministic and explainable.
- Keep providers replaceable.
- Verify changes with real runtime/database tests.
- Do not remove working behavior without checking callers.
- Do not treat planned features as implemented.

---

## 9. DEVELOPMENT RULE

Work **one major task at a time**:

**Inspect → Change → Test → Verify → Update this file → Push changes to GitHub → Move to next task.**

After **every completed task**, we must:
1. Verify the change with real runtime/database tests.
2. Update this Source of Truth with the new status.
3. Commit and **push the completed changes to GitHub**.
4. Only then move to the next major task.

This Source of Truth itself must also be kept in GitHub and updated/pushed whenever its status changes.

For code changes, provide the **complete replacement file** rather than partial snippets unless explicitly requested otherwise.

---

## 10. SOURCE-OF-TRUTH RULE

Priority:

1. Actual source code + verified runtime
2. Current database
3. This file
4. Historical documents
5. Future ideas

If documentation and code disagree, inspect and verify the code before changing architecture.

