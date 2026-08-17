# NutritionOS — Project State

## Project

NutritionOS Backend

## Repository

C:\Users\Admin\NutritionOS-Backend

## GitHub Repository

https://github.com/Pushpak005/NutritionOS-Backend

## Current Branch

main

## Git Status

- Working tree clean
- GitHub is up to date
- Latest checkpoint has been committed and pushed
- Current code is safely backed up in GitHub

## Latest Checkpoint

Commit:

`f73ad7d`

Message:

`Use centralized nutrition state builder`

---

# Current Architecture

## Core Context System

Current active context architecture:

app/core/context/

- context_factory.py
- models.py
- time_context.py

The active context path is:

ContextFactory
→ Context

CoreService uses:

CoreService().get_context(user_id)

---

# Context Model

Current Context contains:

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

ContextFactory is the active builder.

---

# Nutrition State

Current:

app/core/state/nutrition_state.py

NutritionState contains:

- remaining_calories
- remaining_protein
- remaining_carbs
- remaining_fat
- remaining_fiber
- meal_window
- goal

The file provides:

build_nutrition_state(context)

which converts:

Context
→ NutritionState

This conversion is now used by the live recommendation service.

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

Future health/device providers are not considered implemented until verified.

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

Current active context path:

app.core.context

---

# Nutrition Policy

Current:

app/core/policies/nutrition_policy.py

The nutrition completion rule is now centralized in:

can_recommend_full_meal(state)

Current rule:

If:

remaining_calories <= 100

AND

remaining_protein <= 0

then:

can_recommend_full_meal() = False

Otherwise:

can_recommend_full_meal() = True

This policy is deterministic.

The recommendation service consumes this policy rather than duplicating the completion calculation.

---

# Meal Policy

Current:

app/core/policies/meal_policy.py

The file currently exists but has not yet been integrated into the active recommendation decision path.

Do not assume meal policy functionality is implemented until verified.

---

# Recommendation Architecture

Main files:

app/services/recommendation_engine.py

app/services/recommendation_service.py

Current recommendation flow:

user/profile context
→ meal target calculation
→ build NutritionState from Core Context
→ nutrition completion policy
→ load available dishes
→ diet preference filtering
→ nutrition scoring
→ recommendation explanation
→ ranking
→ best/top recommendations

---

# Recommendation State Integration

The recommendation service previously reconstructed NutritionState manually from the recommendation dictionary.

That duplication has now been removed.

Current flow:

DashboardService
→ core_context
→ recommendation_context
→ RecommendationService
→ build_nutrition_state(core_context)
→ NutritionState
→ nutrition policy

This means the recommendation policy now receives the centralized Context-derived nutrition state.

---

# Meal Target Engine

Current:

app/services/meal_engine.py

Meal allocation:

- Breakfast = 25% of daily calories
- Lunch = 35%
- Dinner = 30%
- Snack = 10%

The meal engine itself supports meal-specific targets.

Current known limitation:

The recommendation path has only recently been connected to the dynamic meal window and requires further verification across:

- Breakfast
- Lunch
- Snack
- Dinner
- Late Night

Do not mark full meal-window-aware recommendation behavior as completed until runtime tests verify it.

---

# Current Meal Window Engine

Current:

app/core/context/time_context.py

Current time windows:

- 05:00–10:59 → Breakfast
- 11:00–15:59 → Lunch
- 16:00–18:59 → Snack
- 19:00–22:59 → Dinner
- otherwise → Late Night

The ContextFactory provides the current meal window through Context.

---

# Recommendation Engine

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

Current:

app/services/recommendation_service.py

Main functions:

_get_scored_recommendations()

get_best_recommendation()

get_top_recommendations()

Current behavior:

1. receives user/profile/nutrition context
2. determines meal window
3. calculates meal target calories
4. builds NutritionState from core_context
5. applies nutrition completion policy
6. loads available dishes
7. applies diet preference filtering
8. calculates nutrition score
9. generates recommendation reasons
10. builds recommendation objects
11. sorts by score
12. returns best/top recommendations

---

# Dashboard Architecture

Current:

app/services/dashboard_service.py

The dashboard currently gathers:

1. user profile
2. today's nutrition totals
3. remaining nutrition
4. nutrition completion state
5. recommendation context
6. today's best AI pick
7. top AI picks

The dashboard obtains authoritative remaining nutrition from:

CoreService
→ ContextFactory
→ Context

The recommendation context includes:

- profile
- consumed
- remaining
- meal_window
- core_context

The recommendation service now uses:

core_context

to build NutritionState.

---

# Verified Core Tests

Test user:

`user_id = 23`

Previously verified:

ContextFactory test passed.

CoreService test passed.

ManualProvider test passed.

NutritionState test passed.

DashboardService import passed.

DashboardService test passed.

Core Context remaining nutrition matched DashboardService remaining nutrition:

- Calories: TRUE
- Protein: TRUE
- Carbs: TRUE
- Fat: TRUE
- Fiber: TRUE

---

# Verified Recommendation Regression Test

After the centralized NutritionState refactor:

Core Meal Window:

`Lunch`

Core Remaining Calories:

`1897.0`

Dashboard AI Pick:

`Tofu Teriyaki Bowl 134`

Dashboard Score:

`89`

Dashboard Top Picks:

`5`

This exactly matched the previous known-good recommendation output.

Therefore:

Context-derived NutritionState integration passed regression testing.

---

# Nutrition Completion Test

Known completed-state behavior:

When the user has effectively completed today's calorie and protein targets:

nutrition policy returns:

`False`

Recommendation service returns:

no normal full-meal recommendations.

Dashboard behavior for the previously verified completed state:

today_ai_pick = None

top_ai_picks = []

This behavior is intentional.

---

# Current Test States

Maintain test states representing:

## State A — Under Target

Normal recommendations should appear.

## State B — Near Target

Recommendations should fit the remaining nutrition budget.

## State C — Completed Target

No normal full-meal recommendation should appear.

## State D — Protein Deficient

Higher-protein options should rank higher.

## State E — Vegetarian

Non-vegetarian dishes must be filtered.

## State F — Different Meal Windows

Breakfast/Lunch/Snack/Dinner should use the appropriate meal target.

## State G — Activity Adjusted

Future state once activity integration becomes active.

---

# Current Development Priority

The major engineering objective is:

Unify the existing:

nutrition state
+
context
+
policy
+
recommendation

architecture.

Priority sequence:

1. Make meal window a real input to recommendation decisions.
2. Move nutrition completion / hard constraints toward the policy layer.
3. Make recommendation scoring consume centralized nutrition state.
4. Avoid duplicated nutrition calculations.
5. Verify the complete flow with multiple user states.
6. Only then expand activity/health-provider inputs.
7. Then improve AI explanation and conversational behavior.

---

# Current Completed Architectural Work

1. Core Context architecture established.
2. ContextFactory working.
3. Context model updated with remaining nutrition fields.
4. ManualProvider working.
5. CoreService working.
6. NutritionState working.
7. build_nutrition_state(Context) implemented.
8. Legacy context pipeline isolated.
9. DashboardService working.
10. Dashboard remaining nutrition verified against Core Context.
11. Recommendation engine working.
12. Recommendation scoring and explanations verified.
13. Nutrition completion policy created.
14. RecommendationService integrated with nutrition policy.
15. RecommendationService integrated with centralized build_nutrition_state().
16. Recommendation regression test passed.
17. Git checkpoint created.
18. GitHub checkpoint pushed.
19. Working tree clean.

---

# Current Known Limitations

1. Meal-window-aware recommendation behavior still requires explicit multi-window runtime verification.

2. meal_policy.py exists but is not yet integrated into the active recommendation decision path.

3. Recommendation scoring still primarily consumes the legacy user dictionary rather than a completely state-native scoring contract.

4. Activity data remains prototype/manual.

5. Health/device connection remains prototype/manual.

6. Real external health providers are not yet integrated.

7. Meal quantity handling requires continued verification.

8. Recommendation scoring still needs policy-level refinement beyond basic nutrition matching.

9. Hard constraints and soft ranking preferences need clearer separation.

10. The project needs a canonical policy layer so business rules do not become scattered across dashboard, recommendation and router code.

---

# Development Workflow

## GitHub-First Rule

GitHub is the primary implementation inspection source.

Before proposing a code change:

1. Inspect the current GitHub main branch.
2. Check the relevant project Source of Truth.
3. Identify the actual current implementation.
4. Identify ONE next controlled change.
5. Do not ask the user to paste full files that can be inspected from GitHub.

Use VS Code/local PowerShell for:

- editing
- execution
- testing
- runtime verification
- local git operations

---

# Standard Development Cycle

GitHub inspect

↓

Identify ONE next change

↓

Give ONE exact VS Code / PowerShell action

↓

User runs it

↓

Verify output

↓

Provide complete replacement file when code changes are required

↓

User saves

↓

Compile/test

↓

git diff

↓

git status

↓

git add

↓

git commit

↓

git push origin main

↓

git status must be clean

↓

Re-check GitHub

↓

Identify next ONE change

↓

Repeat

---

# Git Commands

After a successful tested change:

git status

git add <file>

git commit -m "<message>"

git push origin main

git status

Expected final state:

nothing to commit, working tree clean

---

# Important Development Rules

Do not:

- hard-code individual dish recommendations
- use popularity as the primary nutrition decision
- let an LLM override deterministic nutrition constraints
- duplicate nutrition calculations unnecessarily
- bypass the nutrition event model
- treat future integrations as implemented
- mix UI concerns into core nutrition policy
- silently change database semantics
- remove working behavior without verifying downstream impact

Do:

- keep nutrition events as state-changing events
- centralize nutrition state
- keep policy deterministic
- keep ranking explainable
- keep providers replaceable
- test every major state transition
- preserve backward compatibility where practical
- verify changes through real database/runtime tests

---

# Code Change Rule

Whenever modifying a project file:

Provide the COMPLETE replacement file.

Do not provide only a partial snippet when the user is expected to replace a file.

Always provide the exact PowerShell command needed to verify the change.

Always verify before moving to the next architectural step.

---

# Chat Continuation Rule

When a ChatGPT conversation becomes large or slow:

Start a new chat inside the same NutritionOS project.

Use:

"Continue NutritionOS from PROJECT_STATE.md.

Inspect the current GitHub main branch before making assumptions.

Use the project Source of Truth for architectural intent.

Do not ask me to paste the entire codebase.

Work one step at a time using the GitHub → VS Code → test → diff → commit → push → clean → GitHub cycle."

---

# Current Checkpoint

Latest verified commit:

`f73ad7d`

Commit message:

`Use centralized nutrition state builder`

Latest verified dashboard regression:

Core Meal Window: Lunch

Core Remaining Calories: 1897.0

Dashboard AI Pick: Tofu Teriyaki Bowl 134

Dashboard Score: 89

Dashboard Top Picks: 5

Working tree:

clean

GitHub:

up to date

---

# Immediate Next Engineering Task

Before changing additional recommendation logic:

Inspect the current GitHub implementations of:

- app/core/context/time_context.py
- app/services/meal_engine.py
- app/services/recommendation_service.py
- app/services/recommendation_engine.py
- app/core/policies/meal_policy.py

Then implement and verify the next controlled step toward:

Context
→ NutritionState
→ Meal Policy
→ Nutrition Policy
→ Recommendation Ranking

The immediate target is explicit meal-window-aware recommendation behavior.

Do not refactor the entire recommendation engine at once.

Work incrementally and preserve the current verified dashboard behavior.