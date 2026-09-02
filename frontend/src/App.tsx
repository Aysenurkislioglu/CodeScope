import { useState, type FormEvent } from 'react'
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

  return <main className="workspace">
    <header className="topbar"><a className="brand" href="/">RepoLens<span>.</span></a><p>Codebase intelligence, starting with a clean scan.</p><button type="button" className="settings">Settings</button></header>
    <section className="hero-card">
      <p className="eyebrow">Repository scanner · MVP</p>
      <h1>Understand a codebase before you ask it anything.</h1>
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
}

function Metric({ label, value }: { label: string; value: number }) { return <div><strong>{value}</strong><span>{label}</span></div> }

export default App
