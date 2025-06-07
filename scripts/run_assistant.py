import argparse
from pathlib import Path
from wechat_gpt.config import load_config
from wechat_gpt.llm.siliconflow_client import SiliconFlowClient
from wechat_gpt.util.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Run WeChatGPT assistant")
    parser.add_argument("message", help="Message to send to the LLM")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    parser.add_argument(
        "--wechat",
        action="store_true",
        help="Also send the reply to the active WeChat conversation",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        logger.error("Config file %s not found", config_path)
        return

    config = load_config(config_path)
    client = SiliconFlowClient(config)

    messages = [{"role": "user", "content": args.message}]
    reply = client.chat(messages)
    print("Assistant:", reply)
    if args.wechat:
        try:
            from wechat_gpt.wechat.client import send_message

            send_message(reply)
        except Exception as e:  # noqa: BLE001
            logger.error("Failed to send via WeChat: %s", e)


if __name__ == "__main__":
    main()
