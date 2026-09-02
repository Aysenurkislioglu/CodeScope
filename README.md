# CodeScope

AI Codebase Assistant. CodeScope starts by safely scanning a local repository, cataloguing supported code and documentation files, and presenting the result in a focused workspace. RAG, embeddings, and LLM answers are intentional later phases.

## Features

- React + TypeScript workspace for starting a local repository scan
- FastAPI API with validation and browser-friendly error messages
- Scanner for Python, JavaScript/TypeScript, Java, C/C++, Go, Markdown, text, and PDF files
- Secret-like environment files, dependency folders, binaries, and large files are excluded

## Architecture

```text
React + Vite UI
       |
       | POST /api/repositories
       v
FastAPI scanner --> filtered file metadata --> repository summary
```

## Tech Stack

- Frontend: React, Vite, TypeScript, CSS
- Backend: Python, FastAPI
- Testing: pytest and FastAPI TestClient

## Installation

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`; the frontend runs at `http://localhost:5173`.

## Environment Variables

Copy `.env.example` to `.env` when configuration is needed. Never commit `.env`.

`REPOLENS_ALLOWED_ROOT` is optional. When set, local scans must be inside this directory.

## How It Works

1. Enter the absolute path of a local repository.
2. The backend walks it without following symlinks.
3. Ignored directories, `.env*` files, binary files, and files above 1 MB are skipped.
4. CodeScope returns supported file metadata and scan totals.

## Repository Indexing

This milestone is the scanner foundation only; it does not save embeddings or source contents yet. Supported code: `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.java`, `.cpp`, `.c`, `.go`. Documentation: `.md`, `.txt`, `.pdf`.

## RAG Pipeline

Planned: semantic chunks → embeddings/vector database → semantic, symbol, and graph retrieval → cited LLM response.

## Code Intelligence

Planned: AST extraction for functions, classes, imports, calls, callers, callees, and file dependencies, beginning with Python and TypeScript/JavaScript.

## Screenshots

Run the two local services to see the scanner workspace.

## Future Improvements

- GitHub repository cloning
- Persistent repository records and indexing progress
- Tree-sitter AST chunks and relationship graph
- ChromaDB retrieval and LLM-based cited answers
- Source viewer with highlighted lines

## License

No license has been selected yet.
