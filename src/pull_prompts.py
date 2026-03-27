"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from utils import (
    save_yaml,
    load_yaml,
    check_env_vars,
    print_section_header,
    prompt_template_to_dict,
)

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Faz pull do prompt base do desafio e o salva localmente em YAML.
    """
    prompt_repo = os.getenv("SOURCE_PROMPT_NAME", "leonanluppi/bug_to_user_story_v1")
    output_path = Path("prompts/bug_to_user_story_v1.yml")
    raw_output_path = Path("prompts/raw_prompts.yml")

    print(f"Prompt de origem: {prompt_repo}")
    print(f"Arquivo de saída: {output_path}")

    try:
        client = Client()
        prompt_template = client.pull_prompt(prompt_repo)
        prompt_name = prompt_repo.split("/")[-1]
        prompt_payload = prompt_template_to_dict(prompt_name, prompt_template)

        if not prompt_payload[prompt_name]["system_prompt"].strip():
            raise ValueError("O prompt recebido do Hub não possui system prompt serializável.")

        saved_main = save_yaml(prompt_payload, str(output_path))
        saved_raw = save_yaml(prompt_payload, str(raw_output_path))

        if saved_main and saved_raw:
            print(f"✓ Prompt salvo em {output_path}")
            print(f"✓ Cópia raw salva em {raw_output_path}")
            return 0

        print(f"❌ Falha ao salvar o prompt em {output_path} e/ou {raw_output_path}")
        return 1

    except Exception as exc:
        print(f"⚠️  Não foi possível fazer pull do LangSmith Hub: {exc}")

        if output_path.exists():
            existing = load_yaml(str(output_path))
            if existing:
                print("✓ Mantendo o arquivo local existente como fallback.")
                return 0

        print("❌ Pull não concluído e nenhum fallback local utilizável foi encontrado.")
        return 1


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    Path("prompts").mkdir(parents=True, exist_ok=True)
    return pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
