# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através das métricas do desafio (Tone, Acceptance Criteria, User Story Format, Completeness)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

```bash
# Executar o pull do prompt base
python3 src/pull_prompts.py

# Fazer push da versão otimizada
python3 src/push_prompts.py

# Executar avaliação final
python3 src/evaluate.py

==================================================
AVALIAÇÃO DE PROMPTS OTIMIZADOS
==================================================

Prompt: guilhermefaleiros/bug_to_user_story_v2

Métricas do desafio:
  - Tone Score: 0.90 ✓
  - Acceptance Criteria Score: 0.93 ✓
  - User Story Format Score: 0.96 ✓
  - Completeness Score: 0.94 ✓

📊 MÉDIA GERAL: 0.9332

✅ STATUS: APROVADO
```

---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Técnicas Aplicadas (Fase 2)

O prompt final em `prompts/bug_to_user_story_v2.yml` foi refinado com um conjunto de técnicas combinadas para maximizar as quatro métricas do desafio.

1. **Role Prompting**
   - O modelo recebe o papel de **Product Manager sênior**.
   - Isso ajudou a elevar o tom profissional, a coerência do vocabulário e a qualidade geral da user story.

2. **Few-shot Learning**
   - O prompt contém exemplos completos de entrada e saída.
   - Os exemplos cobrem validação, segurança, compatibilidade entre navegadores e inconsistência de dashboard.
   - Isso aumentou a consistência do formato e dos critérios de aceitação.

3. **Rubric-based Prompting**
   - O `system_prompt` orienta explicitamente o modelo para os eixos de avaliação do desafio: tom, formato, critérios e completude.
   - Isso reduziu respostas vagas e ajudou a aproximar o output do padrão esperado pelos avaliadores.

4. **Negative Examples**
   - O prompt lista padrões proibidos, como benefícios vazios, user stories frias e critérios sem resultado observável.
   - Isso foi importante para evitar regressões em `Tone` e `User Story Format`.

5. **Emotional Priming**
   - A instrução central reforça que o bug deve ser traduzido como uma necessidade real de alguém que foi impedido de completar uma tarefa.
   - Isso elevou a qualidade do benefício descrito no `Para que`, que passou a ficar mais humano e concreto.

6. **Structured Output / Skeleton of Thought**
   - A saída foi rigidamente estruturada em:
     - `## User Story`
     - `## Critérios de Aceitação`
     - `## Contexto Técnico`
     - `## Impacto e Prioridade`
     - `## Observações`
   - Essa estrutura ajudou a aumentar `Completeness` sem prejudicar `Format`.

### Como as técnicas foram aplicadas na prática

- Persona explícita e especializada no `system_prompt`.
- Template fixo para `Como / Eu quero / Para que`.
- Requisitos obrigatórios no `user_prompt`.
- Regras para preservar detalhes como IDs, valores, severidade, browsers, HTTP status e mensagens de erro.
- Critérios em `Dado / Quando / Então` sempre numerados e testáveis.
- Seções adicionais condicionais para contexto técnico e impacto.
- Exemplos positivos concretos e padrões proibidos.

## Processo de Refinamento

O refinamento do prompt ocorreu de forma iterativa, com foco nas métricas que estavam mais baixas em cada rodada.

1. **Versão inicial otimizada**
   - Introduziu persona, few-shot e estrutura básica.
   - Melhorou bastante a organização, mas ainda deixava oscilações em `Tone` e `Format`.

2. **Refino de tom e benefício**
   - O prompt passou a enfatizar linguagem positiva e benefício real para a pessoa afetada.
   - Isso reduziu user stories frias e genéricas.

3. **Refino de formato**
   - A saída foi travada em um template mais rígido com `## User Story` e linhas `Como / Eu quero / Para que`.
   - Isso elevou `User Story Format Score`.

4. **Refino de completude**
   - O prompt passou a exigir a preservação explícita de IDs, valores, severidade, endpoints, navegadores, mensagens e impacto.
   - Isso melhorou `Completeness Score`.

5. **Ajustes finais orientados por avaliação**
   - Os few-shots foram expandidos.
   - Foram adicionados padrões proibidos e instruções mais fortes de empatia.
   - O README, os testes e o prompt foram alinhados para garantir qualidade e conformidade ao mesmo tempo.

---

## Resultados Finais

### Resultado aprovado

- **Prompt publicado:** `guilhermefaleiros/bug_to_user_story_v2`

### Métricas finais obtidas

| Métrica                   | Nota       |
| ------------------------- | ---------- |
| Tone Score                | **0.90**   |
| Acceptance Criteria Score | **0.93**   |
| User Story Format Score   | **0.96**   |
| Completeness Score        | **0.94**   |
| Média Geral               | **0.9332** |

### Status final

- Todas as 4 métricas ficaram `>= 0.9`
- A média geral ficou `>= 0.9`
- O prompt foi **aprovado**

### Evidência de avaliação

- Projeto no LangSmith: `prompt-optimization-challenge-resolved`
- Prompt avaliado: `guilhermefaleiros/bug_to_user_story_v2`
- Resultado final do CLI:
  - `Tone Score: 0.90`
  - `Acceptance Criteria Score: 0.93`
  - `User Story Format Score: 0.96`
  - `Completeness Score: 0.94`
  - `Média Geral: 0.9332`

### Screenshots

#### Dataset criado no LangSmith

![Dataset de avaliação no LangSmith](images/dataset.png)

#### Execução final aprovada

![Execução final aprovada da avaliação](images/execution.png)

#### Traces e detalhes da execução

![Traces da avaliação no LangSmith](images/traces.png)

### Tabela comparativa

| Aspecto                        | Prompt v1         | Prompt v2                                                                                                 |
| ------------------------------ | ----------------- | --------------------------------------------------------------------------------------------------------- |
| Persona                        | Genérica          | Product Manager sênior com foco na pessoa impactada                                                       |
| Formato                        | Pouco prescritivo | Markdown com template fixo `Como / Eu quero / Para que`                                                   |
| Few-shot                       | Não               | Sim, 4 exemplos completos                                                                                 |
| Edge cases                     | Não               | Sim                                                                                                       |
| Critérios de aceitação         | Implícitos        | Obrigatórios, numerados e testáveis                                                                       |
| Contexto técnico               | Não orientado     | Obrigatório quando houver dados relevantes                                                                |
| Impacto e prioridade           | Não               | Incluído quando aplicável                                                                                 |
| Técnicas de prompt engineering | Não documentadas  | Role Prompting, Few-shot, Rubric-based Prompting, Negative Examples, Emotional Priming, Structured Output |

---

## Como Executar

### Pré-requisitos

- Python 3.9+
- Credenciais válidas do LangSmith
- Uma API Key de um provider suportado:
  - OpenAI
  - Google Gemini

### Instalação

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Configuração do `.env`

Preencha ao menos:

```bash
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=...
USERNAME_LANGSMITH_HUB=...

LLM_PROVIDER=openai
OPENAI_API_KEY=...
LLM_MODEL=gpt-5-mini
EVAL_MODEL=gpt-5
```

Ou, se preferir Gemini:

```bash
LLM_PROVIDER=google
GOOGLE_API_KEY=...
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
```

### Fase 1: Pull do prompt base

```bash
python3 src/pull_prompts.py
```

Arquivos gerados:

- `prompts/bug_to_user_story_v1.yml`
- `prompts/raw_prompts.yml`

### Fase 2: Prompt otimizado

O prompt otimizado já está pronto em:

```bash
prompts/bug_to_user_story_v2.yml
```

### Fase 3: Push para o LangSmith Hub

```bash
python3 src/push_prompts.py
```

O script tenta publicar:

- `{USERNAME_LANGSMITH_HUB}/bug_to_user_story_v2`

### Fase 4: Avaliação

```bash
python3 src/evaluate.py
```

Critério de aprovação implementado:

- Todas as 4 métricas devem ser `>= 0.9`
- A média geral também deve ser `>= 0.9`

### Fase 5: Testes locais

```bash
pytest tests/test_prompts.py
```

---

## Pacotes recomendados

```python
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder utilizado na versão aprovada**: `gpt-5-mini`
- **Modelo de LLM para avaliação utilizado na versão aprovada**: `gpt-5`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull dos Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme instruções no `README.md` do repositório base)
2. Acessar o script `src/pull_prompts.py` que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompts:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva os prompts localmente em `prompts/raw_prompts.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **pelo menos duas** das seguintes técnicas:
   - **Few-shot Learning**: Fornecer exemplos claros de entrada/saída
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot)
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Criar o script `src/push_prompts.py` que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixa-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Tone Score >= 0.9
- Acceptance Criteria Score >= 0.9
- User Story Format Score >= 0.9
- Completeness Score >= 0.9

MÉDIA das 4 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 4 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
desafio-prompt-engineer/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml       # Prompt inicial (após pull)
│   └── bug_to_user_story_v2.yml # Seu prompt otimizado
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith
│   ├── push_prompts.py       # Push ao LangSmith
│   ├── evaluate.py           # Avaliação automática
│   ├── metrics.py            # 4 métricas implementadas
│   ├── dataset.py            # 15 exemplos de bugs
│   └── utils.py              # Funções auxiliares
│
├── tests/
│   └── test_prompts.py       # Testes de validação
│
```

**O que você vai criar:**

- `prompts/bug_to_user_story_v2.yml` - Seu prompt otimizado
- `tests/test_prompts.py` - Seus testes de validação
- `src/pull_prompt.py` Script de pull do repositório da fullcycle
- `src/push_prompt.py` Script de push para o seu repositório
- `README.md` - Documentação do seu processo de otimização

**O que já vem pronto:**

- Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- 4 métricas específicas para Bug to User Story
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/desafio-prompt-engineer/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 5. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

1. **Repositório público no GitHub** (fork do repositório base) contendo:
   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com:

2. **README.md deve conter:**

   A) **Seção "Técnicas Aplicadas (Fase 2)"**:
   - Quais técnicas avançadas você escolheu para refatorar os prompts
   - Justificativa de por que escolheu cada técnica
   - Exemplos práticos de como aplicou cada técnica

   B) **Seção "Resultados Finais"**:
   - Link público do seu dashboard do LangSmith mostrando as avaliações
   - Screenshots das avaliações com as notas mínimas de 0.9 atingidas
   - Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

   C) **Seção "Como Executar"**:
   - Instruções claras e detalhadas de como executar o projeto
   - Pré-requisitos e dependências
   - Comandos para cada fase do projeto

3. **Evidências no LangSmith**:
   - Link público (ou screenshots) do dashboard do LangSmith
   - Devem estar visíveis:
     - Dataset de avaliação com ≥ 20 exemplos
     - Execuções dos prompts v1 (ruins) com notas baixas
     - Execuções dos prompts v2 (otimizados) com notas ≥ 0.9
     - Tracing detalhado de pelo menos 3 exemplos

---

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de PRs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.9 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final
