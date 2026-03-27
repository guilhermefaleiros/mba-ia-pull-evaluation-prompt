"""
Script COMPLETO para avaliar prompts otimizados.

Este script:
1. Carrega dataset de avaliação de arquivo .jsonl (datasets/bug_to_user_story.jsonl)
2. Cria/atualiza dataset no LangSmith
3. Puxa prompts otimizados do LangSmith Hub com fallback local
4. Executa prompts contra o dataset
5. Calcula as 4 métricas exigidas no desafio
6. Publica resultados no dashboard do LangSmith
7. Exibe resumo no terminal

Suporta múltiplos providers de LLM:
- OpenAI (gpt-4o, gpt-4o-mini)
- Google Gemini (gemini-1.5-flash, gemini-1.5-pro)

Configure o provider no arquivo .env através da variável LLM_PROVIDER.
"""

import os
import sys
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import (
    check_env_vars,
    format_score,
    print_section_header,
    get_llm as get_configured_llm,
    load_yaml,
    build_chat_prompt_template,
)
from metrics import (
    evaluate_tone_score,
    evaluate_acceptance_criteria_score,
    evaluate_user_story_format_score,
    evaluate_completeness_score,
)
from dataset import load_dataset_from_jsonl

load_dotenv()


def get_llm():
    return get_configured_llm(temperature=0)


def create_evaluation_dataset(client: Client, dataset_name: str, jsonl_path: str) -> str:
    print(f"Criando dataset de avaliação: {dataset_name}...")

    try:
        examples = load_dataset_from_jsonl(jsonl_path)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {jsonl_path}")
        print("\nCertifique-se de que o arquivo datasets/bug_to_user_story.jsonl existe.")
        return dataset_name
    except Exception as e:
        print(f"❌ Erro ao carregar dataset: {e}")
        return dataset_name

    if not examples:
        print("❌ Nenhum exemplo carregado do arquivo .jsonl")
        return dataset_name

    print(f"   ✓ Carregados {len(examples)} exemplos do arquivo {jsonl_path}")

    try:
        datasets = client.list_datasets(dataset_name=dataset_name)
        existing_dataset = None

        for ds in datasets:
            if ds.name == dataset_name:
                existing_dataset = ds
                break

        if existing_dataset:
            print(f"   ✓ Dataset '{dataset_name}' já existe, usando existente")
            return dataset_name
        else:
            dataset = client.create_dataset(dataset_name=dataset_name)

            for example in examples:
                client.create_example(
                    dataset_id=dataset.id,
                    inputs=example["inputs"],
                    outputs=example["outputs"]
                )

            print(f"   ✓ Dataset criado com {len(examples)} exemplos")
            return dataset_name

    except Exception as e:
        print(f"   ⚠️  Erro ao criar dataset: {e}")
        return dataset_name


def pull_prompt_from_langsmith(prompt_name: str) -> ChatPromptTemplate:
    try:
        print(f"   Puxando prompt do LangSmith Hub: {prompt_name}")
        client = Client()
        prompt = client.pull_prompt(prompt_name)
        print(f"   ✓ Prompt carregado com sucesso")
        return prompt

    except Exception as e:
        print(f"   ⚠️  Falha ao carregar do Hub: {e}")
        local_yaml = load_yaml("prompts/bug_to_user_story_v2.yml") or {}
        local_prompt = local_yaml.get(prompt_name) or local_yaml.get(prompt_name.split("/")[-1])
        if local_prompt:
            print("   ✓ Usando fallback local em prompts/bug_to_user_story_v2.yml")
            return build_chat_prompt_template(local_prompt)

        raise


def evaluate_prompt_on_example(
    prompt_template: ChatPromptTemplate,
    example: Any,
    llm: Any
) -> Dict[str, Any]:
    try:
        inputs = example.inputs if hasattr(example, 'inputs') else {}
        outputs = example.outputs if hasattr(example, 'outputs') else {}

        chain = prompt_template | llm

        response = chain.invoke(inputs)
        answer = response.content

        reference = outputs.get("reference", "") if isinstance(outputs, dict) else ""

        bug_report = inputs.get("bug_report", "") if isinstance(inputs, dict) else ""

        return {
            "answer": answer,
            "reference": reference,
            "bug_report": bug_report
        }

    except Exception as e:
        print(f"      ⚠️  Erro ao avaliar exemplo: {e}")
        import traceback
        print(f"      Traceback: {traceback.format_exc()}")
        return {
            "answer": "",
            "reference": "",
            "bug_report": ""
        }


def evaluate_prompt(
    prompt_name: str,
    dataset_name: str,
    client: Client
) -> Dict[str, float]:
    print(f"\n🔍 Avaliando: {prompt_name}")

    try:
        prompt_template = pull_prompt_from_langsmith(prompt_name)

        examples = list(client.list_examples(dataset_name=dataset_name))
        print(f"   Dataset: {len(examples)} exemplos")

        llm = get_llm()

        tone_scores = []
        acceptance_scores = []
        format_scores = []
        completeness_scores = []

        print("   Avaliando exemplos...")

        for i, example in enumerate(examples[:10], 1):
            result = evaluate_prompt_on_example(prompt_template, example, llm)

            if result["answer"]:
                tone = evaluate_tone_score(result["bug_report"], result["answer"], result["reference"])
                acceptance = evaluate_acceptance_criteria_score(result["bug_report"], result["answer"], result["reference"])
                story_format = evaluate_user_story_format_score(result["bug_report"], result["answer"], result["reference"])
                completeness = evaluate_completeness_score(result["bug_report"], result["answer"], result["reference"])

                tone_scores.append(tone["score"])
                acceptance_scores.append(acceptance["score"])
                format_scores.append(story_format["score"])
                completeness_scores.append(completeness["score"])

                print(
                    f"      [{i}/{min(10, len(examples))}] "
                    f"Tone:{tone['score']:.2f} "
                    f"Criteria:{acceptance['score']:.2f} "
                    f"Format:{story_format['score']:.2f} "
                    f"Complete:{completeness['score']:.2f}"
                )

        avg_tone = sum(tone_scores) / len(tone_scores) if tone_scores else 0.0
        avg_acceptance = sum(acceptance_scores) / len(acceptance_scores) if acceptance_scores else 0.0
        avg_format = sum(format_scores) / len(format_scores) if format_scores else 0.0
        avg_completeness = sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0.0

        return {
            "tone": round(avg_tone, 4),
            "acceptance_criteria": round(avg_acceptance, 4),
            "user_story_format": round(avg_format, 4),
            "completeness": round(avg_completeness, 4),
        }

    except Exception as e:
        print(f"   ❌ Erro na avaliação: {e}")
        return {
            "tone": 0.0,
            "acceptance_criteria": 0.0,
            "user_story_format": 0.0,
            "completeness": 0.0,
        }


def display_results(prompt_name: str, scores: Dict[str, float]) -> bool:
    print("\n" + "=" * 50)
    print(f"Prompt: {prompt_name}")
    print("=" * 50)

    print("\nMétricas do desafio:")
    print(f"  - Tone Score: {format_score(scores['tone'], threshold=0.9)}")
    print(f"  - Acceptance Criteria Score: {format_score(scores['acceptance_criteria'], threshold=0.9)}")
    print(f"  - User Story Format Score: {format_score(scores['user_story_format'], threshold=0.9)}")
    print(f"  - Completeness Score: {format_score(scores['completeness'], threshold=0.9)}")

    average_score = sum(scores.values()) / len(scores)
    all_thresholds_met = all(score >= 0.9 for score in scores.values())

    print("\n" + "-" * 50)
    print(f"📊 MÉDIA GERAL: {average_score:.4f}")
    print("-" * 50)

    passed = average_score >= 0.9 and all_thresholds_met

    if passed:
        print("\n✅ STATUS: APROVADO (média >= 0.9 e todas as métricas >= 0.9)")
    else:
        print("\n❌ STATUS: REPROVADO")
        print(f"⚠️  Média atual: {average_score:.4f} | Necessário: 0.9000")
        if not all_thresholds_met:
            print("⚠️  Pelo menos uma métrica individual ficou abaixo de 0.9")

    return passed


def main():
    print_section_header("AVALIAÇÃO DE PROMPTS OTIMIZADOS")

    provider = os.getenv("LLM_PROVIDER", "openai")
    llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    eval_model = os.getenv("EVAL_MODEL", "gpt-4o")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    google_key = os.getenv("GOOGLE_API_KEY", "")

    print(f"Provider: {provider}")
    print(f"Modelo Principal: {llm_model}")
    print(f"Modelo de Avaliação: {eval_model}\n")
    if provider == "openai":
        suffix = openai_key[-6:] if openai_key else "N/A"
        print(f"OpenAI API Key carregada: {'sim' if openai_key else 'não'}")
        print(f"Sufixo da chave OpenAI: ***{suffix}\n")
    elif provider in ["google", "gemini"]:
        suffix = google_key[-6:] if google_key else "N/A"
        print(f"Google API Key carregada: {'sim' if google_key else 'não'}")
        print(f"Sufixo da chave Google: ***{suffix}\n")

    required_vars = ["LANGSMITH_API_KEY", "LLM_PROVIDER"]
    if provider == "openai":
        required_vars.append("OPENAI_API_KEY")
    elif provider in ["google", "gemini"]:
        required_vars.append("GOOGLE_API_KEY")

    if not check_env_vars(required_vars):
        return 1

    client = Client()
    project_name = os.getenv("LANGCHAIN_PROJECT", "prompt-optimization-challenge-resolved")

    jsonl_path = "datasets/bug_to_user_story.jsonl"

    if not Path(jsonl_path).exists():
        print(f"❌ Arquivo de dataset não encontrado: {jsonl_path}")
        print("\nCertifique-se de que o arquivo existe antes de continuar.")
        return 1

    dataset_name = f"{project_name}-eval"
    create_evaluation_dataset(client, dataset_name, jsonl_path)

    print("\n" + "=" * 70)
    print("PROMPTS PARA AVALIAR")
    print("=" * 70)
    print("\nEste script irá puxar prompts do LangSmith Hub.")
    print("Certifique-se de ter feito push dos prompts antes de avaliar:")
    print("  python src/push_prompts.py\n")

    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()
    prompts_to_evaluate = [f"{username}/bug_to_user_story_v2" if username else "bug_to_user_story_v2"]

    all_passed = True
    evaluated_count = 0
    results_summary = []

    for prompt_name in prompts_to_evaluate:
        evaluated_count += 1

        try:
            scores = evaluate_prompt(prompt_name, dataset_name, client)

            passed = display_results(prompt_name, scores)
            all_passed = all_passed and passed

            results_summary.append({
                "prompt": prompt_name,
                "scores": scores,
                "passed": passed
            })

        except Exception as e:
            print(f"\n❌ Falha ao avaliar '{prompt_name}': {e}")
            all_passed = False

            results_summary.append({
                "prompt": prompt_name,
                "scores": {
                    "tone": 0.0,
                    "acceptance_criteria": 0.0,
                    "user_story_format": 0.0,
                    "completeness": 0.0,
                },
                "passed": False
            })

    print("\n" + "=" * 50)
    print("RESUMO FINAL")
    print("=" * 50 + "\n")

    if evaluated_count == 0:
        print("⚠️  Nenhum prompt foi avaliado")
        return 1

    print(f"Prompts avaliados: {evaluated_count}")
    print(f"Aprovados: {sum(1 for r in results_summary if r['passed'])}")
    print(f"Reprovados: {sum(1 for r in results_summary if not r['passed'])}\n")

    if all_passed:
        print("✅ Todos os prompts atingiram média >= 0.9!")
        print(f"\n✓ Confira os resultados em:")
        print(f"  https://smith.langchain.com/projects/{project_name}")
        print("\nPróximos passos:")
        print("1. Documente o processo no README.md")
        print("2. Capture screenshots das avaliações")
        print("3. Faça commit e push para o GitHub")
        return 0
    else:
        print("⚠️  Alguns prompts não atingiram média >= 0.9")
        print("\nPróximos passos:")
        print("1. Refatore os prompts com score baixo")
        print("2. Faça push novamente: python src/push_prompts.py")
        print("3. Execute: python src/evaluate.py novamente")
        return 1

if __name__ == "__main__":
    sys.exit(main())
