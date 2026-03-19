# Contributing to TriggerMind

Thanks for your interest in improving TriggerMind.

## Development setup

```bash
git clone https://github.com/example/triggermind.git
cd triggermind
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
```

## Running checks

```bash
pytest
```

## Contribution guidelines

- Keep changes local-first and privacy-preserving.
- Prefer clear abstractions over framework-heavy design.
- Add tests for any behavior change.
- Keep CLI output concise and friendly.
- Update documentation for user-facing changes.

## Pull requests

- Use descriptive commit messages.
- Explain user impact and architectural impact.
- Include command output for tests you ran.
