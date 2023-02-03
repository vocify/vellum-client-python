from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional

import dacite


class Provider(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    UNKNOWN = "UNKNOWN"


class FinishReason(Enum):
    LENGTH = "LENGTH"
    STOP = "STOP"
    UNKNOWN = "UNKNOWN"


@dataclass
class TokenLogProbs:
    token: str
    logprob: Optional[float]
    top_logprobs: Optional[Dict[str, float]] = field(repr=False)
    text_offset: int = field(repr=False)


@dataclass
class LogProbs:
    tokens: List[TokenLogProbs] = field(repr=False)
    likelihood: float


@dataclass
class Completion:
    id: str = field(repr=False)
    text: str
    finish_reason: FinishReason = field(repr=False)
    logprobs: LogProbs = field(repr=False)


@dataclass
class GenerateResult:
    # The LLM provider that was used to generate the predictions.
    provider: Provider
    # The completions generated by the LLM provider, normalized to Vellum's schema.
    completions: List[List[Completion]]

    @classmethod
    def from_raw(cls, raw_result: dict) -> GenerateResult:
        return dacite.from_dict(data_class=cls, data=raw_result, config=dacite.Config(cast=[Provider, FinishReason]))