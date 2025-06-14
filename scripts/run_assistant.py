import argparse
from pathlib import Path
from wechat_gpt.config import load_config
from wechat_gpt.llm.siliconflow_client import SiliconFlowClient
from wechat_gpt.util.logger import get_logger

logger = get_logger(__name__)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run WeChatGPT assistant")
    parser.add_argument(
        "message",
        nargs="?",
        help="Message to send to the LLM. Ignored if --stt is provided",
    )
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument(
        "--wechat",
        action="store_true",
        help="Also send the reply to the active WeChat conversation",
    )
    parser.add_argument(
        "--tts",
        metavar="FILE",
        help="Save the assistant's reply as a speech audio file",
    )
    parser.add_argument(
        "--stt",
        metavar="FILE",
        help="Use speech-to-text on the given audio file as the prompt",
    )

    args = parser.parse_args(argv)

    config_path = Path(args.config)
    if not config_path.exists():
        logger.error("Config file %s not found", config_path)
        return

    config = load_config(config_path)
    client = SiliconFlowClient(config)

    if args.stt:
        try:
            from wechat_gpt.voice.speech_to_text import speech_to_text

            audio_bytes = Path(args.stt).read_bytes()
            args.message = speech_to_text(client, audio_bytes)
            logger.info("Transcribed text: %s", args.message)
        except Exception as e:  # noqa: BLE001
            logger.error("Failed to transcribe audio: %s", e)
            return

    if not args.message:
        logger.error("No message provided")
        return

    messages = [{"role": "user", "content": args.message}]
    reply = client.chat(messages)
    print("Assistant:", reply)

    if args.wechat:
        try:
            from wechat_gpt.wechat.client import send_message

            send_message(reply)
        except Exception as e:  # noqa: BLE001
            logger.error("Failed to send via WeChat: %s", e)

    if args.tts:
        try:
            from wechat_gpt.voice.text_to_speech import text_to_speech

            audio = text_to_speech(client, reply)
            Path(args.tts).write_bytes(audio)
            logger.info("Saved audio to %s", args.tts)
        except Exception as e:  # noqa: BLE001
            logger.error("Failed to generate speech: %s", e)



if __name__ == "__main__":
    main()
