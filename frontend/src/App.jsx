import { useState, useRef } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const[voiceSupported, setVoiceSupported] = useState(true);

  const recognitionRef = useRef(null);
  const transcriptRef = useRef("");

  const askQuestion = async (question = query) => {
    console.log("📤 Asking question:", question);
    if (!question.trim() || loading) {
      console.log("❌ Question empty or already loading");
      return;
    }

    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: question.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data = await response.json();

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      console.error(error);
      setAnswer(
        "Something went wrong while contacting the Kubernetes assistant."
      );
    } finally {
      setLoading(false);
    }
  };

  const startListening = () => {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    setVoiceSupported(false);
    return;
  }

  if (isListening) {
    recognitionRef.current?.stop();
    return;
  }

  const recognition = new SpeechRecognition();

  recognition.lang = "en-IN";
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.maxAlternatives = 3;

  transcriptRef.current = "";

  recognition.onstart = () => {
    console.log("🎙️ Microphone started");
    setIsListening(true);
  };

  recognition.onresult = (event) => {
    let finalTranscript = "";
    let interimTranscript = "";

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;

      if (event.results[i].isFinal) {
        finalTranscript += transcript + " ";
      } else {
        interimTranscript += transcript;
      }
    }

    if (finalTranscript) {
      transcriptRef.current += finalTranscript;
    }

    const currentTranscript = (
      transcriptRef.current + interimTranscript
    ).trim();

    console.log("🎙️ Transcript:", currentTranscript);

    setQuery(currentTranscript);
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    setIsListening(false);
  };

  recognition.onend = () => {
    console.log("🎙️ Microphone stopped");

    setIsListening(false);

    const finalQuestion = transcriptRef.current.trim();

    console.log("✅ Final transcript:", finalQuestion);

    if (finalQuestion) {
      console.log("🚀 Sending final question:", finalQuestion);
      askQuestion(finalQuestion);
    }
  };

  recognitionRef.current = recognition;
  recognition.start();
  };


  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">☸</div>

          <div>
            <h1>Raphael</h1>
            <span>Voice-Enabled Assistant</span>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Backend online
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <div className="hero-badge">Your Everyday AI ASSISTANT</div>

          <h2>
            Ask Raphael.
            <br />
            <span>Get clear answers.</span>
          </h2>

          <p>
            Ask questions naturally and get clear, grounded answers powered by your knowledge base, with relevant sources when available.
          </p>
        </section>

        <section className="chat-card">
          {!answer && !loading && (
            <div className="empty-state">
              <div className="empty-icon">☸</div>

              <h3>What would you like to know?</h3>

              <p>
                Ask about Pods, Deployments, ReplicaSets, Services,
                networking, configuration, and more.
              </p>

              <div className="suggestions">
                <button
                  onClick={() =>
                    setQuery(
                      "How does a ReplicaSet maintain the desired number of Pods?"
                    )
                  }
                >
                  How does a ReplicaSet work?
                </button>

                <button
                  onClick={() =>
                    setQuery("What is the difference between a Pod and a Deployment?")
                  }
                >
                  Pod vs Deployment
                </button>

                <button
                  onClick={() =>
                    setQuery("How does Kubernetes service discovery work?")
                  }
                >
                  How does service discovery work?
                </button>
              </div>
            </div>
          )}

          {loading && (
            <div className="loading-state">
              <div className="loader"></div>

              <div>
                <h3>Searching Kubernetes documentation...</h3>
                <p>Retrieving relevant context and generating an answer.</p>
              </div>
            </div>
          )}

          {answer && !loading && (
            <div className="answer-section">
              <div className="answer-header">
                <div>
                  <span className="answer-label">ASSISTANT</span>
                  <h3>Answer</h3>
                </div>

              </div>

              <div className="answer-content">
                {answer}
              </div>

              {sources.length > 0 && (
                <div className="sources">
                  <h4>Sources</h4>

                  {sources.map((source, index) => (
                    <a
                      key={`${source.chunk_id}-${index}`}
                      href={source.url}
                      target="_blank"
                      rel="noreferrer"
                      className="source-card"
                    >
                      <div className="source-number">{index + 1}</div>

                      <div className="source-info">
                        <strong>{source.title}</strong>
                        <span>{source.chunk_id}</span>
                      </div>

                      <span className="source-arrow">↗</span>
                    </a>
                  ))}
                </div>
              )}
            </div>
          )}

          <div className="input-wrapper">
            <div className="input-box">
              <input
                type="text"
                placeholder="Ask anything about Kubernetes..."
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    askQuestion();
                  }
                }}
              />

              <button
                className={`mic-button ${isListening ? "listening" : ""}`}
                type="button"
                title={
                !voiceSupported
                ? "Speech recognition is not supported"
                : isListening
                ? "Stop listening"
                : "Voice input"
                }
                onClick={startListening}
                disabled={!voiceSupported}
                >
                {isListening ? "⏹" : "🎙"}
              </button>

              <button
              className="ask-button"
              onClick={() => askQuestion()}
              disabled={loading || !query.trim()}
              >
                {loading ? "Thinking..." : "Ask"}
                {!loading && <span>→</span>}
              </button>
            </div>

            <div className="input-hint">
            Press <kbd>Enter</kbd> to ask
            <span>•</span>
            {isListening ? "Listening..." : "Click 🎙 to speak"}
            </div>
          </div>
        </section>
      </main>

      <footer>
        Built with React + FastAPI + Sentence Transformers + Gemini
      </footer>
    </div>
  );
}

export default App;