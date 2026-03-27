"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from utils import (
    load_yaml,
    check_env_vars,
    print_section_header,
    validate_prompt_structure,
    build_chat_prompt_template,
)

load_dotenv()


def get_repo_name(prompt_name: str) -> str:
    """
    Monta o identificador completo do prompt no Hub.
    """
    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()
    if not username:
        raise ValueError(
            "USERNAME_LANGSMITH_HUB não configurado no .env. "
            "Sem isso, o push pode ir para um destino difícil de localizar no Hub."
        )
    return f"{username}/{prompt_name}"


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    repo_name = get_repo_name(prompt_name)
    prompt_template = build_chat_prompt_template(prompt_data)

    description = prompt_data.get("description", "")
    tags = prompt_data.get("tags", [])
    techniques = prompt_data.get("techniques_applied", [])
    readme = (
        f"{description}\n\n"
        f"Técnicas aplicadas: {', '.join(techniques) if techniques else 'não informadas'}.\n"
        f"Tags: {', '.join(tags) if tags else 'sem tags'}."
    )
    print(f"Destino do prompt no Hub: {repo_name}")

    try:
        client = Client()
        result = client.push_prompt(
            repo_name,
            object=prompt_template,
            is_public=True,
            description=description,
            readme=readme,
            tags=tags,
        )
        print(f"✓ Prompt publicado: {repo_name}")
        if result:
            print(f"  Commit: {result}")
        print(f"  Procure no Hub por: {repo_name}")
        return True
    except Exception as exc:
        error_text = str(exc)
        if "Nothing to commit" in error_text or "409 Client Error: Conflict" in error_text:
            print(f"✓ Prompt já estava publicado e sem alterações: {repo_name}")
            print("  O Hub rejeitou um novo commit porque não houve mudança de conteúdo.")
            return True
        print(f"❌ Erro ao publicar prompt: {exc}")

    return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []
    is_valid, structure_errors = validate_prompt_structure(prompt_data)
    errors.extend(structure_errors)

    user_prompt = prompt_data.get("user_prompt", "").strip()
    if not user_prompt:
        errors.append("user_prompt está vazio")

    if "{bug_report}" not in prompt_data.get("system_prompt", "") and "{bug_report}" not in user_prompt:
        errors.append("O placeholder {bug_report} não foi encontrado no prompt")

    return (is_valid and len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]

    if not check_env_vars(required_vars):
        return 1

    yaml_data = load_yaml("prompts/bug_to_user_story_v2.yml")
    if not yaml_data:
        return 1

    prompt_name = "bug_to_user_story_v2"
    prompt_data = yaml_data.get(prompt_name)
    if not prompt_data:
        print(f"❌ Chave '{prompt_name}' não encontrada em prompts/bug_to_user_story_v2.yml")
        return 1

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Prompt inválido:")
        for error in errors:
            print(f"   - {error}")
        return 1

    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    if not success:
        return 1

    print("\nPróximos passos:")
    print(f"1. Abra o LangSmith Hub e procure por `{get_repo_name(prompt_name)}`")
    print("2. Confirme se o prompt ficou público")
    print("3. Rode `python3 src/evaluate.py` para avaliar a versão publicada")
    return 0


if __name__ == "__main__":
    sys.exit(main())
