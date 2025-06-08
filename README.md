# WeChatGPT

A multi-modal WeChat assistant powered by SiliconFlow APIs. This project uses
Poetry for dependency management and pyenv for Python version control.

## Setup

1. Install Python 3.10 with `pyenv` and set the local version:
   ```bash
   pyenv install 3.10.13
   pyenv local 3.10.13
   ```
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Copy `config_template.yaml` to `config.yaml` and fill in your API token and
   desired parameters.

## Running

Use the `scripts/run_assistant.py` script to send a message to the SiliconFlow
API and print the reply. The reply can also be sent to WeChat with `--wechat`
and saved as a speech audio file with `--tts`:

```bash
poetry run python scripts/run_assistant.py "Hello" --wechat --tts reply.mp3
```

## Testing

Run the unit tests with:

```bash
pytest -q
```
