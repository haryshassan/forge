#!/usr/bin/env python3
"""Add session structure rules to the plan generation prompt."""

with open('forge.html', 'r', encoding='utf-8') as f:
    content = f.read()

OLD = """For every single exercise in every plan the notes field must explain in one specific sentence why this exercise was chosen for this person's exact goal, experience level, and how it fits into the session. The notes must reference the science — mention mechanical tension, stretch stimulus, progressive overload, metabolic demand, power transfer, or whatever principle applies. Never write a generic notes entry. It must be specific to this person.

EQUIPMENT AWARENESS:"""

NEW = """For every single exercise in every plan the notes field must explain in one specific sentence why this exercise was chosen for this person's exact goal, experience level, and how it fits into the session. The notes must reference the science — mention mechanical tension, stretch stimulus, progressive overload, metabolic demand, power transfer, or whatever principle applies. Never write a generic notes entry. It must be specific to this person.

SESSION STRUCTURE — NON-NEGOTIABLE:
Every session must follow this exact structure order without exception:

1. ONE PRIMARY COMPOUND MOVEMENT opens the session. This is the heaviest and most technically demanding exercise. It is performed first when the athlete is freshest. Only one barbell compound movement per session — never programme squat and deadlift in the same session, never bench press and overhead press in the same session. Pick one primary and build the entire session around it.

2. ONE OR TWO SECONDARY MOVEMENTS that support the primary. Either a variation of the same pattern or a complementary pattern. If the primary is squat, secondary could be leg press or hack squat. If the primary is bench press, secondary could be incline dumbbell press. Never use two primary-level barbell compounds as primary and secondary.

3. ISOLATION AND ACCESSORY WORK targeting the specific muscles of that session — always performed last, in order from largest to smallest movement.

SESSION TYPE TEMPLATES — apply the correct template for each session:

Leg sessions: Primary is ONE of either a squat pattern OR a hip hinge — never both. Then one quad-specific exercise (leg press, hack squat, leg extension, or Bulgarian split squat). Then one hamstring-specific exercise (Romanian deadlift, lying leg curl, seated leg curl, or Nordic curl — but only if not already used as primary). Then one calf exercise (standing calf raise, seated calf raise, or leg press calf raise). Maximum 4-5 exercises total. Never programme squat and deadlift together, never squat and Romanian deadlift together — both are too taxing on the same session.

Push sessions / chest days: Primary is one horizontal push (flat barbell bench or flat dumbbell press). Secondary is one incline push (incline dumbbell or incline barbell). Then one chest isolation (cable fly, pec deck, or dumbbell fly). Then one shoulder movement (lateral raise, or overhead press only if not already used as primary). Then one tricep exercise (pushdown, overhead extension, or skull crusher). Maximum 5 exercises.

Pull sessions / back days: Primary vertical pull (pull up or lat pulldown). Primary horizontal pull (barbell row, dumbbell row, seated cable row, or chest supported row). One rear delt exercise (face pull, rear delt fly, or reverse pec deck). One bicep exercise (barbell curl, dumbbell curl, or cable curl). One trap exercise if not already covered (shrug or rack pull). Maximum 5 exercises.

Shoulder sessions: Primary overhead press (barbell or dumbbell). One lateral raise (cable or dumbbell). One rear delt exercise (face pull or rear delt fly). One trap exercise (shrug). Optional one more isolation. Maximum 4-5 exercises.

Arm sessions: Two bicep exercises — one compound curl (barbell curl or incline dumbbell curl) and one isolation (cable curl or hammer curl). Two tricep exercises — one overhead (skull crusher or overhead extension) and one pushdown variation. Optional forearm work. Maximum 5 exercises.

Upper body sessions: Follow push plus pull structure — one push compound, one pull compound, supporting isolation for both. Keep pushing and pulling volume balanced.

ADDITIONAL STRUCTURAL RULES — apply to every session:
Never programme the same movement pattern twice as primary and secondary — one squat variation is enough, one hinge is enough, one horizontal push is enough.
Always order accessory and isolation exercises from largest to smallest at the end.
Rest periods must match the exercise — 2-3 minutes after the primary compound, 90 seconds after secondary movements, 60 seconds after isolation work.
For athletic performance goals programme one explosive movement BEFORE the primary compound — box jump, broad jump, or medicine ball throw depending on equipment. This does not count toward the exercise total.
Session length must be strictly respected — if the athlete has 45 minutes do not programme 6 exercises with 3-minute rest periods. Calculate realistic session time and cut exercises if needed.

EQUIPMENT AWARENESS:"""

assert OLD in content, "Anchor text not found"
content = content.replace(OLD, NEW)

with open('forge.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. Total lines:", content.count('\n'))
print("Session structure rules present:", "SESSION STRUCTURE — NON-NEGOTIABLE" in content)
print("Leg template present:", "Leg sessions:" in content)
print("Push template present:", "Push sessions / chest days:" in content)
print("Pull template present:", "Pull sessions / back days:" in content)
print("Equipment awareness still present:", "EQUIPMENT AWARENESS:" in content)
print("Notes rule still present:", "Never write a generic notes entry" in content)
