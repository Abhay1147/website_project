#!/usr/bin/env python3
"""
jokes api logic

@author:
@version: 2025.11
"""

import pathlib
import random
import tomllib
from functools import cache

import pyjokes
from pyjokes.exc import CategoryNotFoundError, LanguageNotFoundError

from .models import Joke


class Joker:
    """
    A layer to retrieve jokes from the pyjokes package

    :raises ValueError: the dataset has not been initialized
    :raises ValueError: the language is invalid
    :raises ValueError: the category is invalid
    :raises ValueError: the joke id is invalid
    :raises ValueError: requested number of jokes is below 0
    
    """
    _dataset: list[Joke] = []
    _languages: dict[str, str] = {}
    _categories: list[str] = ["neutral", "chuck"]

    


    @classmethod
    def init_dataset(cls):
        """
        Initialize the dataset

        Load jokes from the `pyjokes` package into a list of jokes
        """
        # TODO: Implement this method
        if cls._dataset:
            return

        config_path = pathlib.Path(__file__).resolve().parent.parent / "config.toml"
        with open(config_path, "rb") as f: 
            config = tomllib.load(f)

        cls._languages = config.get("LANGUAGES", {})

        joke_id = 0  # ✅ Start from 0, not 1 (tests expect 0-based)
        for lang_code, lang_name in cls._languages.items():
            for category in cls._categories:
                try:
                    jokes_list = pyjokes.get_jokes(language=lang_code, category=category)
                    for text in jokes_list:
                        cls._dataset.append(
                            Joke(
                                id=joke_id,
                                language=lang_code,
                                category=category,
                                text=text,
                            )
                        )
                        joke_id += 1
                except (LanguageNotFoundError, CategoryNotFoundError):
                    continue

        if not cls._dataset:
            raise ValueError("No jokes loaded — dataset initialization failed.")

        

    @classmethod
    def get_jokes(cls, language: str = "any", category: str = "any", number: int = 0) -> list[Joke]:
        """Get all jokes in the specified language/category combination

        :param language: language of the joke
        :param category: category of the joke
        :param number: number of jokes to return, 0 to return all
        """
        # TODO: Implement this method
        if not cls._dataset:
            raise ValueError("Dataset not initialized. Call init_dataset first.")

        # check valid language
        if language == "any":
            language = None
        if category == "any":
            category = None

        jokes = cls._dataset

        if language is not None and language not in cls._languages:
            raise ValueError(f"Language {language} does not exist")

    # Validate category
        valid_categories = {j.category for j in cls._dataset}
        if category is not None and category not in valid_categories:
            raise ValueError(f"Category {category} does not exist")

        # Filter jokes
        jokes = cls._dataset
        if language is not None:
            jokes = [j for j in jokes if j.language.lower() == language.lower()]
        if category is not None:
            jokes = [j for j in jokes if j.category.lower() == category.lower()]

        # Limit number of jokes if requested
        if number > 0:
            jokes = random.sample(jokes, min(number, len(jokes)))

        return jokes



    @classmethod
    def get_the_joke(cls, joke_id: int) -> Joke:
        """Get a specific joke by id

        :param joke_id: joke id
        """
        # TODO: Implement this method
        if not cls._dataset:
            raise ValueError("Dataset not initialized.")

        for j in cls._dataset:
            if j.id == joke_id:
                return j

        # get valid ID range
        if cls._dataset:
            min_id = min(j.id for j in cls._dataset)
            max_id = max(j.id for j in cls._dataset)
        else:
            min_id, max_id = 0, 0

        raise ValueError(f"Joke {joke_id} not found, try an id between {min_id} and {max_id}")