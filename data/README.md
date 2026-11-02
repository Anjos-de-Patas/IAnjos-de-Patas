# Obtenção da base

Base: **PetFinder.my mini**  
Arquivo: `petfinder-mini.csv`

## Fonte

Fonte original:  
https://www.kaggle.com/competitions/petfinder-adoption-prediction/data

Documentação consultada:  
https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers

Download:  
https://storage.googleapis.com/download.tensorflow.org/data/petfinder-mini.zip

## Como obter os dados

Baixe o arquivo ZIP pelo link acima e extraia `petfinder-mini/petfinder-mini.csv`, colocando o arquivo em `data/raw/petfinder-mini.csv`.

Também é possível realizar o download executando, na raiz do projeto:

```bash
python src/obter_dados.py

```

O conjunto utilizado na análise possui **11.537 registros e 15 colunas**.

## Observações

O pacote local contém uma cópia dos dados para reprodução privada. Os CSVs de `raw/` e `processed/` são ignorados pelo Git. A publicação depende da confirmação das condições de redistribuição da fonte. Sem essa confirmação, publique os scripts e manifestos e obtenha a base pelo comando acima.

Depois do download, execute `python src/ted02.py` para gerar `data/processed/petfinder_mini_tratado.csv` e `python src/ted03.py` para treinar e avaliar os modelos. O SHA-256 esperado da base bruta está em `manifesto_ted02.json`.

A base PetFinder.my mini é uma versão simplificada dos dados e não corresponde ao conjunto completo da competição. Os registros são utilizados neste projeto apenas para fins de estudo e não representam animais atualmente disponíveis para adoção pela ONG Anjos de Patas.
