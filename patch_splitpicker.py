#!/usr/bin/env python3
"""Replace preferredSplit free-text question with visual split picker card screen."""

with open('forge.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Change preferredSplit question to type:'splitpicker' ────────────────────
OLD_Q = "    { id:'preferredSplit', text:\"Do you have a preferred way to structure your training? For example Push Pull Legs, Upper Lower, Full Body, Arnold Split, Bro Split — or describe it in your own words. If you have no preference just say so and I will pick the best structure for your goal.\",                                   type:'text',       placeholder:'e.g. Push Pull Legs, or no preference…' },"
NEW_Q = """    { id:'preferredSplit', text:"splitpicker", type:'splitpicker' },"""
assert OLD_Q in content, "Q1 not found"
content = content.replace(OLD_Q, NEW_Q)

# ── 2. Add SPLITS constant + badge logic after SESSION_MAP ─────────────────────
OLD_SESSION_MAP = "  const SESSION_MAP = { '30 minutes':30,'45 minutes':45,'60 minutes':60,'75+ minutes':75 };"
NEW_SESSION_MAP = """  const SESSION_MAP = { '30 minutes':30,'45 minutes':45,'60 minutes':60,'75+ minutes':75 };

  const SPLITS = [
    { id:'Full Body',                     desc:'Train every muscle group each session' },
    { id:'Upper Lower',                   desc:'Alternate upper and lower body sessions' },
    { id:'Push Pull Legs',                desc:'Push muscles, pull muscles, legs — 3-day cycle' },
    { id:'PPL x2',                        desc:'Push Pull Legs run twice per week — 6 days' },
    { id:'Arnold Split',                  desc:'Chest & back, shoulders & arms, legs — 3-day cycle' },
    { id:'Arnold + Upper Lower',          desc:'Arnold split paired with upper/lower days — 5 days' },
    { id:'Bro Split',                     desc:'One muscle group per session — classic bodybuilder style' },
    { id:'PHUL',                          desc:'Power Hypertrophy Upper Lower — 4 days' },
    { id:'PHAT',                          desc:'Power Hypertrophy Adaptive Training — 5 days' },
    { id:'Daily Undulating Periodisation',desc:'Vary intensity and volume each day for strength and size' },
    { id:'5 Day Upper Lower PPL Hybrid',  desc:'Upper, lower, push, pull, legs over 5 days' },
  ];

  const getSplitBadges = (splitId, goal, daysCount) => {
    const byDays = {
      2:['Full Body','Upper Lower'],
      3:['Full Body','Upper Lower'],
      4:['Upper Lower','PHUL'],
      5:['Push Pull Legs','Arnold + Upper Lower'],
      6:['PPL x2','Arnold Split'],
    };
    const byGoal = {
      'Build Muscle':        ['Push Pull Legs','Arnold Split','PHUL','PHAT'],
      'Get Stronger':        ['PHUL','PHAT','Daily Undulating Periodisation'],
      'Lose Fat':            ['Full Body','Push Pull Legs'],
      'Athletic Performance':['Full Body','Upper Lower','Daily Undulating Periodisation'],
      'General Fitness':     ['Full Body','Upper Lower'],
    };
    const badges = [];
    if ((byDays[daysCount] || []).includes(splitId)) badges.push('Best for your days');
    if ((byGoal[goal]      || []).includes(splitId)) badges.push('Best for your goal');
    return badges;
  };"""
assert OLD_SESSION_MAP in content, "SESSION_MAP not found"
content = content.replace(OLD_SESSION_MAP, NEW_SESSION_MAP)

# ── 3. Add showSplitPicker + selectedSplitCard state ──────────────────────────
OLD_STATE = """  const [messages,       setMessages]       = useState([]);
  const [phase,          setPhase]          = useState('chat');
  const [currentQ,       setCurrentQ]       = useState(-1);
  const [answers,        setAnswers]        = useState({});
  const [inputText,      setInputText]      = useState('');
  const [selectedChips,  setSelectedChips]  = useState([]);
  const [typing,         setTyping]         = useState(false);
  const [recommendation, setRecommendation] = useState('');
  const [loadingPhrase,  setLoadingPhrase]  = useState(0);
  const chatEndRef = React.useRef(null);
  const inputRef   = React.useRef(null);"""
NEW_STATE = """  const [messages,        setMessages]        = useState([]);
  const [phase,           setPhase]           = useState('chat');
  const [currentQ,        setCurrentQ]        = useState(-1);
  const [answers,         setAnswers]         = useState({});
  const [inputText,       setInputText]       = useState('');
  const [selectedChips,   setSelectedChips]   = useState([]);
  const [typing,          setTyping]          = useState(false);
  const [recommendation,  setRecommendation]  = useState('');
  const [loadingPhrase,   setLoadingPhrase]   = useState(0);
  const [showSplitPicker, setShowSplitPicker] = useState(false);
  const [selectedSplit,   setSelectedSplit]   = useState('');
  const chatEndRef = React.useRef(null);
  const inputRef   = React.useRef(null);"""
assert OLD_STATE in content, "STATE not found"
content = content.replace(OLD_STATE, NEW_STATE)

# ── 4. Pass newAnswers into getAcknowledgement call from handleSubmit ──────────
OLD_ACK_CALL = "      await getAcknowledgement(q.text, answer, currentQ + 1);"
NEW_ACK_CALL = "      await getAcknowledgement(q.text, answer, currentQ + 1, newAnswers);"
assert OLD_ACK_CALL in content, "ack call not found"
content = content.replace(OLD_ACK_CALL, NEW_ACK_CALL)

# ── 5. Replace getAcknowledgement to handle splitpicker branch ────────────────
OLD_ACK_FN = """  const getAcknowledgement = async (qText, answer, nextIdx) => {
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
  };"""
NEW_ACK_FN = """  const getAcknowledgement = async (qText, answer, nextIdx, allAnswers) => {
    const _ans = allAnswers || answers;
    setTyping(true);
    try {
      const displayText = Array.isArray(answer) ? answer.join(', ') : answer;
      const ackPrompt = 'You are an elite fitness coach named FORGE. The athlete answered "' + displayText + '" to: "' + qText + '". Reply with ONE short motivating acknowledgement (max 12 words). Natural and specific. No questions. No emoji.';
      const ack = await callClaude([{ role:'user', content:ackPrompt }], 80);
      setTyping(false);
      setMessages(prev => [...prev, { role:'coach', text:ack.trim() }]);
      if (QUESTIONS[nextIdx] && QUESTIONS[nextIdx].type === 'splitpicker') {
        const daysStr = _ans.trainingDays || '3 days';
        const goalStr = _ans.goal || 'your goal';
        setTimeout(() => {
          setMessages(prev => [...prev, { role:'coach', text:'Based on your goal and ' + daysStr + ' a week, here are the splits I would recommend for you — but the choice is yours.' }]);
          setTimeout(() => setShowSplitPicker(true), 400);
        }, 500);
      } else {
        setTimeout(() => {
          setCurrentQ(nextIdx);
          setMessages(prev => [...prev, { role:'coach', text:QUESTIONS[nextIdx].text }]);
        }, 500);
      }
    } catch {
      setTyping(false);
      if (QUESTIONS[nextIdx] && QUESTIONS[nextIdx].type === 'splitpicker') {
        const daysStr = _ans.trainingDays || '3 days';
        setMessages(prev => [...prev, { role:'coach', text:'Based on your goal and ' + daysStr + ' a week, here are the splits I would recommend for you — but the choice is yours.' }]);
        setTimeout(() => setShowSplitPicker(true), 400);
      } else {
        setCurrentQ(nextIdx);
        setMessages(prev => [...prev, { role:'coach', text:QUESTIONS[nextIdx].text }]);
      }
    }
  };"""
assert OLD_ACK_FN in content, "ACK_FN not found"
content = content.replace(OLD_ACK_FN, NEW_ACK_FN)

# ── 6. Add handleSplitConfirm after handleSkip ───────────────────────────────
OLD_AFTER_SKIP = """  const getAcknowledgement = async (qText, answer, nextIdx, allAnswers) => {"""
NEW_AFTER_SKIP = """  const handleSplitConfirm = async (splitName) => {
    setShowSplitPicker(false);
    setSelectedSplit('');
    const splitQIdx = QUESTIONS.findIndex(q => q.id === 'preferredSplit');
    const nextIdx = splitQIdx + 1;
    const newAnswers = { ...answers, preferredSplit: splitName };
    setAnswers(newAnswers);
    setMessages(prev => [...prev, { role:'user', text: splitName }]);
    await getAcknowledgement('preferred split', splitName, nextIdx, newAnswers);
  };

  const getAcknowledgement = async (qText, answer, nextIdx, allAnswers) => {"""
assert OLD_AFTER_SKIP in content, "after skip anchor not found"
content = content.replace(OLD_AFTER_SKIP, NEW_AFTER_SKIP, 1)

# ── 7. Add split picker render before the main chat return ────────────────────
OLD_CHAT_RETURN = """  /* ─── CHAT ─── */
  const q = (currentQ >= 0 && currentQ < QUESTIONS.length) ? QUESTIONS[currentQ] : null;

  return ("""
NEW_CHAT_RETURN = """  /* ─── SPLIT PICKER ─── */
  if (showSplitPicker) {
    const daysCount = parseInt(answers.trainingDays) || 3;
    const goal = answers.goal || '';
    return (
      <div style={{ background:'#0D0D0F', height:'100%', display:'flex', flexDirection:'column' }}>
        {/* Header */}
        <div style={{ flexShrink:0, padding:'52px 20px 12px', display:'flex', alignItems:'center', gap:10 }}>
          <div style={{ fontFamily:"'Bebas Neue',sans-serif", fontSize:32, color:'#C8FF00', letterSpacing:'0.08em' }}>FORGE</div>
          <div style={{ flex:1, marginLeft:8 }}>
            <p style={{ color:'#F5F5F0', fontWeight:700, fontSize:15, margin:0 }}>Choose Your Split</p>
            <p style={{ color:'#8A8A8E', fontSize:13, margin:0 }}>Tap a card to select</p>
          </div>
        </div>

        {/* Cards */}
        <div style={{ flex:1, overflowY:'auto', padding:'4px 16px 12px', display:'flex', flexDirection:'column', gap:10 }}>
          {SPLITS.map(split => {
            const badges = getSplitBadges(split.id, goal, daysCount);
            const active = selectedSplit === split.id;
            return (
              <button key={split.id} onClick={() => setSelectedSplit(split.id)}
                style={{ background: active ? 'rgba(200,255,0,0.07)' : '#1A1A1C', border: active ? '2px solid #C8FF00' : '1.5px solid #252527', borderRadius:16, padding:'14px 16px', textAlign:'left', cursor:'pointer', transition:'all 0.12s', position:'relative' }}>
                <div style={{ display:'flex', alignItems:'flex-start', justifyContent:'space-between', gap:8 }}>
                  <p style={{ fontFamily:"'Bebas Neue',sans-serif", fontSize:20, color: active ? '#C8FF00' : '#F5F5F0', margin:0, letterSpacing:'0.04em', lineHeight:1.1 }}>{split.id}</p>
                  {badges.length > 0 && (
                    <div style={{ display:'flex', flexDirection:'column', gap:4, flexShrink:0 }}>
                      {badges.map(b => (
                        <span key={b} style={{ fontSize:10, fontWeight:700, color:'#0D0D0F', background:'#C8FF00', borderRadius:99, padding:'3px 8px', whiteSpace:'nowrap' }}>{b}</span>
                      ))}
                    </div>
                  )}
                </div>
                <p style={{ color:'#8A8A8E', fontSize:13, margin:'5px 0 0', lineHeight:1.4 }}>{split.desc}</p>
              </button>
            );
          })}
        </div>

        {/* Confirm button */}
        <div style={{ flexShrink:0, padding:'12px 16px', paddingBottom:'max(20px, env(safe-area-inset-bottom))', borderTop:'1px solid #1A1A1C' }}>
          <button onClick={() => selectedSplit && handleSplitConfirm(selectedSplit)}
            disabled={!selectedSplit}
            style={{ width:'100%', padding:'18px 0', borderRadius:16, border:'none', background: selectedSplit ? '#C8FF00' : '#252527', color: selectedSplit ? '#0D0D0F' : '#8A8A8E', fontFamily:"'Bebas Neue',sans-serif", fontSize:20, letterSpacing:'0.08em', cursor: selectedSplit ? 'pointer' : 'not-allowed', transition:'background 0.12s, color 0.12s' }}>
            CONFIRM SPLIT
          </button>
        </div>
      </div>
    );
  }

  /* ─── CHAT ─── */
  const q = (currentQ >= 0 && currentQ < QUESTIONS.length) ? QUESTIONS[currentQ] : null;

  return ("""
assert OLD_CHAT_RETURN in content, "chat return anchor not found"
content = content.replace(OLD_CHAT_RETURN, NEW_CHAT_RETURN)

with open('forge.html', 'w', encoding='utf-8') as f:
    f.write(content)

sp = "type:'splitpicker'"
print("Done. Total lines:", content.count('\n'))
print("splitpicker type present:", sp in content)
print("SPLITS array present:", "const SPLITS = [" in content)
print("getSplitBadges present:", "getSplitBadges" in content)
print("showSplitPicker state present:", "showSplitPicker" in content)
print("handleSplitConfirm present:", "handleSplitConfirm" in content)
print("Split picker render present:", "CONFIRM SPLIT" in content)
