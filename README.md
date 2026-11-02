# IAnjos de Patas — Big Data e Ciência de Dados

## Equipe

- Carinne da Silva Borges
- Rogério Mota de Melo
- Júlio Cesar Lima dos Reis
- João Pedro Strasser Santos

Curso de Análise e Desenvolvimento de Sistemas — UNIBALSAS, Balsas (MA), 2026.

## Sobre o projeto

O IAnjos de Patas é um projeto desenvolvido inicialmente na disciplina de Inteligência Artificial, a partir de uma problemática identificada na Sociedade Protetora dos Animais Anjos de Patas.

A proposta é facilitar a busca por animais para adoção de acordo com as preferências do interessado. O MVP permite que o usuário descreva o perfil de animal que procura em linguagem natural, transformando essa descrição em critérios estruturados que possam ser comparados com as informações cadastradas dos animais.

Na disciplina de Big Data e Ciência de Dados, o projeto utiliza a base pública **PetFinder.my mini** para apoiar a seleção, a preparação, a análise e, na TED 03, a modelagem com Machine Learning.

## Documento técnico

| Etapa | Documento |
|---|---|
| **Versão 3.0 (TED 01 + TED 02 + TED 03)** | [`docs/TED03_Documento_Tecnico_v3.0.pdf`](docs/TED03_Documento_Tecnico_v3.0.pdf) |
| Seções da TED 03 em formato editável | `docs/TED03_Documento_Tecnico_v3.0_secoes18-24.docx` |
| TED 02 revisada (base usada na TED 03) | `docs/TED02_Documento_Tecnico_v2_revisado.pdf` |
| TED 02 (entrega de 26/09) | `docs/TED02_BigData_IAnjos.pdf` / `.docx` |
| TED 01 | `docs/TED01_BigData_IAnjos.pdf` / `.docx` e `docs/TED01_IA_Original.pdf` |

## Fonte de dados

**PetFinder.my mini**, arquivo `petfinder-mini.csv`, disponibilizado no tutorial do TensorFlow sobre dados estruturados.

- Documentação: https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers
- Download: https://storage.googleapis.com/download.tensorflow.org/data/petfinder-mini.zip
- Base original: https://www.kaggle.com/competitions/petfinder-adoption-prediction/data

A base possui **11.537 registros e 15 colunas**. Os CSVs não são versionados, pois a licença de redistribuição não foi confirmada; o SHA-256 da versão usada está em `data/manifesto_ted02.json`.

## TED 01 — Seleção e inspeção inicial

Seleção do conjunto de dados e inspeção inicial: 11.537 registros, 15 atributos, 9 descrições ausentes, 143 linhas integralmente repetidas excedentes e valores `Not Sure` em `Vaccinated` e `Sterilized`.

## TED 02 — Limpeza, preparação e análise exploratória

A entrega de 26/09 (`notebooks/TED02/ted02_limpeza_eda.ipynb`) removeu as duplicatas e gerou uma base de 11.394 registros.

Para a TED 03, a preparação foi revisada em `src/ted02.py` (`notebooks/TED02/TED02_Petfinder.ipynb`): os **11.537 registros são preservados** e recebem seis colunas auxiliares (21 no total), como `linha_origem` e `duplicata_excedente`. Assim, as duplicatas ficam marcadas em vez de apagadas, o que permite agrupá-las na divisão dos dados e ocultá-las na exibição sem perder a rastreabilidade. Essa é a base utilizada na TED 03: `data/processed/petfinder_mini_tratado.csv`.

## TED 03 — Modelagem preditiva e Machine Learning

### Experimento A: classificação da espécie pela descrição

- **Tarefa:** classificação supervisionada binária. Entrada: `Description`. Alvo: `Type` (Cat/Dog).
- **Divisão:** `StratifiedGroupKFold` por grupo de descrição normalizada (sem o mesmo texto em treino, validação e teste).
- **Modelos:** linha de base majoritária, Naive Bayes + TF-IDF e Regressão Logística + TF-IDF, com escolha por F1 macro na validação.

| Resultado no teste (2.303 registros) | Valor |
|---|---|
| Acurácia da Regressão Logística | **92,71%** |
| F1 macro | **92,57%** |
| F1 macro da linha de base | 36,42% |
| F1 macro no treino final (sobreajuste) | 96,91% |
| F1 macro com termos de espécie ocultos (sensibilidade) | 83,79% |

### Experimento B: recuperação e ordenação por similaridade

- **Tarefa:** aplicar filtros obrigatórios e ordenar os candidatos por k-NN (cosseno) em relação às preferências opcionais.
- **Representação:** OneHotEncoder (peso 3) + TF-IDF (peso 1). Sem variável-alvo; `AdoptionSpeed` não é usado.
- **Avaliação:** 17 cenários escritos pela equipe (`reports/TED03_recomendacao/consultas_avaliacao.json`), comparando ordem original, regra explícita e k-NN.

| Preferências atendidas no top-5 (16 cenários com candidatos) | Valor |
|---|---|
| Ordem original | 41,04% |
| Regra explícita | **96,25%** |
| k-NN | **96,25%** (empate em todos os cenários) |
| Filtros obrigatórios respeitados | 100% |

**Conclusão:** para atributos estruturados confirmados, a ordenação por regras é tão eficaz quanto o k-NN e mais fácil de auditar; o Machine Learning fica reservado para casos com ganho demonstrável, como textos livres. Nenhum modelo foi integrado ao site da ONG.

## Estrutura

```text
data/
├── README.md, manifesto.json, manifesto_ted02.json
├── raw/                 (petfinder-mini.csv, local)
└── processed/           (petfinder_mini_tratado.csv, local)
docs/                    documentos técnicos das TEDs 01, 02 e 03
notebooks/
├── TED02/               ted02_limpeza_eda.ipynb, TED02_Petfinder.ipynb
└── TED03/               TED03_Machine_Learning.ipynb, TED03_Recomendacao_por_Similaridade.ipynb
reports/
├── inspecao.json, metodo.md
├── TED02/               tabelas e figuras da análise exploratória
├── TED03/               Experimento A: métricas, partições, predições, sobreajuste, termos e figuras
└── TED03_recomendacao/  Experimento B: cenários, métricas por consulta, top-5 e figuras
src/
├── obter_dados.py, inspecionar_dados.py       TED 01
├── ted02.py                                    TED 02 (gera a base tratada)
├── ted03.py, ted03_termos_relevantes.py        TED 03 — Experimento A
├── ted03_recomendacao.py, demo_recomendacao.py TED 03 — Experimento B
└── verificar_projeto.py                        conferência de integridade
```

Os CSVs de resultados não contêm o texto das descrições.

## Como reproduzir

Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/ted02.py                    # baixa a base e gera data/processed
.\.venv\Scripts\python.exe src/ted03.py                    # Experimento A
.\.venv\Scripts\python.exe src/ted03_termos_relevantes.py  # sobreajuste e termos de maior peso
.\.venv\Scripts\python.exe src/ted03_recomendacao.py       # Experimento B
.\.venv\Scripts\python.exe src/demo_recomendacao.py Q01    # demonstração (Q17: consulta sem resultado)
.\.venv\Scripts\python.exe src/verificar_projeto.py        # conferência de integridade
.\.venv\Scripts\python.exe -m jupyterlab                   # notebooks
```

Linux/macOS: use `python3 -m venv .venv` e `.venv/bin/python` no lugar de `.\.venv\Scripts\python.exe`.

`src/ted02.py` baixa a base se `data/raw/petfinder-mini.csv` não existir (requer internet). As versões exatas usadas na execução registrada estão em `requirements-reproducao.txt`; versões diferentes podem alterar ligeiramente as previsões.

## Limitações

A base não representa os animais da ONG Anjos de Patas: são anúncios históricos da PetFinder.my, na Malásia, com descrições majoritariamente em inglês. Não há atributos estruturados de temperamento, convivência com crianças ou com outros animais, nem de disponibilidade atual. Os experimentos são provas de conceito acadêmicas e não validam o chatbot em português.
