# Phase 01: Project Setup

## Context
- Parent plan: [plan.md](plan.md)
- No dependencies

## Overview
- **Priority**: High
- **Status**: ⬜ Pending
- **Effort**: 0.5h
- Initialize project structure, dependencies, config

## Requirements
- Python 3.10+ virtual environment
- All dependencies pinned in requirements.txt
- Frontend served by FastAPI static files (no separate build step)

## Related Code Files
**Create:**
- `requirements.txt` — fastapi, uvicorn[standard], numpy, websockets
- `backend/__init__.py`
- `frontend/` directory
- `.gitignore` — update with __pycache__, .venv, *.npy

## Implementation Steps
1. Create `backend/` and `frontend/` directories
2. Create `requirements.txt` with: fastapi, uvicorn[standard], numpy
3. Create `backend/__init__.py` (empty)
4. Update `.gitignore` with Python-specific entries
5. Verify: `pip install -r requirements.txt` works

## Todo
- [ ] Create directory structure
- [ ] Create requirements.txt
- [ ] Update .gitignore
- [ ] Verify pip install

## Success Criteria
- `pip install -r requirements.txt` succeeds
- Directory structure matches architecture

## Risk Assessment
- Low risk phase

## Next Steps
→ Phase 02: Snake Game Engine
