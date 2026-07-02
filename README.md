# IRIS — Intelligent Real-time Interactive System

A voice-first AI assistant that acts as your hands — listening, thinking, and executing tasks on your PC.

[![CI](https://github.com/Aradhya648/Iris/actions/workflows/ci.yml/badge.svg)](https://github.com/Aradhya648/Iris/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey.svg)]()

---

## What is IRIS?

IRIS is an open-source voice assistant that bridges the gap between natural language and system actions. Say "Iris" to wake it, speak a command, and watch it execute — files, apps, browser, email, todos, weather, timers, and more.

```
You:   "Iris, what's the weather in Tokyo?"
IRIS:  [wakes up] → [transcribes] → [plans via DeepSeek] → [fetches weather] → [speaks answer]
```

### Key capabilities

- **24 action handlers** — files, OS, shell, clipboard, screenshots, OCR, email, todos, weather, timers, browser automation
- **DeepSeek V4 Pro** reasoning with task decomposition (Planner → Executor agent pipeline)
- **Groq Whisper** cloud ASR (whisper-large-v3-turbo) for fast, accurate speech-to-text
- **ElevenLabs** streaming TTS with mid-speech interrupt ("stop")
- **ChromaDB + BGE-M3** vector memory with knowledge graph (NetworkX)
- **Self-improving loop** — logs interactions, proposes prompt refinements, tracks outcomes
- **Tauri v2 overlay** — transparent fullscreen border with animated state feedback
- **Safety classification** — SAFE / WARN / DANGEROUS with approval popups for destructive actions
- **Two deployment modes** — `local` (your own API keys) or `remote` (shared backend proxy)

---

## Quick Start

### Prerequisites

- Python 3.11+
- [Rust + Cargo](https://rustup.rs) (for Tauri UI)
- FFmpeg

### Install

```bash
git clone https://github.com/Aradhya648/Iris.git
cd Iris
pip install -r requirements.txt
python -m playwright install chromium
cargo install tauri-cli
```

### Configure API keys

Copy the template and fill in your keys:

```bash
cp configs/keys.env.example configs/keys.env
```

**Local mode** (default) — you need:
| Key | Service | Get it at |
|-----|---------|-----------|
| `DEEPSEEK_API_KEY` | LLM reasoning | [deepseek.com](https://platform.deepseek.com) |
| `ELEVENLABS_API_KEY` | Voice synthesis | [elevenlabs.io](https://elevenlabs.io) |
| `GROQ_API_KEY` | Speech-to-text | [console.groq.com](https://console.groq.com) |

**Remote mode** — no individual keys needed. Set `mode: "remote"` in `configs/settings.yaml` and point to a shared backend.

### Run

**Terminal 1** — backend:
```bash
python main.py
```

**Terminal 2** — UI overlay (optional):
```bash
cd ui/tauri-app
cargo tauri dev
```

Say **"Iris"** or **"Jarvis"** to wake. Speak your command. Say **"Stop"** to interrupt.

---

## Architecture

```
Voice In → [Mic Listener] → [Groq Whisper ASR] → [Wake Word / Command]
                                                        ↓
                                               [State Manager]
                                           IDLE → INTERACTIVE → ACTING
                                                        ↓
                                            [Memory Injection (ChromaDB)]
                                                        ↓
                                             [DeepSeek V4 Pro LLM]
                                                        ↓
                                           [Planner → Executor Agents]
                                                        ↓
                                      [Action Router → Safety Gate → Handler]
                                                        ↓
                                    [ElevenLabs TTS] ← [Tauri UI Update]
                                                        ↓
                                                    Voice Out
```

### Module map

```
iris/
├── audio/          # Mic listener, ASR (Groq Whisper), wake word, interrupt
├── core/           # Event loop, state manager, task orchestrator
├── llm/            # LLM router + HTTP provider (DeepSeek, AgentRouter, proxy)
├── agents/         # Planner, executor, coding agent, agent manager
├── actions/        # 24 action handlers + safety classifier + approval gate
├── memory/         # Short-term buffer, ChromaDB vectors, knowledge graph, self-improvement
├── voice/          # ElevenLabs TTS, stream player, TTS router
├── browser/        # Playwright automation, login handler, scraper
├── ui/             # WebSocket IPC bridge + Tauri v2 overlay
├── backend/        # Shared proxy server (FastAPI) for remote mode
├── utils/          # Config loader, logger, platform detection
└── main.py         # Entrypoint
```

---

## Action Handlers

### 24 registered actions across 9 modules

| Module | Actions | Safety |
|--------|---------|--------|
| **File** | `read_file`, `write_file`, `move_file`, `delete_file` | SAFE / WARN / DANGEROUS |
| **OS** | `open_app`, `focus_window` | SAFE |
| **Shell** | `run_shell`, `run_shell_sudo` | WARN / DANGEROUS |
| **Screen** | `screenshot`, `ocr` | SAFE |
| **Clipboard** | `get_clipboard`, `set_clipboard` | SAFE / WARN |
| **Email** | `send_email`, `check_email` | WARN / SAFE |
| **Todo** | `add_task`, `list_tasks`, `mark_task_complete`, `delete_task` | WARN / SAFE |
| **Weather** | `get_weather`, `get_forecast` | SAFE |
| **Timer** | `set_timer`, `set_reminder`, `list_reminders`, `cancel_reminder` | WARN / SAFE |

Safety levels: **SAFE** = auto-execute, **WARN** = execute + log, **DANGEROUS** = approval popup required.

---

## UI Overlay

| State | Border | Animation |
|-------|--------|-----------|
| IDLE | White | Static — waiting for wake word |
| INTERACTIVE | Blue `#3B82F6` | Slow pulse — listening |
| ACTING | Green `#22C55E` | Sweeping — executing |
| STOPPING | Fading | Shutting down |

---

## Deployment Modes

### Local mode (default)
Each service uses your own API keys. Full control over endpoints and models.

### Remote mode
All traffic routes through a shared FastAPI proxy. The proxy holds the API keys — clients just need the proxy URL. Deploy on Railway, Render, or any container platform.

```yaml
# configs/settings.yaml
mode: "remote"
remote:
  backend_url: "https://your-proxy.railway.app"
```

See [`backend/`](backend/) for the proxy server.

---

## Configuration

All settings in `configs/settings.yaml`. Key sections:

```yaml
mode: "local"                    # "local" or "remote"

llm:
  base_url: "https://api.deepseek.com"
  default_model: "deepseek-v4-pro"

voice:
  voice_name: "Bella"
  model: "eleven_flash_v2_5"

asr:
  model: "whisper-large-v3-turbo"

audio:
  wake_words: ["jarvis", "iris"]

memory:
  chroma_path: "~/.iris/memory/chroma"
  embedding_model: "BAAI/bge-m3"
```

---

## Development

### Adding a new action

```python
# 1. Create handler — actions/my_action.py
async def my_action(**params) -> dict:
    return {"status": "ok", "result": "done"}

# 2. Register — actions/action_router.py
ACTION_HANDLERS["my_action"] = my_action.my_action

# 3. Classify — actions/safety.py
ACTION_SAFETY_MAP["my_action"] = SafetyLevel.SAFE
```

### Running tests

```bash
python -m pytest tests/ -v
```

### CLI options

```bash
python main.py                          # normal boot
python main.py --headless               # no UI overlay
python main.py --config custom.yaml     # custom config
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Runtime | Python 3.11+ |
| LLM | DeepSeek V4 Pro (via OpenAI-compatible HTTP) |
| ASR | Groq Whisper API (whisper-large-v3-turbo) |
| TTS | ElevenLabs (eleven_flash_v2_5, streaming) |
| Memory | ChromaDB + BGE-M3 embeddings + NetworkX graph |
| Browser | Playwright |
| UI | Tauri v2 (Rust) + WebSocket IPC |
| Backend Proxy | FastAPI |
| CI | GitHub Actions |

---

## Project Guide

Full documentation including milestones, work division, and architecture details:

- [Project Guide (Markdown)](docs/PROJECT_GUIDE.md)
- [Project Guide (PDF)](IRIS_Project_Guide_v0.2.1.pdf)
- [Windows Testing Guide](docs/WINDOWS_TESTING.md)

---

## Team

| Name | Focus | Platform |
|------|-------|----------|
| **Aradhya** | Architecture, core loop, voice, UI, actions, agents | macOS |
| **Aryan** | Audio, LLM, memory, browser, coding agent | Windows |
| **Maneesh** | Actions, integrations, documentation, testing | Windows |

---

## License

[MIT](LICENSE)
