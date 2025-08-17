"use client";

import { useState } from "react";

export default function Home() {
  const [pdf, setPdf] = useState<File | null>(null);
  const [methodology, setMethodology] = useState<string>("");
  const [pseudocode, setPseudocode] = useState<string>("");
  const [code, setCode] = useState<string>("");
  const [runOut, setRunOut] = useState<string>("");
  const [provider, setProvider] = useState<string>("gemini");
  const [apiKey, setApiKey] = useState<string>("");

  const uploadPdf = async () => {
    if (!pdf) return;
    const fd = new FormData();
    fd.append("file", pdf);
    const res = await fetch("/api/papers/parse", { method: "POST", body: fd });
    const data = await res.json();
    setMethodology(data.methodology ?? "");
  };

  const genPseudo = async () => {
    const res = await fetch("/api/pseudocode/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ methodology, provider, api_key: apiKey }),
    });
    const data = await res.json();
    setPseudocode(data.pseudocode ?? "");
  };

  const genCode = async () => {
    const res = await fetch("/api/codegen/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pseudocode, framework: "pytorch", provider, api_key: apiKey }),
    });
    const data = await res.json();
    setCode(data.code ?? "");
  };

  const run = async () => {
    const res = await fetch("/api/experiment/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const data = await res.json();
    setRunOut(`${data.returncode}\n${data.stdout}\n${data.stderr}`);
  };

  return (
    <div style={{ maxWidth: 900, margin: "20px auto", padding: 16 }}>
      <h1>METASCRIBE</h1>
      <p>AI Agent for Research Paper Implementation (MVP)</p>

      <section style={{ marginTop: 16 }}>
        <h3>LLM Settings</h3>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <label>
            Provider:
            <select value={provider} onChange={(e) => setProvider(e.target.value)} style={{ marginLeft: 6 }}>
              <option value="gemini">Gemini</option>
            </select>
          </label>
          <input
            type="password"
            placeholder="API Key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            style={{ flex: 1 }}
          />
        </div>
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>1. Upload PDF</h3>
        <input type="file" accept="application/pdf" onChange={(e) => setPdf(e.target.files?.[0] ?? null)} />
        <button onClick={uploadPdf} disabled={!pdf} style={{ marginLeft: 8 }}>Parse</button>
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>2. Methodology</h3>
        <textarea value={methodology} onChange={(e) => setMethodology(e.target.value)} rows={6} style={{ width: "100%" }} />
        <button onClick={genPseudo} disabled={!methodology}>Generate pseudocode</button>
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>3. Pseudocode</h3>
        <textarea value={pseudocode} onChange={(e) => setPseudocode(e.target.value)} rows={8} style={{ width: "100%" }} />
        <button onClick={genCode} disabled={!pseudocode}>Generate code</button>
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>4. Generated Code</h3>
        <textarea value={code} onChange={(e) => setCode(e.target.value)} rows={12} style={{ width: "100%", fontFamily: "monospace" }} />
        <button onClick={run} disabled={!code}>Run</button>
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>5. Run Output</h3>
        <pre style={{ whiteSpace: "pre-wrap", background: "#111", color: "#0f0", padding: 12 }}>{runOut}</pre>
      </section>
    </div>
  );
}
