# 🎭 Digital Twin

An AI chat app that answers questions as **Mercyline Sandra**, a Computer Science student in Nairobi, Kenya. Visitors can ask about her skills, projects and goals in **English or Kiswahili**. Built with Python and Streamlit.

## Features

- Chat interface with live (streaming) replies
- English and Kiswahili support
- Dark / light mode
- Adjustable creativity and reply length
- Usage statistics (messages, average response time, estimated tokens)
- Export the conversation as a JSON file
- Clear chat with a confirmation step
- Loading indicator and friendly error messages
- Mobile-friendly layout

## Tech stack

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- An LLM provider: Groq, Google Gemini, OpenAI or Anthropic (you only need one)

## Project structure

```
Digitaltwin/
├── app.py            # the whole app
├── requirements.txt  # Python packages
├── .env              # your secret API key (NOT uploaded to GitHub)
├── .gitignore        # tells Git to ignore .env and .venv
└── README.md
```

## Getting started

### 1. Clone the project

```bash
git clone https://github.com/sandracod0/digital-twin.git
cd digital-twin
```

### 2. Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Mac / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the packages

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a file named `.env` in the project folder (next to `app.py`) and add **one** of these lines:

```
GROQ_API_KEY=your_key_here
# GEMINI_API_KEY=your_key_here
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
```

Free keys: [console.groq.com](https://console.groq.com) or [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

Optional: choose a different model with `GROQ_MODEL=...`, `GEMINI_MODEL=...`, `OPENAI_MODEL=...` or `ANTHROPIC_MODEL=...`.

### 5. Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

To test on your phone, connect it to the same Wi-Fi and open the **Network URL** that Streamlit prints in the terminal.

## Customize it

Edit the `PROFILE` section at the top of `app.py` with your own name, bio, skills, projects and goals. The twin only knows what is written there, and it is told not to invent anything else, so keep the profile truthful.

## Deploy (Streamlit Community Cloud)

1. Push this project to GitHub (never include `.env`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app from your repository, with `app.py` as the main file.
3. In **Advanced settings → Secrets**, add your key:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
4. Click **Deploy**.

## Security

- Never commit your `.env` file or share your API key.
- If a key is ever exposed, delete it in the provider's console and create a new one.

## Author

**Mercyline Sandra**, Computer Science student, Nairobi, Kenya.

## License

MIT. Free to use and adapt.