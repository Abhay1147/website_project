#!/usr/bin/env python3
"""
jokes api

@author:
@version: 2025.11
"""

import pathlib
import tomllib

from flask import Flask
from flask_cors import CORS
from .logic import Joker
from .routes import main


def create_app() -> Flask:
    
    this_app = Flask(__name__)

    # TODO: Implement this function
    CORS(this_app)

    # Load configuration from config.toml
    config_path = pathlib.Path(__file__).resolve().parent.parent / "config.toml"
    with open(config_path, "rb") as f:
        config = tomllib.load(f)
    this_app.config.update(config)

    # Initialize dataset

    try:
        Joker.init_dataset()
        print(f"✅ Loaded {len(Joker._dataset)} jokes successfully.")
    except Exception as e:
        print(f"⚠️ Failed to initialize dataset: {e}")

    # Register routes (Blueprint)
    this_app.register_blueprint(main)

    return this_app

