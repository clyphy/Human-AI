---
id: 20260714-github-sync
title: GitHub Sync & CI
tags: [workflow, github, setup]
created: 2026-07-14
updated: 2026-07-14
related: [20260714-dev-workflow, 20260714-us-framework]
summary: Version control and automated testing across your AI projects.
---

# GitHub Sync & CI

> Summary: Version control and automated testing across your AI projects.

## Context

Keep your local AI projects in sync with GitHub, run automated tests on every push, and maintain clean commit history.

## GitHub Setup

### Create repositories

If you don't have repos yet:
```bash
# Create repo on github.com/clyphy
# Then locally:

cd ~/ai-projects/us
git init
git remote add origin https://github.com/clyphy/us.git
git branch -M main
git add .
git commit -m "initial commit"
git push -u origin main
```

### SSH keys (recommended over HTTPS)
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "clyphy@gmail.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
# Paste contents of ~/.ssh/id_ed25519.pub

# Test connection
ssh -T git@github.com
```

## Daily Git Workflow

```bash
# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/description

# Make changes, test locally
pytest tests/

# Commit small, logical chunks
git add src/agents/eve.py
git commit -m "feat: add memory context to Eve responses"

git add tests/test_eve.py
git commit -m "test: add test for Eve memory"

# Push to GitHub
git push origin feature/description

# Create Pull Request on GitHub
# → Review, request feedback, iterate
# → Merge to main when ready
```

## GitHub Actions CI/CD

### Basic test workflow (`.github/workflows/test.yml`)

```yaml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest tests/ -v --cov=src

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Lint & format check (`.github/workflows/lint.yml`)

```yaml
name: Lint & Format

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install tools
        run: pip install black flake8 mypy

      - name: Format check
        run: black --check src/

      - name: Lint
        run: flake8 src/ --max-line-length=100

      - name: Type check
        run: mypy src/
```

### Docker build & push (`.github/workflows/docker.yml`)

```yaml
name: Docker Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: |
          docker build -f api/Dockerfile -t us-api:latest .

      - name: Test image
        run: |
          docker run --rm us-api:latest python -m pytest
```

## Branch Strategy

```
main (protected, requires PR)
  ├── feature/improve-eve-responses (PR open)
  ├── feature/dahlia-memory-optimization (merged)
  └── feature/mcp-server-integration (in review)
```

### Branch naming
- `feature/description` — New functionality
- `fix/description` — Bug fixes
- `docs/description` — Documentation
- `refactor/description` — Code improvements
- `test/description` — Test additions

## Commit Message Convention

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(eve): add contextual memory to responses
fix(us): resolve decision-tree race condition
docs(setup): update installation instructions
test(dahlia): add memory persistence tests
refactor(agents): extract common inference logic
```

## Pull Request Checklist

Before creating a PR:
- [ ] Tests pass locally (`pytest`)
- [ ] Code formatted (`black src/`)
- [ ] Linting passes (`flake8`)
- [ ] Types checked (`mypy`)
- [ ] Updated relevant docs
- [ ] Meaningful commit messages

PR description template:
```markdown
## Description
Brief explanation of what this PR does.

## Related Issue
Closes #123

## Changes
- Change 1
- Change 2

## Testing
How to verify the changes work.

## Checklist
- [x] Tests pass
- [x] Documentation updated
```

## Syncing Multiple Repos

You have 5 repos; keep them in sync:
```bash
#!/bin/bash
# sync-all.sh

for repo in us eve dahlia human-ai ai-self-aware; do
  echo "Updating $repo..."
  cd ~/ai-projects/$repo
  git pull origin main
  git status
done
```

## Remote Collaboration (if working with others)

```bash
# Add collaborator as a remote
git remote add collaborator https://github.com/their-username/us.git

# Fetch their changes
git fetch collaborator

# Merge their branch
git merge collaborator/their-feature

# Or rebase
git rebase collaborator/main
```

## Secrets Management

**Never commit API keys, passwords, or sensitive data!**

```bash
# Example: .env (add to .gitignore)
echo "POSTGRES_PASSWORD=secret" > .env

# Or use GitHub Secrets for CI/CD
# Settings → Secrets and variables → Repository secrets
# Add: POSTGRES_PASSWORD, HUGGINGFACE_TOKEN, etc.

# In workflows, reference them:
# env:
#   POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
```

## Deployment from GitHub

### Trigger deployment on push to main
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to server
        run: |
          ssh user@server "cd ~/projects/us && git pull && docker-compose up -d"
```

## Troubleshooting

### Git merge conflict
```bash
# 1. Find conflicts
git status

# 2. Edit files to resolve
# 3. Add resolved files
git add resolved-file.py

# 4. Commit merge
git commit -m "resolve merge conflict"
```

### Need to undo last commit
```bash
# Soft undo (keep changes)
git reset --soft HEAD~1

# Hard undo (discard changes)
git reset --hard HEAD~1
```

### Large files accidentally committed
```bash
# Use git-lfs for models
git lfs install
git lfs track "*.gguf"
git add .gitattributes models/
```

## Related
- [Dev Workflow](dev-workflow.md) — Local development setup.
- [Projects](../projects/_topic.md) — Your GitHub repos.
