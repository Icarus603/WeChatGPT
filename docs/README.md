
# Additional Notes

## ClickClick

WeChat message sending relies on the [ClickClick](https://github.com/anyshortcut/ClickClick) command line tool. Install it via Homebrew:

```bash
brew install anyshortcut/tap/clickclick
```

Then grant Accessibility permissions for ClickClick in macOS System Settings.

## Configuration

Copy `config_template.yaml` to `config.yaml` and provide your SiliconFlow API token and model settings. The file is git‑ignored.

## Running

You can send a prompt to the assistant and optionally relay the response to the active WeChat chat window. The prompt may come from an audio file using `--stt`, and the reply can also be saved as an audio file using `--tts`:

```bash
poetry run python scripts/run_assistant.py "Hello" --wechat --tts reply.mp3
```
To transcribe audio as the prompt and save the reply as an audio file:
```bash
poetry run python scripts/run_assistant.py --stt question.wav --tts answer.mp3
```

