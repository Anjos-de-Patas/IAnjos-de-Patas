# IAnjos de Patas — TED 01 de Big Data e Ciência de Dados

## Equipe

- Carinne da Silva Borges
- Rogério Mota de Melo
- Júlio Cesar Lima dos Reis
- João Pedro Strasser Santos

## Sobre o projeto

O IAnjos de Patas é um projeto desenvolvido inicialmente na disciplina de Inteligência Artificial, a partir de uma problemática
identificada na ONG Anjos de Patas.

A proposta é facilitar a busca por animais para adoção de acordo com as preferências do interessado. O MVP permite que o usuário
descreva o perfil de animal que procura em linguagem natural, transformando essa descrição em critérios que possam ser comparados 
com as informações cadastradas dos animais.

## Conjunto de dados

Para esta etapa foi selecionado o conjunto de dados **PetFinder.my mini**, derivado de dados da plataforma PetFinder.my.

A base possui 11.537 registros e 15 atributos relacionados às características dos animais, incluindo:

- tipo do animal;
- idade;
- raça;
- sexo;
- porte;
- comprimento do pelo;
- vacinação;
- castração;
- condição de saúde;
- descrição;
- quantidade de fotos;
- velocidade de adoção.

Essas informações permitem trabalhar com características semelhantes às utilizadas pelo MVP para localizar animais compatíveis 
com as preferências dos adotantes.

## Fonte de dados

**PetFinder.my mini**, arquivo `petfinder-mini.csv` disponível no tutorial oficial do TensorFlow sobre dados estruturados.

- Documentação: https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers
- Download da base: https://storage.googleapis.com/download.tensorflow.org/data/petfinder-mini.zip
- Base original: https://www.kaggle.com/competitions/petfinder-adoption-prediction/data
- Na inspeção inicial foram identificados 11.537 registros e 15 colunas.

## Limitações

A base não representa os animais cadastrados pela ONG Anjos de Patas, pois os dados são provenientes da PetFinder.my, na Malásia. 
Além disso, não possui atributos estruturados específicos sobre temperamento, convivência com crianças, convivência com outros animais 
ou disponibilidade atual, informações que seriam relevantes para representar integralmente algumas preferências dos adotantes.

Na inspeção inicial foram identificadas 9 descrições vazias, 143 linhas idênticas excedentes e valores `Not Sure` nos atributos relacionados 
à vacinação e castração. Essas ocorrências serão consideradas nas etapas posteriores de análise e tratamento dos dados.

## Materiais

| Caminho | Conteúdo |
|---|---|
| `docs/TED01_IA_Original.pdf` | Trabalho de IA anexado sem alterações |
| `docs/TED01_BigData_IAnjos.pdf` | Relatório da seleção e análise inicial |
| `docs/TED01_BigData_IAnjos.docx` | Versão editável do relatório |
| `data/README.md` | Fonte e instruções para obtenção dados|
| `data/manifesto.json` | Informações sobre o conjunto de dados utilizado|
| `reports/inspecao.json` | Resultados da inspeção inicial |
| `reports/metodo.md` | Procedimentos utilizados e limitações|
| `src/inspecionar_dados.py` | Script para inspeção inicial dos dados |
| `src/obter_dados.py` | Script para obtenção dos dados |

## Como obter os dados

O conjunto de dados pode ser baixado pelo link informado na seção "Fonte de dados".

Também é possível realizar o download utilizando o script disponível no projeto:

```bash
python src/obter_dados.py
```

Após a obtenção dos dados, a inspeção inicial pode ser realizada com:

```bash
python src/inspecionar_dados.py data/petfinder-mini.csv
```