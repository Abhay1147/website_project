#!/usr/bin/env python3
"""
jokes api models

@author:
@version: 2025.11
"""

from dataclasses import dataclass, asdict


@dataclass
class Joke:
    """
    A model to store individual jokes

    Each joke has language, category, and text
    """

    # TODO: Implement this class
    language: str
    category: str
    text: str
    id: int | None = None  # ✅ optional so test doesn’t break

    def to_dict(self) -> dict:
        return asdict(self)
