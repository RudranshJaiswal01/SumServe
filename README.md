# SumServe — Document Summarization Service

SumServe is a simple, full-stack document summarization web application built as part of a take-home assignment.  
It allows users to upload a document or paste text and generate summaries in different styles using a Large Language Model (LLM).

The project focuses on **clean architecture, correctness, and clarity**, rather than feature breadth.

---

## Assignment Requirements Coverage

This project satisfies the assignment requirements as follows:

- **Accept text input**  
  ✔️ Text can be provided via a textarea or file upload (`.txt`, `.pdf`, `.docx`)

- **Integrate with an LLM API**  
  ✔️ Uses the Groq LLM API for summarization

- **Different summarization styles**  
  ✔️ Supports `brief`, `detailed`, and `bullet` summaries

- **Handle API errors gracefully**  
  ✔️ Backend validates input and handles LLM failures with clear error responses

- **Basic input validation**  
  ✔️ Empty input, invalid combinations, and oversized content are rejected

- **Simple web interface**  
  ✔️ A minimal Next.js frontend with clear UX constraints

---

## Features

- Upload documents (`.txt`, `.pdf`, `.docx`) or paste text directly
- Choose summarization style:
  - **Brief** — concise overview
  - **Detailed** — comprehensive summary
  - **Bullet** — structured bullet-point summary
- Markdown-formatted summaries (for readable bullet points and paragraphs)
- Backend-computed summary word count
- Copy-to-clipboard button for generated summaries
- Single-server production setup (backend serves the frontend)

---

## Tech Stack

### Backend
- **Python** — application logic
- **FastAPI** — API server
- **pdfplumber / python-docx** — document text extraction
- **Groq LLM API** — text summarization
- **Groq Cloud** — LLM inference platform (model options configurable via environment variables)

### Frontend
- **Next.js (App Router)** — UI framework
- **Tailwind CSS** — styling
- **react-markdown** — markdown rendering

---

## Project Structure

```
SumServe/
├── backend/
│ ├── app/
│ │ ├── routes/ # API routes
│ │ ├── services/ # Groq client
│ │ ├── utils/ # File parsing utilities
│ │ └── main.py
│ ├── static/ # Prebuilt frontend (production)
│ ├── tests/ # Backend tests
│ └── requirements.txt
│
├── frontend/ # Frontend source (Next.js)
│
├── README.md
└── .gitignore
```

---

## Design Decisions (Brief)

### 1. Single API Endpoint
A single `/api/summarize` endpoint handles both text and file input to keep the API surface minimal and aligned with the UI.

### 2. Text Extraction in Backend
Files are converted to plain text before being sent to the LLM.  
This ensures predictable input and avoids relying on undocumented multimodal behavior.

### 3. Strict JSON from LLM, Flexible Content
The LLM is required to return strict JSON with a single `summary` field, while markdown is allowed **inside** the summary for better structure (especially for bullet summaries).
This ensures predictable parsing while still allowing well-structured summaries.

### 4. Backend-Computed Word Count
Word count is calculated deterministically in the backend instead of relying on the LLM, ensuring correctness.

### 5. One-Server Production Setup
In development, frontend and backend run separately.  
In production, the frontend is statically built and served directly by FastAPI, resulting in a single server and port.

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API key

### Note: Groq Models

This project allows the Groq model to be configured via the `GROQ_MODEL` environment variable.

Available models and their specifications can be found in Groq’s official documentation:
https://console.groq.com/docs/models

---

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a .env file:

```env
GROQ_API_KEY=your_api_key_here

# Optional configuration
GROQ_MODEL=llama-3.1-8b-instant
GROQ_TIMEOUT=30
```
- `GROQ_MODEL` controls which Groq-hosted model is used for summarization
- `GROQ_TIMEOUT` specifies the request timeout (in seconds)

_If not provided, the application uses sensible defaults._

Run the backend:

```bash
uvicorn app.main:app --reload
```

### Frontend Setup (Development)
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

`http://localhost:3000`

Backend runs at:

`http://localhost:8000`

## Production Build (Single Server)

```bash
cd frontend
npm run build
```

Copy the build output:

```bash
cp -r out/* ../backend/static/
```

Run backend only:

```bash
cd backend
uvicorn app.main:app
```

App will be available at:

`http://localhost:8000`

### Running Tests

```bash
cd backend
export GROQ_API_KEY=dummy   # Required for startup
pytest
```

## Limitations:

- No authentication or user management

- No streaming summaries

- No multilingual support

- No persistence of summaries

These were intentionally omitted to keep the scope focused and aligned with the assignment.

## Summary
*SumServe* is a focused implementation of a document summarisation service that prioritises:
- correctness
- simplicity
- clear separation of concerns
- honest trade-offs

_The goal of this project is not to be feature-complete, but to demonstrate solid engineering fundamentals when integrating LLMs into a web application._

---
