"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    @staticmethod
    def get_prompt():
        prompts = load_prompts("prompts/bug_to_user_story_v2.yml")
        return prompts["bug_to_user_story_v2"]

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = self.get_prompt()
        assert "system_prompt" in prompt
        assert prompt["system_prompt"].strip()

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompt = self.get_prompt()
        system_prompt = prompt["system_prompt"]
        assert "Você é" in system_prompt
        assert any(role in system_prompt for role in ["Product Manager", "Senior Product Manager", "Product Owner"])

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt = self.get_prompt()
        system_prompt = prompt["system_prompt"]
        assert "Markdown" in system_prompt
        assert "Como [persona], eu quero [objetivo], para que [benefício]" in system_prompt

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt = self.get_prompt()
        system_prompt = prompt["system_prompt"]
        assert "Few-shot example 1" in system_prompt
        assert "Entrada:" in system_prompt
        assert "Saída esperada:" in system_prompt

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt = self.get_prompt()
        serialized_prompt = yaml.safe_dump(prompt, allow_unicode=True)
        assert "[TODO]" not in serialized_prompt
        assert "TODO" not in serialized_prompt

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompt = self.get_prompt()
        is_valid, errors = validate_prompt_structure(prompt)
        assert is_valid, f"Prompt inválido: {errors}"
        assert len(prompt.get("techniques_applied", [])) >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
