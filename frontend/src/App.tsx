import { useEffect, useState, type FormEvent } from 'react'
import './App.css'

type ScanResult = {
  repository: { name: string; summary: { files_detected: number; code_files: number; documentation_files: number; ignored_entries: number } }
  files: Array<{ path: string; kind: 'code' | 'documentation'; language: string | null }>
}

function App() {
  const [path, setPath] = useState('')
  const [result, setResult] = useState<ScanResult | null>(null)
  const [error, setError] = useState('')
  const [isScanning, setIsScanning] = useState(false)
  const [showIntro, setShowIntro] = useState(true)

  useEffect(() => {
    const timer = window.setTimeout(() => setShowIntro(false), 2100)
    return () => window.clearTimeout(timer)
  }, [])

  async function scanRepository(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!path.trim()) { setError('Enter the absolute path to a local repository.'); return }
    setIsScanning(true); setError(''); setResult(null)
    try {
      const response = await fetch('http://127.0.0.1:8000/api/repositories', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ local_path: path.trim() }) })
      const payload = await response.json()
      if (!response.ok) throw new Error(payload.detail ?? 'Repository indexing failed.')
      setResult(payload)
    } catch (scanError) {
      setError(scanError instanceof Error ? scanError.message : 'Repository indexing failed.')
    } finally { setIsScanning(false) }
  }

  return <>
    {showIntro && <Intro />}
    <main className="workspace">
      <header className="topbar">
        <a className="brand" href="/" aria-label="CodeScope home"><TelescopeIcon /><span>CodeScope</span></a>
        <p>Codebase intelligence, brought into focus.</p>
        <button type="button" className="settings">Settings</button>
      </header>
      <section className="hero-card">
        <p className="eyebrow">Repository scanner · MVP</p>
        <h1>Bring your codebase into focus.</h1>
        <p className="lede">Add a local repository to map its supported code and documentation files. Secrets, dependencies, and binary files stay out.</p>
        <form onSubmit={scanRepository} className="scan-form">
          <label htmlFor="repository-path">Local repository path</label>
          <div className="input-row"><input id="repository-path" value={path} onChange={(event) => setPath(event.target.value)} placeholder="/Users/you/projects/my-repository" autoComplete="off" /><button type="submit" disabled={isScanning}>{isScanning ? 'Scanning…' : 'Scan repository'}</button></div>
          <small>GitHub import, semantic indexing, and AI chat follow in later milestones.</small>
        </form>
        {error && <p className="error" role="alert">{error}</p>}
      </section>
      {result && <section className="results" aria-live="polite">
        <div className="result-heading"><div><p className="eyebrow success">Repository ready</p><h2>{result.repository.name}</h2></div><p>{result.repository.summary.ignored_entries} unsafe or unsupported entries skipped</p></div>
        <div className="metrics"><Metric label="Files detected" value={result.repository.summary.files_detected} /><Metric label="Code files" value={result.repository.summary.code_files} /><Metric label="Documentation" value={result.repository.summary.documentation_files} /></div>
        <div className="file-list">{result.files.slice(0, 8).map((file) => <div className="file" key={file.path}><span>{file.path}</span><span>{file.language ?? file.kind}</span></div>)}{result.files.length > 8 && <p className="more">+ {result.files.length - 8} more files</p>}</div>
      </section>}
    </main>
  </>
}

function Intro() {
  return <div className="intro" role="status" aria-label="Opening CodeScope">
    <div className="intro-grid" />
    <div className="intro-glow" />
    <div className="intro-optic"><div className="optic-ring ring-one" /><div className="optic-ring ring-two" /><div className="optic-crosshair" /><div className="optic-focus" /><TelescopeIcon /></div>
    <p><span>CodeScope</span><i>Scanning the horizon</i></p>
  </div>
}

function TelescopeIcon() {
  return <svg className="telescope-icon" viewBox="0 0 64 64" fill="none" aria-hidden="true">
    <path d="m17 24 27-10 6 16-27 10z" stroke="currentColor" strokeWidth="4.5" strokeLinejoin="round" />
    <path d="m44 14 8-3 6 16-8 3M31 37l-5 16m8-17 12 12m-7-17-2 18M13 30l10-4" stroke="currentColor" strokeWidth="4.5" strokeLinecap="round" strokeLinejoin="round" />
    <circle cx="18" cy="29" r="3" fill="currentColor" />
  </svg>
}

function Metric({ label, value }: { label: string; value: number }) { return <div><strong>{value}</strong><span>{label}</span></div> }

export default App
