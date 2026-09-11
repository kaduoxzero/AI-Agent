import { useEffect, useMemo, useState } from 'react'

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

const scenarioNumber = (index) => String(index + 1).padStart(2, '0')

function Landing({ scenarios, onStart, loading }) {
  const [selected, setSelected] = useState(null)

  return (
    <main className="landing-shell">
      <section className="hero-copy">
        <div className="brand-mark">AG</div>
        <p className="brand-name">ARMCHAIR GENERAL</p>
        <h1>纸上靶场</h1>
        <p className="hero-lead">
          不是干巴巴的问答，而是一场会记住你本局行动、会改变世界状态的推演。
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

function Game({ scenario, session, setSession, onExit }) {
  const [input, setInput] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [terminal, setTerminal] = useState(() =>
    session.events.map((event) => ({ type: event.kind, text: event.text })),
  )

  const quickCommands = useMemo(
    () => [
      `nmap -p- ${session.target_ip}`,
      `curl http://${session.target_ip}`,
      `ssh ${scenario.ssh_user}@${session.target_ip}`,
      'status',
    ],
    [scenario.ssh_user, session.target_ip],
  )

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
      setSession(payload.session)
      setTerminal((lines) => [...lines, { type: 'output', text: payload.output }])
    } catch (err) {
      setError(err.message)
      setTerminal((lines) => [...lines, { type: 'error', text: err.message }])
    } finally {
      setBusy(false)
    }
  }

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
          <small>{session.id.slice(0, 8)}</small>
        </div>
        <button className="ghost compact" onClick={onExit}>新战役</button>
      </header>

      <section className="game-grid">
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
          <ObjectiveList scenario={scenario} session={session} />
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
              <pre key={`${line.type}-${index}`} className={`line-${line.type}`}>{line.text}</pre>
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
          <div className="intel-section">
            <h3>已发现线索</h3>
            {session.clues.length === 0 ? (
              <p className="empty">还没有线索。世界会根据你的行动逐步暴露信息。</p>
            ) : (
              <ul>{session.clues.map((clue) => <li key={clue}>{clue}</li>)}</ul>
            )}
          </div>
          <div className="intel-section">
            <h3>场景事件</h3>
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
            <small>负责把你的意图映射成模拟动作，而不是向真实网络发包。</small>
          </div>
        </aside>
      </section>

      {session.status === 'completed' && (
        <section className="mission-complete" role="dialog" aria-modal="true">
          <p>MISSION COMPLETE</p>
          <h2>{scenario.name}</h2>
          <code>{session.flag}</code>
          <span>本局状态仍保留到容器结束。开启新战役会创建新的 Session。</span>
          <button className="primary" onClick={onExit}>开始新战役</button>
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
