import { useEffect, useMemo, useRef, useState } from 'react'

const api = async (path, options = {}) => {
  const response = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed: ${response.status}`)
  }
  if (response.status === 204) return null
  return response.json()
}

const STORY_STEPS = [
  { id: 'recon', label: 'RECON', title: '端口侦察' },
  { id: 'web-investigation', label: 'WEB', title: 'Web 初查' },
  { id: 'approach-decision', label: 'BRANCH', title: '调查方式' },
  { id: 'path-enumeration', label: 'PATH', title: '路径枚举' },
  { id: 'evidence-review', label: 'EVIDENCE', title: '证据读取' },
  { id: 'access-validation', label: 'ACCESS', title: '访问验证' },
  { id: 'complete', label: 'DONE', title: '战役完成' },
]

const STREAM_LABELS = {
  connecting: 'CONNECTING',
  live: 'LIVE',
  reconnecting: 'RECONNECTING',
  complete: 'COMPLETE',
  closed: 'CLOSED',
}

const scenarioNumber = (index) => String(index + 1).padStart(2, '0')
const maxEventSeq = (events) => events.reduce((max, event) => Math.max(max, event.seq || 0), 0)

function Landing({ scenarios, onStart, loading }) {
  const [selected, setSelected] = useState(null)

  return (
    <main className="landing-shell">
      <section className="hero-copy">
        <div className="brand-mark">AG</div>
        <p className="brand-name">ARMCHAIR GENERAL</p>
        <h1>纸上靶场</h1>
        <p className="hero-lead">
          不是干巴巴的问答，而是一场会记住你本局行动、会改变世界状态，并在结束后告诉你哪里还能更好的推演。
        </p>
        <div className="hero-actions">
          <button className="primary" disabled={loading} onClick={() => onStart(selected)}>
            {selected ? '进入所选战役' : '随机进入战役'}
          </button>
          {selected && (
            <button className="ghost" disabled={loading} onClick={() => setSelected(null)}>
              改为随机
            </button>
          )}
        </div>
        <p className="ephemeral-note">容器关闭后，本局记忆永久消失。再次启动就是一个新世界。</p>
      </section>

      <section className="scenario-rail" aria-label="战役选择">
        <div className="section-heading">
          <div>
            <p>CHOOSE YOUR OPERATION</p>
            <h2>选择你的战役</h2>
          </div>
          <span>{scenarios.length} 个可用场景</span>
        </div>
        <div className="scenario-list">
          {scenarios.map((scenario, index) => {
            const active = selected === scenario.id
            return (
              <button
                key={scenario.id}
                className={`scenario-row ${active ? 'active' : ''}`}
                onClick={() => setSelected(active ? null : scenario.id)}
              >
                <span className="scenario-index">{scenarioNumber(index)}</span>
                <span className="scenario-main">
                  <strong>{scenario.name}</strong>
                  <small>{scenario.subtitle}</small>
                </span>
                <span className="scenario-meta">
                  <b>{scenario.difficulty}</b>
                  <small>{scenario.category}</small>
                </span>
              </button>
            )
          })}
        </div>
      </section>
    </main>
  )
}

function ObjectiveList({ scenario, session }) {
  return (
    <div className="objective-list">
      {scenario.objectives.map((objective, index) => {
        const complete = session.completed_objectives.includes(objective.id)
        const active = !complete && index === session.objective_index
        return (
          <div key={objective.id} className={`objective ${complete ? 'complete' : ''} ${active ? 'active' : ''}`}>
            <span className="objective-box">{complete ? '✓' : index + 1}</span>
            <div>
              <strong>{objective.title}</strong>
              <small>{objective.description}</small>
            </div>
          </div>
        )
      })}
    </div>
  )
}

function MetricStrip({ session }) {
  return (
    <div className="metric-strip">
      <div><span>SCORE</span><strong>{session.score}</strong></div>
      <div><span>ACTIONS</span><strong>{session.action_count}</strong></div>
      <div><span>HINTS</span><strong>{session.hint_count}</strong></div>
      <div><span>INVALID</span><strong>{session.invalid_action_count}</strong></div>
    </div>
  )
}

function StoryGraph({ session, busy, onChoose }) {
  const currentIndex = Math.max(0, STORY_STEPS.findIndex((step) => step.id === session.story_node))
  const branchReady = session.story_node === 'approach-decision' && !session.story_branch

  return (
    <section className="story-graph-card" aria-label="Story Graph">
      <div className="story-graph-heading">
        <div>
          <span>STORY GRAPH</span>
          <strong>{session.story_node}</strong>
        </div>
        <em>{session.story_branch ? `LOCKED · ${session.story_branch.toUpperCase()}` : 'UNLOCKED'}</em>
      </div>

      <div className="story-path">
        {STORY_STEPS.map((step, index) => {
          const state = index < currentIndex ? 'complete' : index === currentIndex ? 'active' : 'pending'
          return (
            <div className={`story-node ${state}`} key={step.id}>
              <span className="story-node-dot">{index < currentIndex ? '✓' : index + 1}</span>
              <div>
                <small>{step.label}</small>
                <strong>{step.title}</strong>
              </div>
            </div>
          )
        })}
      </div>

      {branchReady && (
        <div className="branch-choice">
          <p>调查方式节点已解锁。选择会写入当前 WorldState，本局不可回滚。</p>
          <div>
            <button disabled={busy} onClick={() => onChoose('approach focused')}>
              <span>FOCUSED</span>
              <strong>定向调查</strong>
              <small>低噪声 · 0 分损耗</small>
            </button>
            <button disabled={busy} onClick={() => onChoose('approach broad')}>
              <span>BROAD</span>
              <strong>广覆盖调查</strong>
              <small>更多路径 · -3 分</small>
            </button>
          </div>
        </div>
      )}

      <div className="world-state-grid">
        <div>
          <span>WORLD TAGS</span>
          <div className="tag-list">
            {session.world_tags.map((tag) => <code key={tag}>{tag}</code>)}
          </div>
        </div>
        <div>
          <span>CONSEQUENCES</span>
          {session.consequences.length === 0 ? (
            <p>尚未产生不可回滚后果。</p>
          ) : (
            <ul>{session.consequences.slice(-3).map((item) => <li key={item}>{item}</li>)}</ul>
          )}
        </div>
      </div>
    </section>
  )
}

function LearningReport({ report }) {
  if (!report) return <div className="report-loading">正在生成学习报告...</div>
  return (
    <div className="learning-report">
      <div className="grade-box">
        <span>GRADE</span>
        <strong>{report.grade}</strong>
        <small>{report.score} / 100</small>
      </div>
      <div className="report-copy">
        <section>
          <h3>做得好的地方</h3>
          <ul>{report.strengths.map((item) => <li key={item}>{item}</li>)}</ul>
        </section>
        <section>
          <h3>下一步训练</h3>
          <ul>{report.next_steps.map((item) => <li key={item}>{item}</li>)}</ul>
        </section>
      </div>
    </div>
  )
}

function Game({ scenario, session, setSession, onExit }) {
  const [input, setInput] = useState('')
  const [busy, setBusy] = useState(false)
  const [hintBusy, setHintBusy] = useState(false)
  const [error, setError] = useState('')
  const [lastHint, setLastHint] = useState('')
  const [report, setReport] = useState(null)
  const [streamState, setStreamState] = useState('connecting')
  const streamSeq = useRef(maxEventSeq(session.events))
  const [terminal, setTerminal] = useState(() =>
    session.events.map((event) => ({ type: event.kind, text: event.text, eventSeq: event.seq })),
  )

  const branchReady = session.story_node === 'approach-decision' && !session.story_branch
  const quickCommands = useMemo(() => {
    const commands = [
      `nmap -p- ${session.target_ip}`,
      `curl http://${session.target_ip}`,
    ]
    if (branchReady) {
      commands.push('approach focused', 'approach broad')
    }
    commands.push(`dirsearch -u http://${session.target_ip}`)
    commands.push(`ssh ${scenario.ssh_user}@${session.target_ip}`)
    commands.push('status')
    return commands
  }, [branchReady, scenario.ssh_user, session.target_ip])

  const mergeResponseSession = (nextSession) => {
    setSession((current) => {
      if (!current || current.id !== nextSession.id) return nextSession
      return { ...nextSession, events: current.events }
    })
  }

  const loadReport = async () => {
    try {
      const payload = await api(`/api/sessions/${session.id}/report`)
      setReport(payload)
    } catch (err) {
      setError(err.message)
    }
  }

  const execute = async (command) => {
    const value = command.trim()
    if (!value || busy) return
    setBusy(true)
    setError('')
    setInput('')
    setTerminal((lines) => [...lines, { type: 'command', text: `root@paper-range:~$ ${value}` }])
    try {
      const payload = await api(`/api/sessions/${session.id}/actions`, {
        method: 'POST',
        body: JSON.stringify({ input: value }),
      })
      mergeResponseSession(payload.session)
      setTerminal((lines) => [
        ...lines,
        { type: 'intent', text: `[intent:${payload.intent.kind} source:${payload.intent.source}]` },
        { type: 'output', text: payload.output },
      ])
      if (payload.session.status === 'completed') {
        const finalReport = await api(`/api/sessions/${session.id}/report`)
        setReport(finalReport)
      }
    } catch (err) {
      setError(err.message)
      setTerminal((lines) => [...lines, { type: 'error', text: err.message }])
    } finally {
      setBusy(false)
    }
  }

  const requestHint = async () => {
    if (hintBusy || session.status === 'completed') return
    setHintBusy(true)
    setError('')
    try {
      const payload = await api(`/api/sessions/${session.id}/hint`, { method: 'POST', body: '{}' })
      mergeResponseSession(payload.session)
      setLastHint(payload.hint)
      setTerminal((lines) => [...lines, { type: 'hint', text: `[Hint -${payload.cost}] ${payload.hint}` }])
    } catch (err) {
      setError(err.message)
    } finally {
      setHintBusy(false)
    }
  }

  useEffect(() => {
    streamSeq.current = maxEventSeq(session.events)
    const source = new EventSource(`/api/sessions/${session.id}/events?after=${streamSeq.current}`)

    source.onopen = () => setStreamState('live')
    source.addEventListener('game_event', (message) => {
      try {
        const event = JSON.parse(message.data)
        if (!event.seq || event.seq <= streamSeq.current) return
        streamSeq.current = event.seq

        setSession((current) => {
          if (!current || current.id !== session.id) return current
          if (current.events.some((item) => item.seq === event.seq)) return current
          return { ...current, events: [...current.events, event] }
        })

        if (event.kind !== 'tool') {
          setTerminal((lines) => {
            if (lines.some((line) => line.eventSeq === event.seq)) return lines
            return [...lines, { type: event.kind, text: `[LIVE #${event.seq}] ${event.text}`, eventSeq: event.seq }]
          })
        }
      } catch {
        setStreamState('reconnecting')
      }
    })
    source.addEventListener('session_complete', () => {
      setStreamState('complete')
      source.close()
    })
    source.addEventListener('session_end', () => {
      setStreamState('closed')
      source.close()
    })
    source.onerror = () => {
      setStreamState(source.readyState === EventSource.CLOSED ? 'closed' : 'reconnecting')
    }

    return () => source.close()
  }, [session.id, setSession])

  useEffect(() => {
    if (session.status === 'completed' && !report) loadReport()
  }, [session.status])

  const recentNarrative = session.events.filter((event) => event.kind !== 'tool').slice(-6)
  const progress = Math.round((session.completed_objectives.length / scenario.objectives.length) * 100)

  return (
    <main className={`game-shell theme-${session.theme_id}`}>
      <header className="game-header">
        <div className="game-brand">
          <div className="brand-mark small">AG</div>
          <div>
            <span>PAPER RANGE</span>
            <strong>{scenario.name}</strong>
          </div>
        </div>
        <div className="game-status">
          <span className={`status-dot ${session.status}`}></span>
          {session.status === 'completed' ? '已完成' : '进行中'}
          <span className={`stream-pill ${streamState}`}>SSE {STREAM_LABELS[streamState] || streamState}</span>
          <small>SCORE {session.score}</small>
          <small>{session.id.slice(0, 8)}</small>
        </div>
        <button className="ghost compact" onClick={onExit}>新战役</button>
      </header>

      <MetricStrip session={session} />

      <section className="game-grid learning-grid">
        <aside className="story-panel panel">
          <p className="panel-label">MISSION BRIEF</p>
          <h2>{scenario.name}</h2>
          <p>{scenario.briefing}</p>
          <div className="progress-block">
            <div className="progress-copy">
              <span>任务进度</span>
              <strong>{progress}%</strong>
            </div>
            <div className="progress-track"><span style={{ width: `${progress}%` }} /></div>
          </div>
          <StoryGraph session={session} busy={busy} onChoose={execute} />
          <ObjectiveList scenario={scenario} session={session} />
          <div className="hint-block">
            <button className="hint-button" disabled={hintBusy || session.status === 'completed'} onClick={requestHint}>
              {hintBusy ? '获取中...' : '请求 Hint · -10 分'}
            </button>
            {lastHint && <p>{lastHint}</p>}
          </div>
        </aside>

        <section className="terminal-panel panel">
          <div className="terminal-topbar">
            <div>
              <span className="traffic red"></span>
              <span className="traffic amber"></span>
              <span className="traffic green"></span>
            </div>
            <span>SIMULATED TERMINAL · {session.target_ip}</span>
          </div>

          <div className="terminal-log" aria-live="polite">
            {terminal.map((line, index) => (
              <pre key={`${line.type}-${line.eventSeq || index}`} className={`line-${line.type}`}>{line.text}</pre>
            ))}
            {busy && <pre className="line-agent">[Agent] 正在解释你的行动并更新世界状态...</pre>}
          </div>

          <div className="quick-actions">
            {quickCommands.map((command) => (
              <button key={command} disabled={busy || session.status === 'completed'} onClick={() => execute(command)}>
                {command}
              </button>
            ))}
          </div>

          <form
            className="command-form"
            onSubmit={(event) => {
              event.preventDefault()
              execute(input)
            }}
          >
            <span>›</span>
            <input
              value={input}
              disabled={busy || session.status === 'completed'}
              onChange={(event) => setInput(event.target.value)}
              placeholder="输入自然语言或模拟命令，例如：我先扫描所有 TCP 端口"
              autoFocus
            />
            <button className="primary compact" disabled={busy || !input.trim() || session.status === 'completed'}>
              执行
            </button>
          </form>
          {error && <p className="error-text">{error}</p>}
        </section>

        <aside className="intel-panel panel">
          <p className="panel-label">LIVE INTEL</p>
          <div className="live-stream-card">
            <span className={`stream-beacon ${streamState}`}></span>
            <div>
              <small>EVENT STREAM</small>
              <strong>{STREAM_LABELS[streamState] || streamState}</strong>
            </div>
            <code>#{streamSeq.current}</code>
          </div>
          <div className="intel-section">
            <h3>已发现线索</h3>
            {session.clues.length === 0 ? (
              <p className="empty">还没有线索。世界会根据你的行动逐步暴露信息。</p>
            ) : (
              <ul>{session.clues.map((clue) => <li key={clue}>{clue}</li>)}</ul>
            )}
          </div>
          <div className="intel-section">
            <h3>实时场景事件</h3>
            <div className="event-stream">
              {recentNarrative.map((event) => (
                <div key={event.seq} className={`event ${event.kind}`}>
                  <span>#{event.seq}</span>
                  <p>{event.text}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="agent-card">
            <span>当前 Agent</span>
            <strong>Security Analyst</strong>
            <small>自然语言和命令先归一化为 Typed Action Intent；SSE 只推送模拟世界事件，不会向真实网络发包。</small>
          </div>
        </aside>
      </section>

      {session.status === 'completed' && (
        <section className="mission-complete report-modal" role="dialog" aria-modal="true">
          <p>MISSION COMPLETE</p>
          <h2>{scenario.name}</h2>
          <code>{session.flag}</code>
          <LearningReport report={report} />
          <div className="complete-actions">
            <button className="ghost" onClick={loadReport}>刷新报告</button>
            <button className="primary" onClick={onExit}>开始新战役</button>
          </div>
        </section>
      )}
    </main>
  )
}

export default function App() {
  const [scenarios, setScenarios] = useState([])
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api('/api/scenarios')
      .then(setScenarios)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const start = async (scenarioId) => {
    setLoading(true)
    setError('')
    try {
      const next = await api('/api/sessions', {
        method: 'POST',
        body: JSON.stringify({ scenario_id: scenarioId || null }),
      })
      setSession(next)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const scenario = session ? scenarios.find((item) => item.id === session.scenario_id) : null

  if (loading && scenarios.length === 0) {
    return <div className="boot-screen">PAPER RANGE // INITIALIZING WORLD...</div>
  }

  if (error && scenarios.length === 0) {
    return <div className="boot-screen error">无法连接纸上靶场后端：{error}</div>
  }

  return (
    <div className="app-root">
      {session && scenario ? (
        <Game scenario={scenario} session={session} setSession={setSession} onExit={() => setSession(null)} />
      ) : (
        <Landing scenarios={scenarios} onStart={start} loading={loading} />
      )}
      {error && scenarios.length > 0 && <div className="toast-error">{error}</div>}
    </div>
  )
}
