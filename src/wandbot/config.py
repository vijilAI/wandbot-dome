import pathlib
from datetime import datetime
from typing import List, Tuple

from pydantic import BaseModel, BaseSettings, Field, root_validator
from wandbot.ingestion.config import VectorIndexConfig


class ChatConfig(BaseSettings):
    model_name: str = "gpt-4"
    max_retries: int = 1
    fallback_model_name: str = "gpt-3.5-turbo"
    max_fallback_retries: int = 6
    chat_temperature: float = 0.0
    chain_type: str = "stuff"
    chat_prompt: pathlib.Path = pathlib.Path("data/prompts/chat_prompt.txt")
    vectorindex_config: VectorIndexConfig = VectorIndexConfig(
        wandb_project="wandb_docs_bot_dev",  # TODO: change this to the correct project using ENV
        hyde_prompt=None,
    )
    vectorindex_artifact: str = (
        "parambharat/wandb_docs_bot_dev/wandbot_vectorindex:latest"
    )
    verbose: bool = False
    wandb_project: str | None = Field(None, env="WANDBOT_WANDB_PROJECT")
    wandb_entity: str | None = Field(None, env="WANDBOT_WANDB_ENTITY")
    wandb_job_type: str | None = "chat"
    include_sources: bool = True
    source_score_threshold: float = 1.0
    query_tokens_threshold: int = 1024

    class Config:
        env_prefix = "WANDBOT_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    @root_validator(pre=False)
    def _set_defaults(cls, values):
        if values["wandb_project"] is None:
            values["wandb_project"] = values["vectorindex_config"].wandb_project
        if values["wandb_entity"] is None:
            values["wandb_entity"] = values["vectorindex_config"].wandb_entity
        return values


class ChatRequest(BaseModel):
    question: str
    chat_history: List[Tuple[str, str]] | None = None


class ChatRepsonse(BaseModel):
    question: str
    answer: str
    model: str
    sources: str
    source_documents: str
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    successful_requests: int
    total_cost: float
    time_taken: float
    start_time: datetime
    end_time: datetime
