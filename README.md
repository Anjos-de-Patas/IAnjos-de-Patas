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

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3 | Linguagem de todos os scripts e notebooks |
| pandas e NumPy | Leitura, limpeza e preparação dos dados |
| scikit-learn | TF-IDF, OneHotEncoder, Regressão Logística, Naive Bayes, k-NN, divisão dos dados e métricas |
| matplotlib | Gráficos das TEDs 02 e 03 |
| Jupyter (JupyterLab) | Notebooks comentados de cada etapa |
| Git e GitHub | Versionamento e entrega |

## Documento técnico

| Etapa | Documento |
|---|---|
| **Versão Final 4.0 (TEDs 01 a 04)** | [`docs/TED04_Documento_Tecnico_Final_v4.0.pdf`](docs/TED04_Documento_Tecnico_Final_v4.0.pdf) |
| Versão Final editável (Word) | `docs/TED04_Documento_Tecnico_Final_v4.0.docx` |
| **Apresentação final (Data Storytelling)** | [`presentation/apresentacao-final.pdf`](presentation/apresentacao-final.pdf) e `presentation/apresentacao-final.pptx` |
| Versão 3.0 (TED 01 + TED 02 + TED 03) | [`docs/TED03_Documento_Tecnico_v3.0.pdf`](docs/TED03_Documento_Tecnico_v3.0.pdf) |
| Versão 3.0 editável (Word) | `docs/TED03_Documento_Tecnico_v3.0.docx` |
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

## TED 04 — Integração dos resultados, ética, LGPD e Data Storytelling

A versão final do Documento Técnico preserva as seções 1 a 24 da versão 3.0 e acrescenta as seções 25 a 38: contexto, dados, preparação, análise exploratória, modelagem, resultados, interpretação integrada, análise ética, privacidade e LGPD, limitações, Data Storytelling, conclusões, evolução da solução e histórico de versões.

Principais pontos:

- **Interpretação integrada:** a IA deve interpretar a linguagem livre do pedido; filtros e regras sobre dados confirmados devem decidir quais animais mostrar. É a arquitetura adotada no assistente da aplicação web do projeto (https://anjos-de-patas.netlify.app).
- **Privacidade:** a base não tem colunas com dados de pessoas, mas 4 descrições livres contêm telefone e nome de contato. Por isso os CSV não são publicados e os arquivos de resultados não contêm descrições.
- **Reprodutibilidade:** em 23/11/2026 os scripts das TEDs 02 e 03 foram executados novamente a partir da fonte oficial (SHA-256 conferido) e geraram arquivos de resultados idênticos aos versionados.
- **Figura-síntese:** `src/ted04_storytelling.py` lê os JSON de resultados e gera `reports/TED04/figures/01_sintese_resultados.png`.

O documento é gerado a partir da versão 3.0 por `src/gerar_documento_final.py` (python-docx).

## Estrutura

```text
data/
├── README.md, manifesto.json, manifesto_ted02.json
├── raw/                 (petfinder-mini.csv, local)
└── processed/           (petfinder_mini_tratado.csv, local)
docs/                    documentos técnicos das TEDs 01 a 04 (versão final: TED04_Documento_Tecnico_Final_v4.0)
notebooks/
├── TED02/               ted02_limpeza_eda.ipynb, TED02_Petfinder.ipynb
└── TED03/               TED03_Machine_Learning.ipynb, TED03_Recomendacao_por_Similaridade.ipynb
reports/
├── inspecao.json, metodo.md
├── TED02/               tabelas e figuras da análise exploratória
├── TED03/               Experimento A: métricas, partições, predições, sobreajuste, termos e figuras
├── TED03_recomendacao/  Experimento B: cenários, métricas por consulta, top-5 e figuras
└── TED04/               figura-síntese de Data Storytelling
presentation/            apresentação final (PDF e PowerPoint)
src/
├── obter_dados.py, inspecionar_dados.py       TED 01
├── ted02.py                                    TED 02 (gera a base tratada)
├── ted03.py, ted03_termos_relevantes.py        TED 03 — Experimento A
├── ted03_recomendacao.py, demo_recomendacao.py TED 03 — Experimento B
├── ted04_storytelling.py                       TED 04 — figura-síntese
├── gerar_documento_final.py                    TED 04 — documento técnico final (a partir da v3.0)
├── formatar_tabelas.py                         TED 04 — padroniza as tabelas do documento final
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
.\.venv\Scripts\python.exe src/ted04_storytelling.py      # TED 04: figura-síntese
.\.venv\Scripts\python.exe src/verificar_projeto.py        # conferência de integridade
.\.venv\Scripts\python.exe -m jupyterlab                   # notebooks
```

Linux/macOS: use `python3 -m venv .venv` e `.venv/bin/python` no lugar de `.\.venv\Scripts\python.exe`.

`src/ted02.py` baixa a base se `data/raw/petfinder-mini.csv` não existir (requer internet). As versões exatas usadas na execução registrada estão em `requirements-reproducao.txt`; versões diferentes podem alterar ligeiramente as previsões.

## Limitações

A base não representa os animais da ONG Anjos de Patas: são anúncios históricos da PetFinder.my, na Malásia, com descrições majoritariamente em inglês. Não há atributos estruturados de temperamento, convivência com crianças ou com outros animais, nem de disponibilidade atual. Os experimentos são provas de conceito acadêmicas e não validam o chatbot em português. Algumas descrições contêm dados pessoais de contato; não publique os CSV nem as descrições em novos relatórios.
