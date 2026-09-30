# AI Learning LMS — Streamlit Edition

A GitHub/Streamlit Cloud-ready AI learning platform for students. It includes 8 AI-in-banking courses, lessons, demo quizzes, progress tracking, certificates, profile editing, dashboard KPIs, sponsors, and an AI Generative Tutor.

## Streamlit Cloud deployment

1. Create a GitHub repository.
2. Upload **all files and folders in this project** to the repository root.
3. In Streamlit Community Cloud choose the repository.
4. Set **Main file path** to:

```text
app.py
```

5. Deploy.

`requirements.txt` tells Streamlit Cloud to install Streamlit automatically.

## Main files

- `app.py` — complete Streamlit application
- `requirements.txt` — Python dependency
- `data/users.json` — local demo user store
- `.streamlit/config.toml` — theme settings

## Important architecture note

This is the Streamlit deployment edition. It replaces the previous React/Vite + Express runtime with a single Python Streamlit entry point so it can be deployed directly from GitHub to Streamlit Cloud. The learning content and UI behavior are preserved in the Streamlit implementation.

For production authentication, replace the demo JSON user store with a real database/auth provider and use secure secrets. The included password storage is intended for this demo deployment and should not be treated as production authentication infrastructure.
