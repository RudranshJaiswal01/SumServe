"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";


type Style = "brief" | "detailed" | "bullet";

export default function Page() {
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [style, setStyle] = useState<Style>("brief");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [wordCount, setWordCount] = useState<number | null>(null);

  const MAX_CHARS = 12000;
  const charCount = text.length;
  const isOverLimit = charCount > MAX_CHARS;


  const isSubmitDisabled = loading || (!file && text.trim().length === 0) || isOverLimit;


  async function handleSubmit() {
    setLoading(true);
    setError(null);
    setSummary(null);
    setWordCount(null);

    const formData = new FormData();
    formData.append("style", style);

    if (file) {
      formData.append("file", file);
    } else {
      formData.append("text", text);
    }

    try {
      const res = await fetch("/api/summarize", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Summarization failed");
      }

      setSummary(data.summary);
      setWordCount(data.word_count);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleCopy() {
    if (!summary) return;
    navigator.clipboard.writeText(summary);
  }


  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-2xl bg-white rounded-xl shadow-sm p-6">
        <h1 className="text-2xl font-semibold mb-1">SumServe</h1>
        <p className="text-gray-500 mb-5">
          Simple document summarization service
        </p>

        {/* Text Input */}
        <textarea
          className="w-full border rounded-lg p-3 mb-1 disabled:bg-gray-100"
          rows={6}
          placeholder="Paste document text here…"
          value={text}
          disabled={!!file}
          onChange={(e) => setText(e.target.value)}
        />

        <div className="flex justify-between text-sm text-gray-500 mb-3">
          <span>
            {charCount} / {MAX_CHARS} characters
          </span>

          {isOverLimit && (
            <span className="text-red-600">
              Reduce text to enable summarization
            </span>
          )}
        </div>

        {/* File Upload */}
        <input
          type="file"
          accept=".txt,.pdf,.docx"
          disabled={text.trim().length > 0}
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="mb-4 block"
        />

        {/* Style Selector */}
        <div className="flex gap-4 mb-4 text-sm">
          {(["brief", "detailed", "bullet"] as Style[]).map((s) => (
            <label key={s} className="flex items-center gap-1">
              <input
                type="radio"
                name="style"
                value={s}
                checked={style === s}
                onChange={() => setStyle(s)}
              />
              {s}
            </label>
          ))}
        </div>

        {/* Submit Button */}
        <button
          onClick={handleSubmit}
          disabled={isSubmitDisabled}
          className="w-full bg-black text-white py-2 rounded-lg disabled:opacity-50"
        >
          {loading ? "Summarizing…" : "Summarize"}
        </button>

        {/* Error */}
        {error && (
          <p className="text-red-600 text-sm mt-3">{error}</p>
        )}

        {/* Output */}
        {summary && (
          <div className="mt-4">
            <div className="flex justify-end mb-2">
              <button
                onClick={handleCopy}
                className="text-sm text-gray-600 hover:text-black"
                >
                Copy summary
              </button>
            </div>

            <div className="bg-gray-100 rounded-lg p-4 prose prose-sm max-w-none">
              <ReactMarkdown>
                {summary}
              </ReactMarkdown>
            </div>
          </div>
        )}
        {summary && wordCount !== null && (
          <p className="mt-2 text-sm text-gray-500">
            Summary word count: {wordCount}
          </p>
        )}

      </div>
    </main>
  );
}
