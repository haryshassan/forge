#!/usr/bin/env python3
"""Replace onboarding wizard with conversational AI onboarding."""

with open('forge.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Replace the entire ProfileScreen + the section header ──────────────────
OLD_PROFILE_SECTION = '''/* ═══════════════════════════════════════════════
   PROFILE / ONBOARDING SCREEN
═══════════════════════════════════════════════ */
function ProfileScreen({ profile, onSave, onGeneratePlan, isExisting, onNutritionGoals=()=>{}, onLogout=()=>{} }) {
  const TOTAL_STEPS = 7;
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({
    name:                profile.name || '',
    fitnessLevel:        profile.fitnessLevel || '',
    goal:                profile.goal || '',
    equipment:           profile.equipment || [],
    trainingDaysPerWeek: profile.trainingDaysPerWeek || 3,
    trainingDays:        profile.trainingDays || [],
    trainingSplit:       profile.trainingSplit || '',
    sessionLength:       profile.sessionLength || 60,
  });

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const toggleArr = (k, val) =>
    setForm(f => ({
      ...f, [k]: f[k].includes(val) ? f[k].filter(x => x !== val) : [...f[k], val]
    }));

  const canAdvance = () => {
    if (step === 0) return form.name.trim().length > 0;
    if (step === 1) return !!form.fitnessLevel;
    if (step === 2) return !!form.goal;
    if (step === 3) return form.equipment.length > 0;
    if (step === 4) return form.trainingDays.length > 0;
    if (step === 5) return !!form.trainingSplit;
    if (step === 6) return !!form.sessionLength;
    return true;
  };

  const handleFinish = () => {
    const saved = { ...form, trainingDaysPerWeek: form.trainingDays.length, onboardingComplete: true };
    onSave(saved);
    onGeneratePlan(saved);
  };'''

assert OLD_PROFILE_SECTION in content, "Could not find ProfileScreen start"

# Find end of ProfileScreen (the closing `}` after the wizard return)
# We'll replace from the section header to the closing brace of ProfileScreen
# The section ends at line 2271 which contains just `}`
# Let's find the exact old block to replace

OLD_WIZARD_TAIL = '''  /* ── Onboarding wizard ── */
  return (
    <div className="h-full flex flex-col bg-[#0D0D0F]">
      {/* Progress bar */}
      <div className="flex-shrink-0 px-5 pt-14 pb-0">
        <div className="flex gap-1.5 mb-8">
          {Array.from({ length: TOTAL_STEPS }).map((_,i) => (
            <div key={i} className="h-1 flex-1 rounded-full transition-all duration-300"
              style={{ background: i <= step ? '#C8FF00' : '#252527' }}/>
          ))}
        </div>
      </div>

      {/* Step content */}
      <div className="flex-1 overflow-y-auto px-5 pb-4">

        {/* Step 0: Name */}
        {step === 0 && (
          <div className="animate-fade-slide">
            <p className="text-[#C8FF00] font-display text-sm tracking-widest mb-2" style={{ fontFamily:"'Bebas Neue',sans-serif" }}>STEP 1 OF 7</p>
            <h2 className="font-display text-5xl text-[#F5F5F0] mb-2" style={{ fontFamily:"'Bebas Neue',sans-serif" }}>WHAT\'S YOUR NAME?</h2>
            <p className="text-[#8A8A8E] mb-8">We\'ll use this to personalise everything.</p>
            <input type="text" value={form.name}
              onChange={e => set(\'name\', e.target.value)}
              onKeyDown={e => e.key === \'Enter\' && canAdvance() && setStep(1)}
              placeholder="Your name…" autoFocus
              className="w-full bg-[#1A1A1C] text-[#F5F5F0] rounded-2xl px-5 py-5 text-2xl font-display border border-[#3A3A3C] focus:border-[#C8FF00] outline-none tracking-wider"
              style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}/>
          </div>
        )}

        {/* Step 1: Level */}
        {step === 1 && (
          <div className="animate-fade-slide">
            <p className="text-[#C8FF00] font-display text-sm tracking-widest mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>STEP 2 OF 7</p>
            <h2 className="font-display text-5xl text-[#F5F5F0] mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>YOUR LEVEL?</h2>
            <p className="text-[#8A8A8E] mb-8">Be honest — it helps us build the right plan.</p>
            <div className="space-y-3">
              {LEVELS.map(level => (
                <button key={level} onClick={() => set(\'fitnessLevel\', level)}
                  className={`w-full text-left px-6 py-5 rounded-2xl border-2 transition-all active:scale-95
                    ${form.fitnessLevel === level
                      ? \'border-[#C8FF00] bg-[rgba(200,255,0,0.07)]\'
                      : \'border-[#3A3A3C] bg-[#1A1A1C]\'}`}>
                  <p className={`font-display text-2xl ${form.fitnessLevel === level ? \'text-[#C8FF00]\' : \'text-[#F5F5F0]\'}`}
                    style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>{level.toUpperCase()}</p>
                  <p className="text-[#8A8A8E] text-sm mt-0.5">{LEVEL_DESC[level]}</p>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 2: Goal */}
        {step === 2 && (
          <div className="animate-fade-slide">
            <p className="text-[#C8FF00] font-display text-sm tracking-widest mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>STEP 3 OF 7</p>
            <h2 className="font-display text-5xl text-[#F5F5F0] mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>YOUR GOAL?</h2>
            <p className="text-[#8A8A8E] mb-8">What are you training for?</p>
            <div className="space-y-3">
              {GOALS.map(goal => (
                <button key={goal} onClick={() => set(\'goal\', goal)}
                  className={`w-full text-left px-6 py-4 rounded-2xl border-2 transition-all active:scale-95
                    ${form.goal === goal
                      ? \'border-[#C8FF00] bg-[rgba(200,255,0,0.07)]\'
                      : \'border-[#3A3A3C] bg-[#1A1A1C]\'}`}>
                  <p className={`font-display text-xl ${form.goal === goal ? \'text-[#C8FF00]\' : \'text-[#F5F5F0]\'}`}
                    style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>{goal.toUpperCase()}</p>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 3: Equipment */}
        {step === 3 && (
          <div className="animate-fade-slide">
            <p className="text-[#C8FF00] font-display text-sm tracking-widest mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>STEP 4 OF 7</p>
            <h2 className="font-display text-5xl text-[#F5F5F0] mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>EQUIPMENT?</h2>
            <p className="text-[#8A8A8E] mb-8">Select everything you have access to.</p>
            <div className="flex flex-wrap gap-3">
              {EQUIPMENT_OPTIONS.map(eq => (
                <Pill key={eq} active={form.equipment.includes(eq)} onClick={() => toggleArr(\'equipment\', eq)}>{eq}</Pill>
              ))}
            </div>
          </div>
        )}

        {/* Step 4: Training days */}
        {step === 4 && (
          <div className="animate-fade-slide">
            <p className="text-[#C8FF00] font-display text-sm tracking-widest mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>STEP 5 OF 7</p>
            <h2 className="font-display text-5xl text-[#F5F5F0] mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>TRAINING DAYS?</h2>
            <p className="text-[#8A8A8E] mb-6">Which days will you train each week?</p>
            <div className="flex justify-between gap-1 mb-5">
              {DAY_ABBR.map((abbr, i) => {
                const day = DAYS[i];
                const on = form.trainingDays.includes(day);
                return (
                  <button key={day} onClick={() => toggleArr(\'trainingDays\', day)}
                    className={`w-10 h-10 rounded-xl text-xs font-display transition-all active:scale-90
                      ${on ? \'bg-[#C8FF00] text-[#0D0D0F]\' : \'bg-[#1A1A1C] text-[#8A8A8E] border border-[#3A3A3C]\'}`}
                    style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>
                    {abbr}
                  </button>
                );
              })}
            </div>
            {form.trainingDays.length > 0 && (
              <div className="bg-[#1A1A1C] rounded-2xl p-4 border border-[#252527] flex flex-wrap gap-2">
                {form.trainingDays.map(d => (
                  <span key={d} className="text-[#C8FF00] text-xs bg-[rgba(200,255,0,0.1)] px-2 py-0.5 rounded-full">{d.slice(0,3)}</span>
                ))}
                <span className="text-[#8A8A8E] text-xs ml-auto self-center">{form.trainingDays.length} days</span>
              </div>
            )}
          </div>
        )}

        {/* Step 5: Training split */}
        {step === 5 && (
          <div className="animate-fade-slide">
            <p className="text-[#C8FF00] font-display text-sm tracking-widest mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>STEP 6 OF 7</p>
            <h2 className="font-display text-5xl text-[#F5F5F0] mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>YOUR SPLIT?</h2>
            <p className="text-[#8A8A8E] mb-6">Choose how to structure your {form.trainingDays.length}-day week.</p>
            <div className="space-y-3">
              {(TRAINING_SPLITS[Math.min(form.trainingDays.length, 7)] || TRAINING_SPLITS[3]).map(split => {
                const sel = form.trainingSplit === split.id;
                return (
                <button key={split.id} onClick={() => set(\'trainingSplit\', split.id)}
                  className={`w-full text-left px-5 py-4 rounded-2xl border-2 transition-all active:scale-95 relative
                    ${sel ? \'border-[#C8FF00] bg-[rgba(200,255,0,0.07)]\' : \'border-[#3A3A3C] bg-[#1A1A1C]\'}`}>
                  {split.badge && (
                    <span className="absolute top-3 right-4 text-[9px] font-bold px-2 py-0.5 rounded-full"
                      style={{ background:\'rgba(200,255,0,0.2)\', color:\'#C8FF00\', border:\'1px solid rgba(200,255,0,0.3)\' }}>
                      {split.badge}
                    </span>
                  )}
                  <p className={`font-display text-xl ${sel ? \'text-[#C8FF00]\' : \'text-[#F5F5F0]\'}`}
                    style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>{split.name.toUpperCase()}</p>
                  {split.days && (
                    <p className="text-[#8A8A8E] text-xs mt-0.5">{split.days}</p>
                  )}
                  <p className={`text-sm mt-1 ${sel ? \'text-[rgba(200,255,0,0.7)]\' : \'text-[#8A8A8E]\'}`}>{split.desc}</p>
                  {split.bestFor && (
                    <p className="text-[#8A8A8E] text-[11px] mt-1">Best for: {split.bestFor}</p>
                  )}
                </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Step 6: Session length */}
        {step === 6 && (
          <div className="animate-fade-slide">
            <p className="text-[#C8FF00] font-display text-sm tracking-widest mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>STEP 7 OF 7</p>
            <h2 className="font-display text-5xl text-[#F5F5F0] mb-2" style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>LAST DETAILS</h2>
            <p className="text-[#8A8A8E] mb-6">How long are your sessions?</p>

            <div className="grid grid-cols-4 gap-3 mb-8">
              {SESSION_LENGTHS.map(len => (
                <button key={len} onClick={() => set(\'sessionLength\', len)}
                  className={`py-4 rounded-2xl text-center border-2 transition-all active:scale-95
                    ${form.sessionLength === len
                      ? \'border-[#C8FF00] bg-[rgba(200,255,0,0.07)]\'
                      : \'border-[#3A3A3C] bg-[#1A1A1C]\'}`}>
                  <p className={`font-display text-2xl ${form.sessionLength === len ? \'text-[#C8FF00]\' : \'text-[#F5F5F0]\'}`}
                    style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>{len}</p>
                  <p className="text-[#8A8A8E] text-xs">min</p>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* CTA row */}
      <div className="flex-shrink-0 px-5 py-4 flex gap-3"
        style={{ paddingBottom:\'max(1.5rem, env(safe-area-inset-bottom))\' }}>
        {step > 0 && (
          <button onClick={() => setStep(s => s - 1)}
            className="w-14 h-14 rounded-2xl bg-[#1A1A1C] flex items-center justify-center active:scale-95 transition-all border border-[#3A3A3C]">
            <ChevronLeft size={24} color="#F5F5F0"/>
          </button>
        )}
        <button
          onClick={() => step < TOTAL_STEPS - 1 ? setStep(s => s + 1) : handleFinish()}
          disabled={!canAdvance()}
          className={`flex-1 py-4 rounded-2xl font-display text-xl tracking-wider transition-all active:scale-95
            ${canAdvance() ? \'bg-[#C8FF00] text-[#0D0D0F]\' : \'bg-[#252527] text-[#8A8A8E]\'}`}
          style={{ fontFamily:"\'Bebas Neue\',sans-serif" }}>
          {step === TOTAL_STEPS - 1 ? \'GENERATE MY PLAN\' : \'CONTINUE\'}
        </button>
      </div>
    </div>
  );
}'''

assert OLD_WIZARD_TAIL in content, "Could not find wizard tail"

NEW_COMPONENTS = '''/* ═══════════════════════════════════════════════
   CONVERSATIONAL ONBOARDING
═══════════════════════════════════════════════ */
function ConversationalOnboarding({ onComplete }) {
  const QUESTIONS = [
    { id:'name',              text:"What should I call you?",                                                             type:'text',       placeholder:'Your name…' },
    { id:'goal',              text:"What’s your main goal right now?",                                                   type:'chips',      options:['Build Muscle','Get Stronger','Lose Fat','Athletic Performance','General Fitness'] },
    { id:'experience',        text:"How long have you been training seriously?",                                          type:'chips',      options:['Less than 6 months','6 months to 2 years','2 to 5 years','5+ years'] },
    { id:'currentRoutine',    text:"Tell me about your current training. What does your week look like right now?",       type:'text',       placeholder:'e.g. I go to the gym 3x a week…' },
    { id:'obstacle',          text:"What’s the biggest thing that’s stopped you from reaching your goal before?",       type:'text',       placeholder:'Be honest…' },
    { id:'equipment',         text:"What equipment do you have access to?",                                               type:'multichips', options:['Full Gym','Dumbbells Only','Barbell and Rack','Cables','Resistance Bands','Pull Up Bar','No Equipment'] },
    { id:'trainingDaysCount', text:"How many days per week can you train?",                                               type:'chips',      options:['2','3','4','5','6'] },
    { id:'sessionLength',     text:"How long can you train per session?",                                                 type:'chips',      options:['30 minutes','45 minutes','60 minutes','75+ minutes'] },
    { id:'limitations',       text:"Do you have any injuries, pain, or physical limitations I should know about?",        type:'text',       placeholder:'e.g. Lower back pain, bad knees…', skippable:true },
    { id:'lifestyle',         text:"How’s your sleep and stress generally?",                                             type:'chips',      options:['Pretty good','Could be better','Pretty poor'] },
  ];

  const LOADING_PHRASES = [
    'Analysing your goals…',
    'Reviewing your training history…',
    'Selecting your exercises…',
    'Building your weekly structure…',
    'Calibrating recovery protocols…',
    'Finalising your program…',
  ];

  const EXP_MAP = {
    'Less than 6 months':'Beginner',
    '6 months to 2 years':'Beginner',
    '2 to 5 years':'Intermediate',
    '5+ years':'Advanced',
  };
  const DAYS_MAP = {
    2:['Monday','Thursday'],
    3:['Monday','Wednesday','Friday'],
    4:['Monday','Tuesday','Thursday','Friday'],
    5:['Monday','Tuesday','Wednesday','Thursday','Friday'],
    6:['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
  };
  const SESSION_MAP = { '30 minutes':30,'45 minutes':45,'60 minutes':60,'75+ minutes':75 };

  const autoSplit = (goal, days) => {
    if (days <= 2) return 'Full Body';
    if (days === 3) return goal === 'Get Stronger' ? 'Push / Pull / Legs' : 'Full Body';
    if (days === 4) return 'Upper / Lower';
    return 'Push / Pull / Legs';
  };

  const [messages,       setMessages]       = useState([]);
  const [phase,          setPhase]          = useState('chat');
  const [currentQ,       setCurrentQ]       = useState(-1);
  const [answers,        setAnswers]        = useState({});
  const [inputText,      setInputText]      = useState('');
  const [selectedChips,  setSelectedChips]  = useState([]);
  const [typing,         setTyping]         = useState(false);
  const [recommendation, setRecommendation] = useState('');
  const [loadingPhrase,  setLoadingPhrase]  = useState(0);
  const chatEndRef = React.useRef(null);
  const inputRef   = React.useRef(null);

  React.useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior:'smooth' });
  }, [messages, typing]);

  React.useEffect(() => {
    if (phase !== 'loading') return;
    const t = setInterval(() => setLoadingPhrase(p => (p + 1) % LOADING_PHRASES.length), 1800);
    return () => clearInterval(t);
  }, [phase]);

  React.useEffect(() => {
    const t1 = setTimeout(() => {
      setMessages([{ role:'coach', text:"Hey, I’m your FORGE Coach. Before I build your program, I want to get to know you properly. This will only take a couple of minutes — and everything I ask will shape exactly how I train you. Let’s go." }]);
      const t2 = setTimeout(() => {
        setCurrentQ(0);
        setMessages(prev => [...prev, { role:'coach', text:QUESTIONS[0].text }]);
      }, 900);
      return () => clearTimeout(t2);
    }, 400);
    return () => clearTimeout(t1);
  }, []);

  const canSubmit = () => {
    if (currentQ < 0 || currentQ >= QUESTIONS.length) return false;
    const q = QUESTIONS[currentQ];
    if (q.type === 'text')       return inputText.trim().length > 0;
    if (q.type === 'chips')      return selectedChips.length === 1;
    if (q.type === 'multichips') return selectedChips.length > 0;
    return false;
  };

  const handleChipToggle = (chip) => {
    const q = QUESTIONS[currentQ];
    if (!q) return;
    if (q.type === 'chips') {
      setSelectedChips([chip]);
    } else {
      setSelectedChips(prev => prev.includes(chip) ? prev.filter(c => c !== chip) : [...prev, chip]);
    }
  };

  const handleSubmit = async () => {
    if (!canSubmit()) return;
    const q = QUESTIONS[currentQ];
    const answer = q.type === 'text' ? inputText.trim()
      : q.type === 'chips' ? selectedChips[0]
      : [...selectedChips];
    const displayText = Array.isArray(answer) ? answer.join(', ') : answer;
    const newAnswers = { ...answers, [q.id]: answer };

    setMessages(prev => [...prev, { role:'user', text:displayText }]);
    setAnswers(newAnswers);
    setInputText('');
    setSelectedChips('');
    setCurrentQ(-1);

    if (currentQ === QUESTIONS.length - 1) {
      await buildRecommendation(newAnswers);
    } else {
      await getAcknowledgement(q.text, answer, currentQ + 1);
    }
  };

  const handleSkip = () => {
    const newAnswers = { ...answers, limitations:'' };
    setAnswers(newAnswers);
    setMessages(prev => [...prev, { role:'user', text:'No limitations' }]);
    setInputText('');
    const nextIdx = currentQ + 1;
    setCurrentQ(nextIdx);
    setTimeout(() => setMessages(prev => [...prev, { role:'coach', text:QUESTIONS[nextIdx].text }]), 300);
  };

  const getAcknowledgement = async (qText, answer, nextIdx) => {
    setTyping(true);
    try {
      const displayText = Array.isArray(answer) ? answer.join(', ') : answer;
      const ackPrompt = 'You are an elite fitness coach named FORGE. The athlete answered "' + displayText + '" to: "' + qText + '". Reply with ONE short motivating acknowledgement (max 12 words). Natural and specific. No questions. No emoji.';
      const ack = await callClaude([{ role:'user', content:ackPrompt }], 80);
      setTyping(false);
      setMessages(prev => [...prev, { role:'coach', text:ack.trim() }]);
      setTimeout(() => {
        setCurrentQ(nextIdx);
        setMessages(prev => [...prev, { role:'coach', text:QUESTIONS[nextIdx].text }]);
      }, 500);
    } catch {
      setTyping(false);
      setCurrentQ(nextIdx);
      setMessages(prev => [...prev, { role:'coach', text:QUESTIONS[nextIdx].text }]);
    }
  };

  const buildRecommendation = async (finalAnswers) => {
    setPhase('loading');
    try {
      const eqStr = Array.isArray(finalAnswers.equipment) ? finalAnswers.equipment.join(', ') : (finalAnswers.equipment || 'Not specified');
      const recPrompt = 'You are an elite personal trainer. Based on this athlete profile, write a personalised program recommendation with EXACTLY these 5 bold headings, one short paragraph each:\n\n**Your Program** — recommended split and why it suits them\n**Your Week** — day-by-day structure\n**First 4 Weeks** — what to focus on and expect\n**Addressing Your Obstacle** — advice based on what held them back\n**Recovery Note** — based on their sleep/stress\n\nProfile: Name: ' + finalAnswers.name + '. Goal: ' + finalAnswers.goal + '. Experience: ' + finalAnswers.experience + '. Current routine: ' + finalAnswers.currentRoutine + '. Obstacle: ' + finalAnswers.obstacle + '. Equipment: ' + eqStr + '. Training days: ' + finalAnswers.trainingDaysCount + '/week. Session: ' + finalAnswers.sessionLength + '. Limitations: ' + (finalAnswers.limitations || 'None') + '. Sleep/stress: ' + finalAnswers.lifestyle + '.\n\nBe direct and specific. Max 220 words total.';
      const rec = await callClaude([{ role:'user', content:recPrompt }], 600);
      setRecommendation(rec.trim());
      setPhase('recommendation');
    } catch {
      setRecommendation('**Your Program**\n\nProgram analysis complete based on your profile.\n\n**Your Week**\n\nA personalised schedule will be generated for you.\n\n**First 4 Weeks**\n\nFocus on form and building the habit.\n\n**Addressing Your Obstacle**\n\nWe’ll tackle this together with the right structure.\n\n**Recovery Note**\n\nPrioritise sleep — it’s when you actually get stronger.');
      setPhase('recommendation');
    }
  };

  const handleConfirm = () => {
    const daysCount = parseInt(answers.trainingDaysCount) || 3;
    const profile = {
      name:                answers.name || '',
      goal:                answers.goal || '',
      fitnessLevel:        EXP_MAP[answers.experience] || 'Beginner',
      currentRoutine:      answers.currentRoutine || '',
      obstacle:            answers.obstacle || '',
      equipment:           Array.isArray(answers.equipment) ? answers.equipment : (answers.equipment ? [answers.equipment] : []),
      trainingDays:        DAYS_MAP[daysCount] || DAYS_MAP[3],
      trainingDaysPerWeek: daysCount,
      sessionLength:       SESSION_MAP[answers.sessionLength] || 60,
      limitations:         answers.limitations || '',
      lifestyle:           answers.lifestyle || '',
      trainingSplit:       autoSplit(answers.goal, daysCount),
      onboardingComplete:  true,
    };
    onComplete(profile);
  };

  const handleAdjust = () => {
    setPhase('chat');
    setRecommendation('');
    setSelectedChips([]);
    setInputText('');
    const backIdx = 6;
    setCurrentQ(backIdx);
    setMessages(prev => [...prev,
      { role:'coach', text:"No problem — let’s refine a few things." },
      { role:'coach', text:QUESTIONS[backIdx].text },
    ]);
  };

  /* ─── LOADING ─── */
  if (phase === 'loading') {
    return (
      <div style={{ background:'#0D0D0F', height:'100%', display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', gap:32, padding:'0 40px' }}>
        <div style={{ fontFamily:"'Bebas Neue',sans-serif", fontSize:52, color:'#C8FF00', letterSpacing:'0.08em' }}>FORGE</div>
        <div style={{ textAlign:'center' }}>
          <p style={{ color:'#F5F5F0', fontSize:18, fontWeight:700, marginBottom:8, margin:'0 0 8px' }}>Building your program</p>
          <p style={{ color:'#8A8A8E', fontSize:14, margin:0 }}>{LOADING_PHRASES[loadingPhrase]}</p>
        </div>
        <div style={{ width:'100%', height:4, background:'#1A1A1C', borderRadius:99, overflow:'hidden' }}>
          <div style={{ height:'100%', background:'#C8FF00', borderRadius:99, animation:'forgeProgress 3s ease-in-out infinite' }}/>
        </div>
      </div>
    );
  }

  /* ─── RECOMMENDATION ─── */
  if (phase === 'recommendation') {
    const parseRec = (text) => {
      const parts = [];
      const regex = /\*\*(.+?)\*\*\s*[—-]?\s*([\s\S]*?)(?=\*\*|$)/g;
      let m;
      while ((m = regex.exec(text)) !== null) {
        parts.push({ heading: m[1].trim(), body: m[2].trim() });
      }
      if (parts.length === 0) parts.push({ heading: null, body: text });
      return parts;
    };
    const sections = parseRec(recommendation);

    return (
      <div style={{ background:'#0D0D0F', height:'100%', display:'flex', flexDirection:'column' }}>
        <div style={{ flexShrink:0, padding:'52px 20px 16px', display:'flex', alignItems:'center', gap:12 }}>
          <div style={{ fontFamily:"'Bebas Neue',sans-serif", fontSize:34, color:'#C8FF00', letterSpacing:'0.08em' }}>FORGE</div>
          <div style={{ flex:1 }}>
            <p style={{ color:'#F5F5F0', fontWeight:700, fontSize:16, margin:'0 0 2px' }}>Your Program is Ready</p>
            <p style={{ color:'#8A8A8E', fontSize:13, margin:0 }}>Here’s what I’ve built for you, {answers.name}</p>
          </div>
        </div>

        <div style={{ flex:1, overflowY:'auto', padding:'0 20px 12px' }}>
          <div style={{ background:'#1A1A1C', borderRadius:20, padding:'20px', border:'1px solid #252527', display:'flex', flexDirection:'column', gap:16 }}>
            {sections.map((s, i) => (
              <div key={i}>
                {s.heading && (
                  <p style={{ color:'#C8FF00', fontFamily:"'Bebas Neue',sans-serif", fontSize:13, letterSpacing:'0.1em', margin:'0 0 5px' }}>{s.heading.toUpperCase()}</p>
                )}
                <p style={{ color:'#F5F5F0', fontSize:14, lineHeight:1.65, margin:0 }}>{s.body}</p>
              </div>
            ))}
          </div>
        </div>

        <div style={{ flexShrink:0, padding:'12px 20px', paddingBottom:'max(20px, env(safe-area-inset-bottom))', display:'flex', flexDirection:'column', gap:10 }}>
          <button onClick={handleConfirm}
            style={{ background:'#C8FF00', color:'#0D0D0F', border:'none', borderRadius:16, padding:'18px 0', fontFamily:"'Bebas Neue',sans-serif", fontSize:20, letterSpacing:'0.08em', cursor:'pointer', width:'100%', fontWeight:700 }}>
            LOOKS GOOD — LET’S GO
          </button>
          <button onClick={handleAdjust}
            style={{ background:'#1A1A1C', color:'#F5F5F0', border:'1.5px solid #3A3A3C', borderRadius:16, padding:'15px 0', fontFamily:"'Bebas Neue',sans-serif", fontSize:18, letterSpacing:'0.08em', cursor:'pointer', width:'100%' }}>
            ADJUST THIS
          </button>
        </div>
      </div>
    );
  }

  /* ─── CHAT ─── */
  const q = (currentQ >= 0 && currentQ < QUESTIONS.length) ? QUESTIONS[currentQ] : null;

  return (
    <div style={{ background:'#0D0D0F', height:'100%', display:'flex', flexDirection:'column' }}>
      {/* Header */}
      <div style={{ flexShrink:0, padding:'52px 20px 10px', display:'flex', alignItems:'center', gap:10 }}>
        <div style={{ fontFamily:"'Bebas Neue',sans-serif", fontSize:32, color:'#C8FF00', letterSpacing:'0.08em' }}>FORGE</div>
        <div style={{ width:7, height:7, borderRadius:'50%', background:'#C8FF00', marginLeft:4, opacity:0.8 }}/>
        <p style={{ color:'#8A8A8E', fontSize:13, margin:0 }}>Coach Assessment</p>
      </div>

      {/* Chat feed */}
      <div style={{ flex:1, overflowY:'auto', padding:'4px 16px 8px', display:'flex', flexDirection:'column', gap:10 }}>
        {messages.map((m, i) => (
          <div key={i} style={{ display:'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start' }}>
            {m.role === 'coach' && (
              <div style={{ maxWidth:'82%', background:'#1A1A1C', borderRadius:'18px 18px 18px 4px', padding:'12px 16px', border:'1px solid #252527' }}>
                <p style={{ color:'#F5F5F0', fontSize:15, lineHeight:1.55, margin:0 }}>{m.text}</p>
              </div>
            )}
            {m.role === 'user' && (
              <div style={{ maxWidth:'82%', background:'#C8FF00', borderRadius:'18px 18px 4px 18px', padding:'12px 16px' }}>
                <p style={{ color:'#0D0D0F', fontSize:15, lineHeight:1.55, margin:0, fontWeight:600 }}>{m.text}</p>
              </div>
            )}
          </div>
        ))}

        {typing && (
          <div style={{ display:'flex', justifyContent:'flex-start' }}>
            <div style={{ background:'#1A1A1C', borderRadius:'18px 18px 18px 4px', padding:'13px 18px', border:'1px solid #252527', display:'flex', gap:6, alignItems:'center' }}>
              {[0,1,2].map(i => (
                <div key={i} style={{ width:7, height:7, borderRadius:'50%', background:'#C8FF00', animation:'dotPulse 1.2s ' + (i*0.2) + 's ease-in-out infinite', opacity:0.4 }}/>
              ))}
            </div>
          </div>
        )}
        <div ref={chatEndRef}/>
      </div>

      {/* Input area */}
      {q && (
        <div style={{ flexShrink:0, padding:'10px 16px', paddingBottom:'max(16px, env(safe-area-inset-bottom))', borderTop:'1px solid #1A1A1C', background:'#111113' }}>
          {(q.type === 'chips' || q.type === 'multichips') && (
            <div style={{ display:'flex', flexWrap:'wrap', gap:8, marginBottom:10 }}>
              {q.options.map(opt => {
                const active = selectedChips.includes(opt);
                return (
                  <button key={opt} onClick={() => handleChipToggle(opt)}
                    style={{ padding:'9px 15px', borderRadius:99, border: active ? '1.5px solid #C8FF00' : '1.5px solid #3A3A3C', background: active ? 'rgba(200,255,0,0.12)' : '#1A1A1C', color: active ? '#C8FF00' : '#F5F5F0', fontSize:14, fontWeight:500, cursor:'pointer', transition:'all 0.12s' }}>
                    {opt}
                  </button>
                );
              })}
            </div>
          )}

          {q.type === 'text' && (
            <div style={{ marginBottom:10 }}>
              <input
                ref={inputRef}
                value={inputText}
                onChange={e => setInputText(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey && canSubmit()) { e.preventDefault(); handleSubmit(); } }}
                placeholder={q.placeholder || 'Type your answer…'}
                style={{ width:'100%', background:'#1A1A1C', border:'1.5px solid #3A3A3C', borderRadius:14, padding:'12px 16px', color:'#F5F5F0', fontSize:15, outline:'none', boxSizing:'border-box', fontFamily:"'DM Sans',sans-serif" }}
                autoFocus
              />
            </div>
          )}

          <div style={{ display:'flex', gap:10 }}>
            {q.skippable && (
              <button onClick={handleSkip}
                style={{ padding:'14px 18px', borderRadius:14, border:'1.5px solid #3A3A3C', background:'#1A1A1C', color:'#8A8A8E', fontSize:15, fontWeight:600, cursor:'pointer', flexShrink:0 }}>
                Skip
              </button>
            )}
            <button onClick={handleSubmit} disabled={!canSubmit()}
              style={{ flex:1, padding:'14px 0', borderRadius:14, border:'none', background: canSubmit() ? '#C8FF00' : '#252527', color: canSubmit() ? '#0D0D0F' : '#8A8A8E', fontFamily:"'Bebas Neue',sans-serif", fontSize:19, letterSpacing:'0.08em', cursor: canSubmit() ? 'pointer' : 'not-allowed', transition:'background 0.12s, color 0.12s' }}>
              {currentQ === QUESTIONS.length - 1 ? 'DONE' : 'SEND'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════
   PROFILE SCREEN (ME TAB — existing users)
═══════════════════════════════════════════════ */
function ProfileScreen({ profile, onSave, onGeneratePlan, isExisting, onNutritionGoals=()=>{}, onLogout=()=>{}, onReset=()=>{} }) {'''

# The old ProfileScreen start we already captured above — we replace starting from the section header
# through to the end of the wizard
REPLACEMENT = NEW_COMPONENTS + '''
  /* ── Existing profile view ── */
  if (isExisting) {
    return (
      <div className="h-full overflow-y-auto pb-28">
        {/* Header */}
        <div className="px-5 pt-14 pb-6">
          <h1 className="font-display text-5xl text-[#F5F5F0]" style={{ fontFamily:"'Bebas Neue',sans-serif" }}>PROFILE</h1>
          <p className="text-[#8A8A8E] text-sm">Your training preferences</p>
        </div>

        <div className="px-5 space-y-3">
          {/* Name / level / goal */}
          <div className="bg-[#1A1A1C] rounded-2xl p-5 border border-[#252527] flex items-center justify-between">
            <div>
              <p className="text-[#8A8A8E] text-xs uppercase tracking-widest mb-0.5">Athlete</p>
              <p className="font-display text-2xl text-[#F5F5F0]" style={{ fontFamily:"'Bebas Neue',sans-serif" }}>{profile.name}</p>
            </div>
            <span className="bg-[rgba(200,255,0,0.1)] text-[#C8FF00] text-xs px-3 py-1 rounded-full font-semibold border border-[rgba(200,255,0,0.2)]">{profile.fitnessLevel}</span>
          </div>

          <div className="bg-[#1A1A1C] rounded-2xl p-5 border border-[#252527]">
            <p className="text-[#8A8A8E] text-xs uppercase tracking-widest mb-2">Goal</p>
            <span className="bg-[#C8FF00] text-[#0D0D0F] px-3 py-1 rounded-full text-sm font-bold">{profile.goal}</span>
          </div>

          <div className="bg-[#1A1A1C] rounded-2xl p-5 border border-[#252527]">
            <p className="text-[#8A8A8E] text-xs uppercase tracking-widest mb-3">Equipment</p>
            <div className="flex flex-wrap gap-2">
              {(profile.equipment||[]).map(e => (
                <span key={e} className="bg-[#252527] text-[#F5F5F0] px-3 py-1 rounded-full text-xs border border-[#3A3A3C]">{e}</span>
              ))}
            </div>
          </div>

          <div className="bg-[#1A1A1C] rounded-2xl p-5 border border-[#252527]">
            <p className="text-[#8A8A8E] text-xs uppercase tracking-widest mb-3">Training Schedule</p>
            <div className="flex flex-wrap gap-2 mb-2">
              {(profile.trainingDays||[]).map(d => (
                <span key={d} className="bg-[#252527] text-[#F5F5F0] px-3 py-1 rounded-full text-xs border border-[#3A3A3C]">{d}</span>
              ))}
            </div>
            <p className="text-[#8A8A8E] text-xs">{profile.sessionLength} min sessions</p>
          </div>

          <button onClick={() => onGeneratePlan(profile)}
            className="w-full py-4 rounded-2xl bg-[#C8FF00] text-[#0D0D0F] font-display text-xl tracking-wider active:scale-95 transition-all"
            style={{ fontFamily:"'Bebas Neue',sans-serif" }}>
            REGENERATE PLAN
          </button>

          {/* Nutrition goals link */}
          <button onClick={onNutritionGoals}
            className="w-full py-4 rounded-2xl bg-[#1A1A1C] text-[#C8FF00] font-display text-xl tracking-wider active:scale-95 transition-all border border-[rgba(200,255,0,0.2)] flex items-center justify-center gap-2"
            style={{ fontFamily:"'Bebas Neue',sans-serif" }}>
            <Flame size={18} color="#C8FF00"/> NUTRITION GOALS
          </button>

          <button onClick={onReset}
            className="w-full py-4 rounded-2xl bg-[#1A1A1C] text-[#FF453A] font-display text-xl tracking-wider active:scale-95 transition-all border border-[rgba(255,69,58,0.25)]"
            style={{ fontFamily:"'Bebas Neue',sans-serif" }}>
            RESET PROFILE
          </button>

          <button onClick={onLogout}
            className="w-full py-4 rounded-2xl bg-[#1A1A1C] text-[#8A8A8E] font-display text-xl tracking-wider active:scale-95 transition-all border border-[#252527]"
            style={{ fontFamily:"'Bebas Neue',sans-serif" }}>
            LOG OUT
          </button>
        </div>
      </div>
    );
  }

  return null;
}'''

# Now do the actual replacement
# We'll replace from the old section header through to the end of the wizard
OLD_FULL = (
    '/* ═══════════════════════════════════════════════\n'
    '   PROFILE / ONBOARDING SCREEN\n'
    '═══════════════════════════════════════════════ */\n'
    'function ProfileScreen({ profile, onSave, onGeneratePlan, isExisting, onNutritionGoals=()=>{}, onLogout=()=>{} }) {\n'
    '  const TOTAL_STEPS = 7;\n'
    '  const [step, setStep] = useState(0);\n'
    '  const [form, setForm] = useState({\n'
    '    name:                profile.name || \'\',\n'
    '    fitnessLevel:        profile.fitnessLevel || \'\',\n'
    '    goal:                profile.goal || \'\',\n'
    '    equipment:           profile.equipment || [],\n'
    '    trainingDaysPerWeek: profile.trainingDaysPerWeek || 3,\n'
    '    trainingDays:        profile.trainingDays || [],\n'
    '    trainingSplit:       profile.trainingSplit || \'\',\n'
    '    sessionLength:       profile.sessionLength || 60,\n'
    '  });\n'
    '\n'
    '  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));\n'
    '\n'
    '  const toggleArr = (k, val) =>\n'
    '    setForm(f => ({\n'
    '      ...f, [k]: f[k].includes(val) ? f[k].filter(x => x !== val) : [...f[k], val]\n'
    '    }));\n'
    '\n'
    '  const canAdvance = () => {\n'
    '    if (step === 0) return form.name.trim().length > 0;\n'
    '    if (step === 1) return !!form.fitnessLevel;\n'
    '    if (step === 2) return !!form.goal;\n'
    '    if (step === 3) return form.equipment.length > 0;\n'
    '    if (step === 4) return form.trainingDays.length > 0;\n'
    '    if (step === 5) return !!form.trainingSplit;\n'
    '    if (step === 6) return !!form.sessionLength;\n'
    '    return true;\n'
    '  };\n'
    '\n'
    '  const handleFinish = () => {\n'
    '    const saved = { ...form, trainingDaysPerWeek: form.trainingDays.length, onboardingComplete: true };\n'
    '    onSave(saved);\n'
    '    onGeneratePlan(saved);\n'
    '  };'
)

assert OLD_FULL in content, f"Could not find old ProfileScreen start block exactly"

# The wizard tail starts with "  /* ── Existing profile view ── */"
# We want to replace everything from OLD_FULL through to the end of the whole function
# including the wizard tail

# Let's find the index of the old full section
start_idx = content.index(OLD_FULL)
# Find the end of the old component (the wizard closing brace)
# Find OLD_WIZARD_TAIL after start_idx
wizard_end_marker = '  /* ── Onboarding wizard ── */\n  return ('
wizard_start = content.index(wizard_end_marker, start_idx)
# Find the `}` that closes the ProfileScreen function - it's after the wizard's last `)`
# The wizard ends with:
closing_sequence = '    </div>\n  );\n}'
wizard_func_end = content.index(closing_sequence, wizard_start)
# end index is after the closing `}`
end_idx = wizard_func_end + len(closing_sequence)

old_block = content[start_idx:end_idx]
print(f"Found block to replace: chars {start_idx} to {end_idx} ({end_idx - start_idx} chars)")
print(f"Block starts: {repr(old_block[:80])}")
print(f"Block ends:   {repr(old_block[-80:])}")

content = content[:start_idx] + REPLACEMENT + content[end_idx:]

# ── 2. Update App: onboarding route to use ConversationalOnboarding ─────────────
OLD_ONBOARDING_ROUTE = '''  /* Onboarding */
  if (!profile.onboardingComplete) {
    return (
      <div className="max-w-[430px] mx-auto h-screen overflow-hidden relative bg-[#0D0D0F]"
        style={{ fontFamily:"'DM Sans',sans-serif" }}>
        <ProfileScreen profile={profile} onSave={setProfile}
          onGeneratePlan={handleGeneratePlan} isExisting={false}/>
      </div>
    );
  }'''

assert OLD_ONBOARDING_ROUTE in content, "Could not find onboarding route"

NEW_ONBOARDING_ROUTE = '''  /* Onboarding */
  if (!profile.onboardingComplete) {
    return (
      <div className="max-w-[430px] mx-auto h-screen overflow-hidden relative bg-[#0D0D0F]"
        style={{ fontFamily:"'DM Sans',sans-serif" }}>
        <ConversationalOnboarding onComplete={(p) => { setProfile(p); handleGeneratePlan(p); }}/>
      </div>
    );
  }'''

content = content.replace(OLD_ONBOARDING_ROUTE, NEW_ONBOARDING_ROUTE)
assert NEW_ONBOARDING_ROUTE in content

# ── 3. Add onReset prop to ProfileScreen in the profile tab ─────────────────────
OLD_PROFILE_TAB = '''      case 'profile':  return <ProfileScreen profile={profile} onSave={setProfile}
                                onGeneratePlan={handleGeneratePlan} isExisting={true}
                                onNutritionGoals={()=>setShowNutrGoals(true)}
                                onLogout={handleLogout}/>;'''

assert OLD_PROFILE_TAB in content, "Could not find profile tab render"

NEW_PROFILE_TAB = '''      case 'profile':  return <ProfileScreen profile={profile} onSave={setProfile}
                                onGeneratePlan={handleGeneratePlan} isExisting={true}
                                onNutritionGoals={()=>setShowNutrGoals(true)}
                                onLogout={handleLogout}
                                onReset={() => { setProfile(p => ({ ...p, onboardingComplete:false })); setPlan(null); }}/>;'''

content = content.replace(OLD_PROFILE_TAB, NEW_PROFILE_TAB)
assert NEW_PROFILE_TAB in content

# ── 4. Add forgeProgress keyframe to the existing style injection at the bottom ─
OLD_STYLE = '''const __style = document.createElement('style');
__style.textContent = `@keyframes dotPulse{0%,100%{opacity:.2;transform:scale(.7)}50%{opacity:1;transform:scale(1)}}`;
document.head.appendChild(__style);'''

assert OLD_STYLE in content, "Could not find style injection"

NEW_STYLE = '''const __style = document.createElement('style');
__style.textContent = `@keyframes dotPulse{0%,100%{opacity:.2;transform:scale(.7)}50%{opacity:1;transform:scale(1)}}@keyframes forgeProgress{0%{width:0%;transform:translateX(0)}50%{width:70%}100%{width:100%;transform:translateX(0)}}`;
document.head.appendChild(__style);'''

content = content.replace(OLD_STYLE, NEW_STYLE)
assert NEW_STYLE in content

with open('forge.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Done. Total lines: {content.count(chr(10))}")
print(f"ConversationalOnboarding present: {'ConversationalOnboarding' in content}")
print(f"LOOKS GOOD button present: {'LOOKS GOOD' in content}")
print(f"RESET PROFILE button present: {'RESET PROFILE' in content}")
print(f"forgeProgress animation present: {'forgeProgress' in content}")
print(f"Old TOTAL_STEPS gone: {'const TOTAL_STEPS = 7' not in content}")
