#!/usr/bin/env python3
"""5-part injury/physio feature implementation."""

with open('forge.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ════════════════════════════════════════════════════════════════════
# PART 1a — Add currentInjuries and physioExercises to QUESTIONS
# ════════════════════════════════════════════════════════════════════
# Find the exact limitations line from the file
lim_idx = content.find("    { id:'limitations',")
assert lim_idx != -1, "limitations question not found"
lim_end = content.find('\n', lim_idx) + 1  # end of limitations line (includes newline)
lifestyle_line_start = content.find("    { id:'lifestyle',", lim_end)
lifestyle_line_end = content.find('\n', lifestyle_line_start) + 1

OLD_Q = content[lim_idx:lifestyle_line_start]  # limitations line up to but not including lifestyle
new_questions = (
    "    { id:'currentInjuries', text:\"Do you have any current injuries I need to know about? Even minor ones affect how I programme your training.\","
    "                                                                                                                                                                         "
    "type:'text',       placeholder:'e.g. Left shoulder impingement, right knee pain…', skippable:true },\n"
    "    { id:'physioExercises', text:\"Has a physiotherapist, doctor, or specialist given you any specific exercises to do? I will include them in your programme.\","
    "                                                                                                                                                                           "
    "type:'text',       placeholder:'e.g. Clamshells, banded monster walks, dead bugs…', skippable:true },\n"
)
NEW_Q = OLD_Q + new_questions

assert OLD_Q in content, "QUESTIONS anchor not found"
content = content.replace(OLD_Q, NEW_Q, 1)
print("Part 1a done: currentInjuries and physioExercises questions added")

# ════════════════════════════════════════════════════════════════════
# PART 1b — Make handleSkip generic
# ════════════════════════════════════════════════════════════════════
OLD_SKIP = """  const handleSkip = () => {
    const newAnswers = { ...answers, limitations:'' };
    setAnswers(newAnswers);
    setMessages(prev => [...prev, { role:'user', text:'No limitations' }]);
    setInputText('');
    const nextIdx = currentQ + 1;
    setCurrentQ(nextIdx);
    setTimeout(() => setMessages(prev => [...prev, { role:'coach', text:QUESTIONS[nextIdx].text }]), 300);
  };"""

NEW_SKIP = """  const handleSkip = () => {
    const qId = QUESTIONS[currentQ].id;
    const skipLabel = qId === 'limitations' ? 'No limitations' : qId === 'currentInjuries' ? 'No current injuries' : 'None specified';
    const newAnswers = { ...answers, [qId]: '' };
    setAnswers(newAnswers);
    setMessages(prev => [...prev, { role:'user', text:skipLabel }]);
    setInputText('');
    const nextIdx = currentQ + 1;
    if (nextIdx >= QUESTIONS.length) {
      buildRecommendation(newAnswers);
      return;
    }
    setCurrentQ(nextIdx);
    setTimeout(() => setMessages(prev => [...prev, { role:'coach', text:QUESTIONS[nextIdx].text }]), 300);
  };"""

assert OLD_SKIP in content, "handleSkip anchor not found"
content = content.replace(OLD_SKIP, NEW_SKIP)
print("Part 1b done: handleSkip is now generic")

# ════════════════════════════════════════════════════════════════════
# PART 1c — Add currentInjuries and physioExercises to handleConfirm
# ════════════════════════════════════════════════════════════════════
OLD_CONFIRM = "      limitations:         answers.limitations || '',\n      lifestyle:           answers.lifestyle || '',"

NEW_CONFIRM = "      limitations:         answers.limitations || '',\n      currentInjuries:     answers.currentInjuries || '',\n      physioExercises:     answers.physioExercises || '',\n      lifestyle:           answers.lifestyle || '',"

assert OLD_CONFIRM in content, "handleConfirm anchor not found"
content = content.replace(OLD_CONFIRM, NEW_CONFIRM)
print("Part 1c done: handleConfirm updated")

# ════════════════════════════════════════════════════════════════════
# PART 1d — Update buildRecommendation recPrompt
# ════════════════════════════════════════════════════════════════════
OLD_REC = "Limitations: ${finalAnswers.limitations || 'None'}. Sleep/stress: ${finalAnswers.lifestyle}."
NEW_REC = "Limitations: ${finalAnswers.limitations || 'None'}. Current injuries: ${finalAnswers.currentInjuries || 'None'}. Physio exercises: ${finalAnswers.physioExercises || 'None'}. Sleep/stress: ${finalAnswers.lifestyle}."

assert OLD_REC in content, "buildRecommendation recPrompt anchor not found"
content = content.replace(OLD_REC, NEW_REC)
print("Part 1d done: buildRecommendation recPrompt updated")

# ════════════════════════════════════════════════════════════════════
# PART 2 — Add physio/injury rules to plan generation prompt
# ════════════════════════════════════════════════════════════════════
OLD_PLAN = "SESSION LENGTH TARGETS:\n30 minutes — 3 to 4 exercises, minimal rest."

NEW_PLAN = """PHYSIO AND INJURY MANAGEMENT:
If the athlete has listed physio prescribed exercises, include them at the START of every session as a dedicated block. List each physio exercise first in the workouts array with the exercise name exactly as specified, sets:2, reps:"12-15", rest:"30s", and notes:"Physiotherapist prescribed — perform before every session." These exercises are mandatory and non-negotiable.

If the athlete has listed current injuries, never programme any exercise that directly loads the injured structure. Substitute every conflicting exercise with a safe alternative. If shoulder injury: avoid overhead pressing, upright rows, behind-neck movements — substitute with cable flyes, push-ups, neutral grip pressing. If knee pain: avoid full depth squats and heavy lunges — substitute with box squats, step-ups, or leg press with limited range. If lower back pain: avoid conventional deadlifts, bent-over barbell rows, good mornings — substitute with trap bar deadlift, light RDL, seated cable row, or chest supported row. Always note the injury accommodation in the exercise notes field.

SESSION LENGTH TARGETS:
30 minutes — 3 to 4 exercises, minimal rest."""

assert OLD_PLAN in content, "plan SESSION LENGTH TARGETS anchor not found"
content = content.replace(OLD_PLAN, NEW_PLAN)
print("Part 2 done: physio/injury rules added to plan generation prompt")

# ════════════════════════════════════════════════════════════════════
# PART 3a — Extend parsePlanChange to handle PROFILE_UPDATE
# ════════════════════════════════════════════════════════════════════
OLD_PARSE = """function parsePlanChange(text) {
  const marker = 'PLAN_CHANGE_SUGGESTED:';
  const idx = text.indexOf(marker);
  if (idx === -1) return { displayText: text, planChange: null };
  const displayText = text.slice(0, idx).trim();
  try {
    const planChange = JSON.parse(text.slice(idx + marker.length).trim());
    return { displayText, planChange };
  } catch {
    return { displayText, planChange: null };
  }
}"""

NEW_PARSE = """function parsePlanChange(text) {
  let workingText = text;
  let profileUpdate = null;
  const puMarker = 'PROFILE_UPDATE:';
  const puIdx = workingText.indexOf(puMarker);
  if (puIdx !== -1) {
    const beforePU = workingText.slice(0, puIdx).trim();
    try { profileUpdate = JSON.parse(workingText.slice(puIdx + puMarker.length).trim()); } catch {}
    workingText = beforePU;
  }
  const marker = 'PLAN_CHANGE_SUGGESTED:';
  const idx = workingText.indexOf(marker);
  if (idx === -1) return { displayText: workingText, planChange: null, profileUpdate };
  const displayText = workingText.slice(0, idx).trim();
  try {
    const planChange = JSON.parse(workingText.slice(idx + marker.length).trim());
    return { displayText, planChange, profileUpdate };
  } catch {
    return { displayText: workingText, planChange: null, profileUpdate };
  }
}"""

assert OLD_PARSE in content, "parsePlanChange anchor not found"
content = content.replace(OLD_PARSE, NEW_PARSE)
print("Part 3a done: parsePlanChange extended with PROFILE_UPDATE")

# ════════════════════════════════════════════════════════════════════
# PART 3b — Add CoachProfileUpdateCard component after PlanChangeCard
# ════════════════════════════════════════════════════════════════════
OLD_AFTER_CARD = """/* ═══════════════════════════════════════════════
   COACH SCREEN
═══════════════════════════════════════════════ */"""

NEW_AFTER_CARD = """function CoachProfileUpdateCard({ profileUpdate, onApply, onDismiss }) {
  const fields = Object.entries(profileUpdate).filter(([k]) => k !== 'reason').filter(([,v]) => v);
  return (
    <div style={{ borderLeft:'3px solid #0A84FF', background:'#1A1A1C', borderRadius:16, padding:'14px 16px', margin:'8px 0 4px 0' }}>
      <p style={{ fontFamily:"'Bebas Neue',sans-serif", color:'#0A84FF', fontSize:13, letterSpacing:'0.08em', marginBottom:6 }}>
        PROFILE UPDATE SUGGESTED
      </p>
      {profileUpdate.reason && (
        <p style={{ color:'#8A8A8E', fontSize:12, marginBottom:8, fontFamily:"'DM Sans',sans-serif" }}>{profileUpdate.reason}</p>
      )}
      {fields.map(([k,v]) => (
        <p key={k} style={{ color:'#F5F5F0', fontSize:13, lineHeight:1.5, fontFamily:"'DM Sans',sans-serif", marginBottom:4 }}>
          <span style={{ color:'#8A8A8E' }}>{k === 'currentInjuries' ? 'Current injuries' : k === 'physioExercises' ? 'Physio exercises' : k}: </span>{String(v)}
        </p>
      ))}
      <div style={{ display:'flex', gap:8, marginTop:10 }}>
        <button onClick={onApply}
          style={{ flex:1, padding:'10px 0', borderRadius:12, background:'#0A84FF', color:'#fff', fontFamily:"'Bebas Neue',sans-serif", fontSize:14, letterSpacing:'0.05em', border:'none', cursor:'pointer' }}>
          UPDATE PROFILE
        </button>
        <button onClick={onDismiss}
          style={{ flex:1, padding:'10px 0', borderRadius:12, background:'#252527', color:'#8A8A8E', fontFamily:"'Bebas Neue',sans-serif", fontSize:14, letterSpacing:'0.05em', border:'1px solid #3A3A3C', cursor:'pointer' }}>
          DISMISS
        </button>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════
   COACH SCREEN
═══════════════════════════════════════════════ */"""

assert OLD_AFTER_CARD in content, "CoachScreen section header anchor not found"
content = content.replace(OLD_AFTER_CARD, NEW_AFTER_CARD)
print("Part 3b done: CoachProfileUpdateCard added")

# ════════════════════════════════════════════════════════════════════
# PART 3c — Add onProfileUpdate to CoachScreen signature
# ════════════════════════════════════════════════════════════════════
OLD_SIG = "function CoachScreen({ coachCheckins, profile, plan, logs, prs, streak,\n  nutritionLog, nutritionGoals, weightHistory, cardioLog, badges, onPlanUpdate }) {"
NEW_SIG = "function CoachScreen({ coachCheckins, profile, plan, logs, prs, streak,\n  nutritionLog, nutritionGoals, weightHistory, cardioLog, badges, onPlanUpdate, onProfileUpdate=()=>{} }) {"

assert OLD_SIG in content, "CoachScreen signature anchor not found"
content = content.replace(OLD_SIG, NEW_SIG)
print("Part 3c done: onProfileUpdate prop added to CoachScreen")

# ════════════════════════════════════════════════════════════════════
# PART 3d — Add pendingProfileUpdates state
# ════════════════════════════════════════════════════════════════════
OLD_STATE = "  const [pendingPlanChanges, setPendingPlanChanges] = useState({});"
NEW_STATE = "  const [pendingPlanChanges, setPendingPlanChanges] = useState({});\n  const [pendingProfileUpdates, setPendingProfileUpdates] = useState({});"

assert OLD_STATE in content, "pendingPlanChanges state anchor not found"
content = content.replace(OLD_STATE, NEW_STATE)
print("Part 3d done: pendingProfileUpdates state added")

# ════════════════════════════════════════════════════════════════════
# PART 3e — Add handleApplyProfileUpdate and handleDismissProfileUpdate
# ════════════════════════════════════════════════════════════════════
OLD_KEEP = """  const handleKeepPlanChange = (cardKey) => {
    setMessages(m => [...m, { role:'assistant', content:`No problem — keeping your current plan as is.` }].slice(-50));
    setPendingPlanChanges(prev => { const n = {...prev}; delete n[cardKey]; return n; });
  };

  /* ── Send message ── */"""

NEW_KEEP = """  const handleKeepPlanChange = (cardKey) => {
    setMessages(m => [...m, { role:'assistant', content:`No problem — keeping your current plan as is.` }].slice(-50));
    setPendingPlanChanges(prev => { const n = {...prev}; delete n[cardKey]; return n; });
  };

  const handleApplyProfileUpdate = (profileUpdate, cardKey) => {
    const updated = { ...profile };
    if (profileUpdate.currentInjuries !== undefined) updated.currentInjuries = profileUpdate.currentInjuries;
    if (profileUpdate.physioExercises !== undefined) updated.physioExercises = profileUpdate.physioExercises;
    if (profileUpdate.limitations !== undefined) updated.limitations = profileUpdate.limitations;
    onProfileUpdate(updated);
    setMessages(m => [...m, { role:'assistant', content:'Profile updated. I have noted your injury and will factor it into all future advice.' }].slice(-50));
    setPendingProfileUpdates(prev => { const n = {...prev}; delete n[cardKey]; return n; });
  };

  const handleDismissProfileUpdate = (cardKey) => {
    setPendingProfileUpdates(prev => { const n = {...prev}; delete n[cardKey]; return n; });
  };

  /* ── Send message ── */"""

assert OLD_KEEP in content, "handleKeepPlanChange anchor not found"
content = content.replace(OLD_KEEP, NEW_KEEP)
print("Part 3e done: handleApplyProfileUpdate and handleDismissProfileUpdate added")

# ════════════════════════════════════════════════════════════════════
# PART 3f — Handle profileUpdate in sendMessage response
# ════════════════════════════════════════════════════════════════════
OLD_SEND = "      const { displayText, planChange } = parsePlanChange(rawReply);\n      const msgId = `msg_${Date.now()}`;\n      setMessages(m => [...m, { role:'assistant', content:displayText, id:msgId }].slice(-50));\n      if (planChange) setPendingPlanChanges(prev => ({ ...prev, [msgId]: planChange }));"

NEW_SEND = "      const { displayText, planChange, profileUpdate } = parsePlanChange(rawReply);\n      const msgId = `msg_${Date.now()}`;\n      setMessages(m => [...m, { role:'assistant', content:displayText, id:msgId }].slice(-50));\n      if (planChange) setPendingPlanChanges(prev => ({ ...prev, [msgId]: planChange }));\n      if (profileUpdate) setPendingProfileUpdates(prev => ({ ...prev, [msgId]: profileUpdate }));"

assert OLD_SEND in content, "sendMessage response anchor not found"
content = content.replace(OLD_SEND, NEW_SEND)
print("Part 3f done: profileUpdate handled in sendMessage")

# ════════════════════════════════════════════════════════════════════
# PART 3g — Render CoachProfileUpdateCard in messages list
# ════════════════════════════════════════════════════════════════════
OLD_RENDER = """                {msg.role==='assistant' && msg.id && pendingPlanChanges[msg.id] && (
                  <div className="ml-9 mb-3">
                    <PlanChangeCard
                      planChange={pendingPlanChanges[msg.id]}
                      onApply={() => handleApplyPlanChange(pendingPlanChanges[msg.id], msg.id)}
                      onKeep={() => handleKeepPlanChange(msg.id)}
                    />
                  </div>
                )}
              </div>
            ))}

            {/* Typing indicator */}"""

NEW_RENDER = """                {msg.role==='assistant' && msg.id && pendingPlanChanges[msg.id] && (
                  <div className="ml-9 mb-3">
                    <PlanChangeCard
                      planChange={pendingPlanChanges[msg.id]}
                      onApply={() => handleApplyPlanChange(pendingPlanChanges[msg.id], msg.id)}
                      onKeep={() => handleKeepPlanChange(msg.id)}
                    />
                  </div>
                )}
                {msg.role==='assistant' && msg.id && pendingProfileUpdates[msg.id] && (
                  <div className="ml-9 mb-3">
                    <CoachProfileUpdateCard
                      profileUpdate={pendingProfileUpdates[msg.id]}
                      onApply={() => handleApplyProfileUpdate(pendingProfileUpdates[msg.id], msg.id)}
                      onDismiss={() => handleDismissProfileUpdate(msg.id)}
                    />
                  </div>
                )}
              </div>
            ))}

            {/* Typing indicator */}"""

assert OLD_RENDER in content, "message render anchor not found"
content = content.replace(OLD_RENDER, NEW_RENDER)
print("Part 3g done: CoachProfileUpdateCard rendered in messages list")

# ════════════════════════════════════════════════════════════════════
# PART 3h — Add PROFILE_UPDATE instruction to coach system prompt
# ════════════════════════════════════════════════════════════════════
OLD_PROMPT = "When the athlete reports pain, fatigue, soreness, injury, or asks to modify their plan, you may suggest specific changes. To do so, end your message with PLAN_CHANGE_SUGGESTED: followed immediately by a valid JSON object (no extra text after the JSON) with fields: reason (string), changes (array of objects each with day, exercise_to_replace, replacement_exercise, new_sets, new_reps). Only suggest a plan change when clearly warranted — not every message."

NEW_PROMPT = """When the athlete reports pain, fatigue, soreness, injury, or asks to modify their plan, you may suggest specific changes. To do so, end your message with PLAN_CHANGE_SUGGESTED: followed immediately by a valid JSON object (no extra text after the JSON) with fields: reason (string), changes (array of objects each with day, exercise_to_replace, replacement_exercise, new_sets, new_reps). Only suggest a plan change when clearly warranted — not every message.

If the athlete mentions a new injury they have not previously reported, respond normally then end your message with PROFILE_UPDATE: followed immediately by a valid JSON object with fields: reason (string), currentInjuries (string, full updated description of all known injuries). If they also mention physio prescribed exercises, include physioExercises (string) in the JSON. Only emit PROFILE_UPDATE when genuinely new injury information is disclosed — not for every mention of soreness. Never emit both PLAN_CHANGE_SUGGESTED and PROFILE_UPDATE in the same message — choose the most appropriate one."""

assert OLD_PROMPT in content, "coach system prompt PLAN_CHANGE anchor not found"
content = content.replace(OLD_PROMPT, NEW_PROMPT)
print("Part 3h done: PROFILE_UPDATE instruction added to coach system prompt")

# ════════════════════════════════════════════════════════════════════
# PART 3i — Wire onProfileUpdate in app
# ════════════════════════════════════════════════════════════════════
OLD_WIRE = "                                onPlanUpdate={setPlan}/>;"
NEW_WIRE = "                                onPlanUpdate={setPlan} onProfileUpdate={setProfile}/>;"

assert OLD_WIRE in content, "CoachScreen onPlanUpdate wire anchor not found"
content = content.replace(OLD_WIRE, NEW_WIRE)
print("Part 3i done: onProfileUpdate wired in app")

# ════════════════════════════════════════════════════════════════════
# PART 4 — Add injury/physio context to body map
# ════════════════════════════════════════════════════════════════════
OLD_BODYMAP_SYS = "      const systemPrompt = `You are a sports physiotherapist sending a quick clinical note. Keep the entire response under 120 words. Use these bold headings only, one sentence each: **What It Could Be**, **Likely Trigger**, **Before You Train**, **Avoid**, **Train Today?**. End with one short italicised sentence advising to consult a physio or doctor if it persists. Be direct. No waffle.`;"

NEW_BODYMAP_SYS = "      const systemPrompt = `You are a sports physiotherapist sending a quick clinical note. You have full context on the athlete's injury history and physio prescription — cross-reference these when interpreting the reported area. Keep the entire response under 120 words. Use these bold headings only, one sentence each: **What It Could Be**, **Likely Trigger**, **Before You Train**, **Avoid**, **Train Today?**. End with one short italicised sentence advising to consult a physio or doctor if it persists. Be direct. No waffle.`;"

assert OLD_BODYMAP_SYS in content, "body map systemPrompt anchor not found"
content = content.replace(OLD_BODYMAP_SYS, NEW_BODYMAP_SYS)

OLD_BODYMAP_MSG = "      const userMsg = `Athlete: ${profile.name||'Athlete'}, ${profile.fitnessLevel||''}, Goal: ${profile.goal||''}.\n\nAFFECTED AREAS AND SEVERITY:\n${muscleList}\n\nASSESSMENT ANSWERS:\n${qaText}\n\nCURRENT TRAINING PLAN:\n${planText}\n\nLAST 7 SESSIONS:\n${recentSessions}\n\nLAST 3 DAYS NUTRITION:\n${nutrText}`;"

NEW_BODYMAP_MSG = "      const userMsg = `Athlete: ${profile.name||'Athlete'}, ${profile.fitnessLevel||''}, Goal: ${profile.goal||''}.\n\nKNOWN INJURIES: ${profile.currentInjuries || 'None reported'}\nPHYSIO PRESCRIBED EXERCISES: ${profile.physioExercises || 'None'}\n\nAFFECTED AREAS AND SEVERITY:\n${muscleList}\n\nASSESSMENT ANSWERS:\n${qaText}\n\nCURRENT TRAINING PLAN:\n${planText}\n\nLAST 7 SESSIONS:\n${recentSessions}\n\nLAST 3 DAYS NUTRITION:\n${nutrText}`;"

assert OLD_BODYMAP_MSG in content, "body map userMsg anchor not found"
content = content.replace(OLD_BODYMAP_MSG, NEW_BODYMAP_MSG)
print("Part 4 done: injury/physio context added to body map")

# ════════════════════════════════════════════════════════════════════
# PART 5a — Add React state hooks to ProfileScreen (before isExisting check)
# ════════════════════════════════════════════════════════════════════
OLD_PROFILE_FN = "function ProfileScreen({ profile, onSave, onGeneratePlan, isExisting, onNutritionGoals=()=>{}, onLogout=()=>{}, onReset=()=>{} }) {\n  /* ── Existing profile view ── */\n  if (isExisting) {"

NEW_PROFILE_FN = """function ProfileScreen({ profile, onSave, onGeneratePlan, isExisting, onNutritionGoals=()=>{}, onLogout=()=>{}, onReset=()=>{} }) {
  const [injuryText, setInjuryText] = React.useState(profile.currentInjuries || '');
  const [physioText, setPhysioText] = React.useState(profile.physioExercises || '');
  const [injuryPhysioSaved, setInjuryPhysioSaved] = React.useState(false);
  const saveInjuryPhysio = () => {
    onSave({ ...profile, currentInjuries: injuryText, physioExercises: physioText });
    setInjuryPhysioSaved(true);
    setTimeout(() => setInjuryPhysioSaved(false), 2000);
  };
  /* ── Existing profile view ── */
  if (isExisting) {"""

assert OLD_PROFILE_FN in content, "ProfileScreen function anchor not found"
content = content.replace(OLD_PROFILE_FN, NEW_PROFILE_FN)
print("Part 5a done: ProfileScreen state hooks added")

# ════════════════════════════════════════════════════════════════════
# PART 5b — Add injury/physio card before REGENERATE PLAN button
# ════════════════════════════════════════════════════════════════════
OLD_REGEN = """          <button onClick={() => onGeneratePlan(profile)}
            className="w-full py-4 rounded-2xl bg-[#C8FF00] text-[#0D0D0F] font-display text-xl tracking-wider active:scale-95 transition-all"
            style={{ fontFamily:"'Bebas Neue',sans-serif" }}>
            REGENERATE PLAN
          </button>"""

NEW_REGEN = """          {/* My Injuries & Physio */}
          <div className="bg-[#1A1A1C] rounded-2xl p-5 border border-[#252527]">
            <p className="text-[#8A8A8E] text-xs uppercase tracking-widest mb-3">My Injuries & Physio</p>
            <p className="text-[#8A8A8E] text-xs mb-1">Current injuries</p>
            <textarea
              value={injuryText}
              onChange={e => setInjuryText(e.target.value)}
              placeholder="e.g. Left shoulder impingement, right knee pain…"
              rows={2}
              className="w-full bg-[#252527] text-[#F5F5F0] text-sm rounded-xl px-3 py-2 border border-[#3A3A3C] resize-none outline-none placeholder-[#5A5A5E]"
              style={{ fontFamily:"'DM Sans',sans-serif" }}
            />
            <p className="text-[#8A8A8E] text-xs mb-1 mt-3">Physio prescribed exercises</p>
            <textarea
              value={physioText}
              onChange={e => setPhysioText(e.target.value)}
              placeholder="e.g. Clamshells, banded monster walks, dead bugs…"
              rows={2}
              className="w-full bg-[#252527] text-[#F5F5F0] text-sm rounded-xl px-3 py-2 border border-[#3A3A3C] resize-none outline-none placeholder-[#5A5A5E]"
              style={{ fontFamily:"'DM Sans',sans-serif" }}
            />
            <button onClick={saveInjuryPhysio}
              className="w-full mt-3 py-3 rounded-xl active:scale-95 transition-all"
              style={{ background: injuryPhysioSaved ? '#30D158' : '#C8FF00', color:'#0D0D0F', fontFamily:"'Bebas Neue',sans-serif", fontSize:15, letterSpacing:'0.06em', border:'none', cursor:'pointer' }}>
              {injuryPhysioSaved ? 'SAVED' : 'SAVE INJURY & PHYSIO'}
            </button>
          </div>

          <button onClick={() => onGeneratePlan(profile)}
            className="w-full py-4 rounded-2xl bg-[#C8FF00] text-[#0D0D0F] font-display text-xl tracking-wider active:scale-95 transition-all"
            style={{ fontFamily:"'Bebas Neue',sans-serif" }}>
            REGENERATE PLAN
          </button>"""

assert OLD_REGEN in content, "REGENERATE PLAN anchor not found"
content = content.replace(OLD_REGEN, NEW_REGEN)
print("Part 5b done: Injury & Physio card added to ProfileScreen")

# ════════════════════════════════════════════════════════════════════
# Bonus — Add injury/physio to coach ATHLETE line in buildSystemPrompt
# ════════════════════════════════════════════════════════════════════
OLD_ATHLETE = "ATHLETE: ${name} | Level: ${profile.fitnessLevel||'unknown'} | Goal: ${profile.goal||'unknown'} | Equipment: ${(profile.equipment||[]).join(', ')||'unknown'} | Split: ${profile.preferredSplit||'coach-selected'} | Days: ${(profile.trainingDays||[]).join(', ')||'unknown'} | Session: ${profile.sessionLength||60}min"

NEW_ATHLETE = "ATHLETE: ${name} | Level: ${profile.fitnessLevel||'unknown'} | Goal: ${profile.goal||'unknown'} | Equipment: ${(profile.equipment||[]).join(', ')||'unknown'} | Split: ${profile.preferredSplit||'coach-selected'} | Days: ${(profile.trainingDays||[]).join(', ')||'unknown'} | Session: ${profile.sessionLength||60}min | Injuries: ${profile.currentInjuries||'None'} | Physio: ${profile.physioExercises||'None'}"

assert OLD_ATHLETE in content, "ATHLETE line in buildSystemPrompt not found"
content = content.replace(OLD_ATHLETE, NEW_ATHLETE)
print("Bonus: currentInjuries and physioExercises added to coach ATHLETE line")

# ════════════════════════════════════════════════════════════════════
# Bonus — Add injury/physio to plan ATHLETE PROFILE
# ════════════════════════════════════════════════════════════════════
OLD_PLAN_PROFILE = "- Session Length: ${profile.sessionLength} minutes\n\nGENERAL RULES"
NEW_PLAN_PROFILE = "- Session Length: ${profile.sessionLength} minutes\n- Current Injuries: ${profile.currentInjuries || 'None'}\n- Physio Prescribed Exercises: ${profile.physioExercises || 'None'}\n\nGENERAL RULES"

assert OLD_PLAN_PROFILE in content, "plan ATHLETE PROFILE anchor not found"
content = content.replace(OLD_PLAN_PROFILE, NEW_PLAN_PROFILE)
print("Bonus: injury/physio added to plan ATHLETE PROFILE")

with open('forge.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll done. Total lines:", content.count('\n'))
print("currentInjuries question present:", "Do you have any current injuries" in content)
print("physioExercises question present:", "physiotherapist, doctor, or specialist given you" in content)
print("handleSkip generic:", "QUESTIONS[currentQ].id" in content)
print("parsePlanChange PROFILE_UPDATE:", "PROFILE_UPDATE:" in content and "profileUpdate" in content)
print("CoachProfileUpdateCard present:", "CoachProfileUpdateCard" in content)
print("pendingProfileUpdates present:", "pendingProfileUpdates" in content)
print("body map injury context:", "KNOWN INJURIES:" in content)
print("ME tab injury card:", "My Injuries" in content)
print("Plan PHYSIO section:", "PHYSIO AND INJURY MANAGEMENT:" in content)
