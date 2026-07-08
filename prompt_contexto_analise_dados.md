# Prompt de Contexto para Analise Exploratoria de Dados

Use este arquivo como prompt para que o Claude replique a mesma estrutura de analise para qualquer nova base de dados. Basta fornecer este arquivo junto com o dataset (CSV, Excel, etc.) e o Claude criara automaticamente todos os arquivos do projeto.

---

## Instrucoes para o Claude

Voce recebera uma base de dados (CSV ou similar). Sua tarefa e criar um projeto completo de analise exploratoria de dados com os seguintes entregaveis:

### 1. Analise Inicial dos Dados

Antes de tudo, faca uma analise completa do dataset:
- Leia o arquivo e identifique todas as colunas, tipos de dados e quantidade de registros
- Verifique valores nulos, duplicados e inconsistencias
- Identifique variaveis categoricas (e seus valores unicos) e numericas (com estatisticas descritivas)
- Entenda o contexto dos dados (o que cada coluna representa)

### 2. Criacao de 15 Perguntas Analiticas

Com base na analise inicial, crie **15 perguntas** que:
- Cubram diferentes dimensoes dos dados (demograficas, temporais, financeiras, comportamentais, correlacoes)
- Gerem **insights acionaveis** para o negocio
- Variem em complexidade (agregacoes simples, cruzamentos, correlacoes, segmentacoes, rankings)
- Sejam respondidas exclusivamente com os dados disponiveis

**Distribuicao sugerida de temas:**
- 2-3 perguntas sobre **receita/valores** (agregacoes, rankings)
- 2-3 perguntas sobre **demografia/segmentacao** (faixas etarias, genero, localizacao)
- 2-3 perguntas sobre **tendencias/evolucao** (temporal, sazonalidade)
- 2-3 perguntas sobre **comportamento** (frequencia, preferencias, fidelidade)
- 2-3 perguntas sobre **correlacoes e metricas compostas** (relacoes entre variaveis, indices)
- 1-2 perguntas sobre **segmentacao avancada** (quartis, perfis multidimensionais)

### 3. Respostas com Pandas e PostgreSQL

Para **cada pergunta**, fornecer:
- **Codigo Pandas** funcional e executavel
- **Query PostgreSQL** equivalente (documentada, nao executada)
- **Insight por escrito** explicando o resultado e sua relevancia para o negocio

**Importante:** o codigo Pandas e a query SQL de cada pergunta devem chegar ao **mesmo resultado**. Atencao especial a:
- Ordenacao: sempre usar `ORDER BY` explicito no SQL (sem ele a ordem e indefinida) e desempates deterministicos (ex.: `ORDER BY qtd DESC, "Coluna"`) quando houver contagens empatadas
- Quartis: `pd.qcut` equivale a limites via `PERCENTILE_CONT` + `CASE`, e nao a `NTILE()` (que quebra empates arbitrariamente)

**Padroes de codigo Pandas a seguir:**
```python
# Usar chaining com parenteses para legibilidade
resultado = (
    df.groupby('coluna').agg(
        metrica1=('coluna_valor', 'sum'),
        metrica2=('coluna_valor', 'mean')
    )
    .sort_values('metrica1', ascending=False)
    .round(2)
)
```

**Padroes de SQL a seguir:**
```sql
-- Usar nomes de colunas com aspas duplas quando contem espacos
-- Usar CTEs para consultas complexas
-- Usar ROUND() e ::numeric para formatacao
-- Usar CASE WHEN para faixas/categorias
-- Usar NTILE(), RANK(), ROW_NUMBER() para rankings
-- Usar CORR(), STDDEV() para estatisticas
SELECT "Coluna Com Espaco",
       COUNT(*) AS qtd,
       ROUND(AVG("Valor")::numeric, 2) AS media
FROM nome_tabela
GROUP BY "Coluna Com Espaco"
ORDER BY qtd DESC;
```

### 4. Arquivos a Criar

#### README.md

Estrutura obrigatoria:

```markdown
# Titulo do Projeto

Descricao em 2-3 linhas sobre os dados e o que o projeto faz.

---

## Sobre os Dados

| Arquivo | Descricao | Registros |
|---------|-----------|-----------|
| `arquivo.csv` | Descricao | X registros, Y colunas |

**Fonte:** [Link para a fonte dos dados]

### Principais Variaveis

| Variavel | Descricao | Tipo | Exemplos |
|----------|-----------|------|----------|
| Coluna1  | O que e   | Tipo | Valores  |

---

## 15 Perguntas e Respostas

Cada pergunta e respondida com duas abordagens: **Pandas** (Python) e **PostgreSQL**.

---

### Pergunta N: [Texto da pergunta]

**Objetivo:** [1 linha explicando o proposito]

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white"><img src="https://img.shields.io/badge/Pandas-Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python"></picture> &nbsp;<b>Pandas</b></summary>

<br>

> ```python
> # Codigo Pandas aqui
> ```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white"><img src="https://img.shields.io/badge/PostgreSQL-SQL-4169E1?style=flat&logo=postgresql&logoColor=white" alt="SQL"></picture> &nbsp;<b>PostgreSQL</b></summary>

<br>

> ```sql
> -- Query SQL aqui
> ```

</details>

**Insight:** [Texto explicativo com numeros em negrito]

---

[Repetir para as 15 perguntas]

## Conclusao

| Tema | Perguntas | Principal Descoberta |
|------|-----------|---------------------|
| ... | ... | ... |

> **Insight geral:** [Resumo]

---

## Estrutura do Projeto
## Tecnologias Utilizadas
## Como Executar
```

#### analise_[nome].ipynb (Jupyter Notebook)

Estrutura de celulas (total: 84 celulas):

**Abertura (8 celulas):**
- [0] Markdown: Titulo + descricao
- [1] Markdown: "## Configuracao e Carregamento dos Dados"
- [2] Markdown: "### Opcao 1: Carregamento via API do Kaggle" (explicacao + instrucoes .env)
- [3] Code: bloco Kaggle API (import kaggle, authenticate, download, load)
- [4] Markdown: "### Opcao 2: Carregamento local" (explicacao)
- [5] Code: imports + load CSV local + print metadata
- [6] Code: df.head()
- [7] Code: df.describe(include="all").T

**Bloco Kaggle API (celula 3) - template:**

```python
import glob
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from dotenv import load_dotenv

# Carrega o KAGGLE_API_TOKEN do arquivo .env para o ambiente.
# A biblioteca kaggle le a variavel automaticamente ao autenticar;
# na ausencia dela, o arquivo ~/.kaggle/kaggle.json tambem e aceito.
load_dotenv()

api = KaggleApi()
api.authenticate()

DATASET = "usuario/nome-do-dataset"  # Alterar conforme o dataset

api.dataset_download_files(DATASET, path="/tmp/dados", unzip=True, quiet=False)

arquivos = glob.glob("/tmp/dados/*")
print(arquivos)

df = pd.read_csv("/tmp/dados/nome_do_arquivo.csv", index_col=0)
print(f"\nDataset carregado via API: {df.shape[0]} registros, {df.shape[1]} colunas")
```

**Para cada pergunta (5 celulas x 15 = 75 celulas):**
- [N+0] Markdown: "---\n## Pergunta X: [texto]\n\n[contexto]"
- [N+1] Markdown: "### Resposta com Pandas"
- [N+2] Code: codigo Pandas executavel
- [N+3] Markdown: "### Resposta com PostgreSQL\n\n```sql\n[query]\n```"
- [N+4] Markdown: "### Analise\n\n[insight com numeros em negrito]"

**Fechamento (1 celula):**
- [83] Markdown: "## Conclusao" com tabela resumo

### 5. Checklist de Qualidade

Antes de entregar, verificar:
- [ ] Todas as 15 perguntas cobrem diferentes dimensoes dos dados
- [ ] Codigo Pandas e funcional (testar executando)
- [ ] Queries SQL usam sintaxe PostgreSQL valida
- [ ] Pandas e SQL de cada pergunta chegam ao mesmo resultado (ordenacao e desempates deterministicos)
- [ ] Insights contem numeros reais extraidos da analise
- [ ] README.md usa tags `<details>` para secoes colapsaveis
- [ ] README.md usa badges visuais para Pandas e PostgreSQL
- [ ] Notebook tem exatamente 84 celulas (8 + 75 + 1)
- [ ] Notebook tem 65 celulas markdown e 19 celulas code
- [ ] Notebook executado com as saidas salvas (visiveis no GitHub)
- [ ] Nenhum arquivo contem credenciais ou dados sensiveis

---

## Exemplo de Uso

Para usar este prompt:

1. Abra uma nova conversa com o Claude
2. Envie este arquivo como contexto
3. Envie o dataset (CSV, Excel, etc.)
4. Diga: "Analise esta base de dados seguindo as instrucoes do prompt de contexto"
5. O Claude criara automaticamente todos os arquivos do projeto

O Claude ira:
1. Analisar o dataset completamente (colunas, tipos, valores unicos, estatisticas)
2. Criar 15 perguntas relevantes para o dominio dos dados
3. Responder cada pergunta com Pandas e PostgreSQL
4. Executar o codigo para obter numeros reais para os insights
5. Criar o README.md com markdown formatado para GitHub
6. Criar o notebook .ipynb com a estrutura padrao
7. Verificar a qualidade e consistencia de todos os arquivos
