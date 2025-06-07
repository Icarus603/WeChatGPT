from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class APIConfig:
    token: str
    base_url: str


@dataclass
class ModelConfig:
    chat: str
    stt: str
    tts: str
    image: str


@dataclass
class ParamsConfig:
    temperature: float
    top_p: float
    top_k: int
    max_tokens: int


@dataclass
class Config:
    api: APIConfig
    models: ModelConfig
    params: ParamsConfig


def load_config(path: str | Path) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    api = APIConfig(**data["api"])
    models = ModelConfig(**data["models"])
    params = ParamsConfig(**data["params"])
    return Config(api=api, models=models, params=params)
