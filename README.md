# Voice-Enabled Kubernetes RAG Assistant

## Overview

This project is a **voice-enabled question-answering assistant** built around the Kubernetes documentation. It combines **real-time speech-to-text**, a custom **hybrid Retrieval-Augmented Generation (RAG) pipeline**, and **Gemini** as a fallback when the documentation does not provide a sufficiently confident answer.

The system retrieves relevant Kubernetes documentation using both **semantic vector search** and **keyword-based search**, evaluates retrieval confidence, and generates grounded responses with relevant source information when available.

## Features

* **Real-Time Speech-to-Text** using the browser's speech recognition capabilities
* **Question Detection** to identify user questions from spoken input
* **Hybrid RAG Retrieval** combining semantic vector search and keyword matching
* **Retrieval Confidence Scoring** to determine whether retrieved documentation is reliable enough to answer from
* **Kubernetes Knowledge Base** built from Kubernetes documentation
* **Gemini Fallback** for questions that cannot be confidently answered from the knowledge base
* **Source-Aware Responses** with retrieved documentation metadata when available
* **FastAPI Backend** providing the query-processing API
* **React Frontend** providing the voice-enabled user interface

## Tech Stack

* **Frontend:** React, Vite, JavaScript
* **Backend:** Python, FastAPI
* **Speech-to-Text:** Browser Web Speech API
* **Embeddings:** Sentence Transformers
* **Embedding Model:** `all-MiniLM-L6-v2`
* **Retrieval:** Vector similarity + keyword matching
* **LLM Fallback:** Gemini
* **Knowledge Base:** Kubernetes documentation
* **API Communication:** REST

## Project Structure

```text
Raphael/
├── app/
│   ├── api/
│   │   └── main.py
│   ├── audio/
│   ├── llm/
│   ├── nlp/
│   ├── retrieval/
│   ├── scraper/
│   └── speech/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   └── package.json
│
├── knowledge_base/
│   └── Kubernetes/
│
├── tests/
├── requirements.txt
└── .gitignore
```

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/Vaibhav080/Raphael.git
cd Raphael
```

### 2. Create a Virtual Environment

```sh
python -m venv .venv
```

On Windows:

```sh
.venv\Scripts\activate
```

### 3. Install Python Dependencies

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit your `.env` file to GitHub.

### 5. Start the FastAPI Backend

From the project root:

```sh
uvicorn app.api.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

### 6. Start the React Frontend

Open another terminal:

```sh
cd frontend
npm install
npm run dev
```

The frontend will be available at the URL provided by Vite, typically:

```text
http://localhost:5173
```

## How It Works

### 1. Voice Input

The user activates the microphone and asks a question using natural language.

The frontend continuously captures the speech and converts it into text.

### 2. Question Processing

Once the user finishes speaking, the final transcript is sent to the FastAPI backend through the `/ask` endpoint.

### 3. Hybrid Retrieval

The backend searches the Kubernetes knowledge base using two retrieval approaches:

* **Vector Retrieval** — finds documentation that is semantically similar to the question.
* **Keyword Retrieval** — finds documentation containing relevant keywords.

The two scores are combined into a **hybrid retrieval score**.

### 4. Retrieval Confidence

The system evaluates the top retrieval score to determine whether the retrieved documentation is reliable enough to answer the question.

If confidence is sufficiently high, the retrieved Kubernetes documentation is passed to the answer-generation pipeline.

### 5. Gemini Fallback

If retrieval confidence is low, the system falls back to Gemini to generate a general response.

This allows the assistant to handle questions outside the available Kubernetes documentation rather than returning an unreliable documentation-grounded answer.

### 6. Response

The backend returns the generated answer along with the response source and retrieved source information when available.

## Example

A user can ask:

```text
"What is a Kubernetes ConfigMap?"
```

The system:

```text
Voice Input
     ↓
Speech-to-Text
     ↓
Question
     ↓
Hybrid Retrieval
     ↓
Confidence Evaluation
     ↓
 ┌───────────────┐
 │ High          │ Low
 ↓               ↓
Kubernetes RAG   Gemini Fallback
 ↓               ↓
Grounded Answer  General Answer
     └───────┬───────┘
             ↓
          Response
```

## API

### `POST /ask`

Accepts a natural-language question.

Request:

```json
{
  "query": "What is a Kubernetes ConfigMap?"
}
```

Response:

```json
{
  "answer": "A ConfigMap is...",
  "source": "rag",
  "confidence": "high",
  "sources": []
}
```

The `sources` field contains relevant documentation metadata when the response is generated from retrieved knowledge-base content.

## Future Enhancements

* Improve source attribution for fallback responses
* Add multi-turn conversation support
* Improve retrieval and confidence thresholds
* Add more Kubernetes documentation to the knowledge base
* Deploy the FastAPI backend and React frontend
* Add persistent conversation history
* Improve voice interaction and response playback
