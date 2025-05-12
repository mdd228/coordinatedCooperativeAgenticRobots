---
title: Multi-Agent Palindrome Detector
emoji: 🤖
colorFrom: indigo
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

# Multi-Agent Palindrome Detector

This app uses a custom HTML/JS frontend (index.html) and a Flask backend API for agentic palindrome detection. It is designed to run on Hugging Face Spaces using the Docker/Flask template.

## How it works
- `index.html` is served as the main page.
- All static assets (CSS, JS) should be placed in the `static/` directory.
- The backend API is available at `/api/process` for text processing.

## Running locally
```
pip install -r requirements.txt
python app.py
```
Then open http://localhost:7860 in your browser.

## Deploying on Hugging Face Spaces
- Set `app_file: app.py` in your Space settings.
- Make sure all static assets are in the `static/` directory.