"""
Utilitários para carregar o dataset do desafio.
"""

import json
from typing import List, Dict, Any


def load_dataset_from_jsonl(jsonl_path: str) -> List[Dict[str, Any]]:
    """
    Carrega exemplos de avaliação a partir de um arquivo JSONL.
    """
    examples: List[Dict[str, Any]] = []

    with open(jsonl_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            examples.append(json.loads(line))

    return examples
