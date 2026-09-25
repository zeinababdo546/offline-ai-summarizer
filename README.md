## Offline AI Tool

A lightweight CLI tool that summarizes notes **100% offline** using a local model via **Ollama**, with an optional flag to route requests to a hosted cloud API.

---

## 🚀 Quickstart 

Make sure [Ollama](https://ollama.com/) is installed and running, then pull the local model:

```bash
ollama pull qwen2.5:3b

```

Install the dependencies:

```bash
pip install -r requirements.txt

```

---


* **Default Mode (Offline - Local Ollama):**
```bash
python cli.py note.txt

```


* **Optional Remote Flag (Cloud API via OpenRouter / OpenAI):**
```bash
$env:OPENAI_API_KEY="your_api_key_here"
python cli.py note.txt --remote

```



---


### Model Choice Justification (`qwen2.5:3b`)

* **Low Footprint:** Runs efficiently on local hardware (~1.9 GB VRAM/RAM).
* **High Quality Output:** Outperforms standard sub-4B models in multi-lingual structured summarization and instruction following.

---

### Benchmarking

| Metric | Local (`qwen2.5:3b`) | Remote (`openai/gpt-4o-mini`) |
| --- | --- | --- |
| **Execution Mode** | Fully Offline (Ollama) | Cloud API (OpenRouter/OpenAI) |
| **Generation Speed** | **~4.68 tokens/sec** | **~13.15 tokens/sec** |
| **Total Latency** | **16.78 seconds** | **9.71 seconds** |
| **Summary Quality** | Clear & Concise (4 Key Bullet Points) | Structured Sections with Headers |

