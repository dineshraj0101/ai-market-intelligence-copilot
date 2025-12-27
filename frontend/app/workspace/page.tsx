"use client";

import { useState } from "react";
import Card from "../components/Card";

export default function WorkspacePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [hasError, setHasError] = useState(false);

  const handleAnalyze = () => {
    setHasError(false);
    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      setHasError(true); // simulate an error
    }, 1200);
  };

  return (
    <main style={{ padding: "40px", maxWidth: "800px" }}>
      <h1>Workspace</h1>

      <p>Enter a US stock ticker to begin.</p>

      <div style={{ display: "flex", gap: "12px", marginTop: "16px" }}>
        <input
          type="text"
          placeholder="e.g. AAPL"
          disabled={isLoading}
          style={{
            flex: 1,
            padding: "12px",
            fontSize: "16px",
            border: "1px solid #ccc",
            borderRadius: "8px",
            opacity: isLoading ? 0.6 : 1,
          }}
        />
        <button
          onClick={handleAnalyze}
          disabled={isLoading}
          style={{
            padding: "12px 16px",
            fontSize: "16px",
            borderRadius: "8px",
            border: "1px solid #111",
            background: "#111",
            color: "#fff",
            cursor: isLoading ? "not-allowed" : "pointer",
            opacity: isLoading ? 0.7 : 1,
          }}
        >
          {isLoading ? "Loading..." : "Analyze"}
        </button>
      </div>

      {isLoading && (
        <p style={{ marginTop: "16px", color: "#555" }}>
          Fetching data and preparing your 7-card snapshot...
        </p>
      )}

      {hasError && (
        <p style={{ marginTop: "16px", color: "#b00020" }}>
          Unable to retrieve data. Please check the ticker and try again.
        </p>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr",
          gap: "16px",
          marginTop: "32px",
          opacity: isLoading ? 0.6 : 1,
        }}
      >
        <Card title="1. What is happening?" />
        <Card title="2. Is participation changing?" />
        <Card title="3. What macro forces matter now?" />
        <Card title="4. Is the business improving or deteriorating?" />
        <Card title="5. Is this stock winning vs alternatives?" />
        <Card title="6. Can I trust what I’m seeing?" />
        <Card title="7. Intelligence brief" />
      </div>
    </main>
  );
}