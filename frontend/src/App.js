import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    setLoading(true);
    setError("");
    setSummary("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/summarize", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text);
      }

      const data = await res.json();
      setSummary(data.summary);
    } catch (err) {
      console.error("Fetch error:", err);
      setError("Backend connection failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title"> AI Text & PDF Summarizer</h1>
      <p className="app-subtitle">
        Upload a TXT or PDF file to generate an AI-powered summary
      </p>

      <input
        type="file"
        className="file-input"
        accept=".txt,.pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        className="button"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Summarizing..." : "Summarize"}
      </button>

      {loading && <p className="loading">⏳ Generating summary...</p>}

      {error && <p className="error">{error}</p>}

      {summary && (
        <div className="summary-container">
          <h3 className="summary-title"> Summary</h3>
          <div className="summary-box">{summary}</div>
        </div>
      )}
    </div>
  );
}

export default App;
