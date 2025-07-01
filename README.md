# 🔧 Terminal AI Agent with Tool Use and Model Selection

This repository implements a minimal yet extensible terminal-based AI agent interface using [Hugging Face](https://huggingface.co) InferenceClient and Ollama. The agent supports:

- Model selection at launch (from a `config.yml` list)
- Multi-turn conversations
- Tool usage (e.g., function calling)
- Terminal-based UI with keyboard input (arrow key navigation)
- Extensible tool registry for adding functionality

## 📦 Features

- ✅ Model selection via interactive terminal menu
- ✅ Function calling support (tool execution)
- ✅ Tool registry for structured tool descriptions
- ✅ Agent prompt with reasoning guidelines
- ✅ Easy-to-extend memory and planning (in development)
- 🖥️ Terminal-based user interface with ASCII branding

## 📁 Project Structure
```
.
├── nanoAgent.py      # Core LLMAgent class
├── tools.py          # Tool implementations and function registry
├── model_selector.py # Model selection logic with terminal UI
├── nanoUI.py         # Terminal entry point and main loop
├── config.yml        # Ollama base url and list of models for selection
└── README.md         # This file
└── requirements.txt
```

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/sdelahaies/nano-agent.git
cd nano-agent
```

2. Create a virtual env and install dependencies

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

# 🚀 Running the Agent
```bash
python nanoUI.py
```

# ⚙️ Configuration
The config.yml contains a list of ollama model identifiers :
```yaml
base_url: http://localhost:11434/
models:
  - qwen3:1.7b
  - llama3.2:3b
```
you need to pull them first.


# 🧰 Adding Tools

To add new tools add the function in `tools.py` with the `@register_function` decorator, make sure the function has a proper docstring, the tool definition is generated from the docstring.

# 📌 License

MIT License