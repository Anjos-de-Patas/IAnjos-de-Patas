# IAnjos de Patas — Big Data e Ciência de Dados

## Equipe

- Carinne da Silva Borges
- Rogério Mota de Melo
- Júlio Cesar Lima dos Reis
- João Pedro Strasser Santos

## Sobre o projeto

O IAnjos de Patas é um projeto desenvolvido inicialmente na disciplina de Inteligência Artificial, a partir de uma problemática identificada na ONG Anjos de Patas.

A proposta é facilitar a busca por animais para adoção de acordo com as preferências do interessado. O MVP permite que o usuário descreva o perfil de animal que procura em linguagem natural, transformando essa descrição em critérios estruturados que possam ser comparados com as informações cadastradas dos animais.

Na disciplina de Big Data e Ciência de Dados, o projeto utiliza uma base pública para apoiar a seleção, compreensão, preparação e análise dos dados necessários aos testes do MVP.

## Conjunto de dados

Foi selecionado o conjunto de dados **PetFinder.my mini**, derivado de dados da plataforma PetFinder.my.

A base original utilizada possui **11.537 registros e 15 atributos**, relacionados às características dos animais, incluindo:

- tipo do animal;
- idade;
- raça;
- sexo;
- cores;
- porte;
- comprimento do pelo;
- vacinação;
- castração;
- condição de saúde;
- taxa de adoção;
- descrição;
- quantidade de fotos;
- velocidade histórica de adoção.

Essas informações permitem trabalhar com características semelhantes às utilizadas pelo MVP para localizar animais compatíveis com as preferências dos adotantes.

## Fonte de dados

**PetFinder.my mini**, arquivo `petfinder-mini.csv` disponibilizado no tutorial oficial do TensorFlow sobre dados estruturados.

- Documentação: https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers
- Download da base: https://storage.googleapis.com/download.tensorflow.org/data/petfinder-mini.zip
- Base original: https://www.kaggle.com/competitions/petfinder-adoption-prediction/data

Na inspeção inicial foram identificados **11.537 registros e 15 colunas**.

## TED01 — Seleção e inspeção inicial dos dados

No TED01 foi realizada a seleção do conjunto de dados e sua inspeção inicial.

Foram identificados:

- 11.537 registros;
- 15 atributos;
- 9 valores ausentes em `Description`;
- 143 ocorrências excedentes de linhas integralmente repetidas;
- valores `Not Sure` em `Vaccinated` e `Sterilized`;
- valores numéricos que exigiam análise antes de qualquer tratamento.

A etapa também permitiu avaliar a adequação e as limitações da base em relação às necessidades do MVP.

## TED02 — Limpeza, preparação e análise exploratória

No TED02 foram realizadas a limpeza, a preparação e a análise exploratória do conjunto de dados.

Durante o tratamento:

- as 143 ocorrências excedentes de linhas integralmente repetidas foram removidas, mantendo uma ocorrência de cada registro;
- os 9 valores ausentes em `Description` foram substituídos por `Sem descrição`;
- as categorias das variáveis categóricas foram verificadas;
- valores como `Not Sure` e `No Color` foram preservados por possuírem significado próprio;
- possíveis valores extremos das variáveis numéricas foram analisados sem remoção automática;
- os 15 atributos originais foram mantidos.

Após o tratamento, a base processada passou a possuir **11.394 registros, 15 atributos, nenhum valor ausente e nenhuma linha integralmente duplicada**.

A análise exploratória investigou a distribuição de características como tipo, idade e porte, além de relações entre essas características e a variável histórica `AdoptionSpeed`.

`AdoptionSpeed` foi utilizada somente para análise exploratória dos dados históricos. Ela não constitui critério de compatibilidade, indicador de disponibilidade atual ou mecanismo de previsão de adoção no MVP.

## Limitações

A base não representa os animais atualmente cadastrados pela ONG Anjos de Patas, pois os dados são provenientes da PetFinder.my, na Malásia.

Além disso, não possui atributos estruturados específicos sobre temperamento, convivência com crianças, convivência com outros animais ou disponibilidade atual, informações relevantes para representar integralmente algumas preferências dos adotantes.

Também foram identificadas possíveis inconsistências em alguns valores de idade. Esses registros foram preservados porque não foi encontrada uma regra suficientemente segura para realizar correções automáticas sem risco de modificar valores válidos.

Por essas razões, a base é utilizada para exploração e testes dos filtros básicos do MVP, não para representar os animais atualmente disponíveis na ONG.

## Estrutura do projeto

```text
data/
├── raw/
└── processed/

docs/
├── TED01_BigData_IAnjos.docx
├── TED01_BigData_IAnjos.pdf
├── TED01_IA_Original.pdf
├── TED02_BigData_IAnjos.docx
└── TED02_BigData_IAnjos.pdf

notebooks/
├── TED01/
└── TED02/
    └── ted02_limpeza_eda.ipynb

reports/
├── inspecao.json
└── metodo.md

src/
├── inspecionar_dados.py
└── obter_dados.py
```

Os arquivos CSV utilizados localmente não são versionados no repositório.

## Materiais

| Caminho | Conteúdo |
|---|---|
| `docs/TED01_IA_Original.pdf` | Trabalho original da disciplina de Inteligência Artificial |
| `docs/TED01_BigData_IAnjos.pdf` | Documento da etapa TED01 |
| `docs/TED01_BigData_IAnjos.docx` | Versão editável do documento TED01 |
| `docs/TED02_BigData_IAnjos.pdf` | Documento Técnico v2.0 com a etapa TED02 |
| `docs/TED02_BigData_IAnjos.docx` | Versão editável do Documento Técnico v2.0 |
| `notebooks/TED02/ted02_limpeza_eda.ipynb` | Notebook de limpeza, preparação e análise exploratória |
| `data/README.md` | Fonte e instruções para obtenção dos dados |
| `data/manifesto.json` | Informações sobre o conjunto de dados utilizado |
| `reports/inspecao.json` | Resultados da inspeção inicial |
| `reports/metodo.md` | Procedimentos utilizados e limitações |
| `src/inspecionar_dados.py` | Script utilizado na inspeção inicial |
| `src/obter_dados.py` | Script utilizado para obtenção dos dados |

## Como reproduzir

### 1. Obter os dados

O conjunto de dados pode ser baixado a partir da fonte indicada anteriormente ou utilizando:

```bash
python src/obter_dados.py
```

O arquivo original deve ser mantido em:

```text
data/raw/petfinder-mini.csv
```

### 2. Executar a inspeção inicial

A inspeção desenvolvida no TED01 pode ser executada utilizando:

```bash
python src/inspecionar_dados.py data/raw/petfinder-mini.csv
```

### 3. Executar o TED02

A limpeza, preparação e análise exploratória estão documentadas no notebook:

```text
notebooks/TED02/ted02_limpeza_eda.ipynb
```

O notebook utiliza Python, pandas e matplotlib.

Após sua execução, a versão processada é armazenada localmente em:

```text
data/processed/petfinder-mini-tratado.csv
```

Os arquivos CSV das pastas `data/raw/` e `data/processed/` são mantidos localmente e ignorados pelo Git.