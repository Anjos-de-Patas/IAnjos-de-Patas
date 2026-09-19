import argparse
import csv
import io
import json
from collections import Counter
from pathlib import Path


def analisar(path):
    raw = Path(path).read_bytes()

    reader = csv.DictReader(
        io.StringIO(raw.decode("utf-8-sig"))
    )

    fields = reader.fieldnames
    rows = list(reader)

    if not rows or not fields:
        raise ValueError("CSV vazio ou sem cabeçalho")

    # Conta campos vazios em cada coluna
    missing = {
        coluna: sum(not linha[coluna].strip() for linha in rows)
        for coluna in fields
    }

    # Representa cada linha como uma tupla para identificar linhas idênticas
    tuples = [
        tuple(linha[coluna] for coluna in fields)
        for linha in rows
    ]

    # Inspeção das colunas numéricas
    numeric = {}

    for coluna in ["Age", "Fee", "PhotoAmt", "AdoptionSpeed"]:
        valores = []
        invalidos = 0

        for linha in rows:
            try:
                valores.append(float(linha[coluna]))
            except (ValueError, TypeError):
                invalidos += 1

        numeric[coluna] = {
            "min": min(valores) if valores else None,
            "max": max(valores) if valores else None,
            "negativos": sum(valor < 0 for valor in valores),
            "zeros": sum(valor == 0 for valor in valores),
            "nao_numericos_ou_vazios": invalidos,
        }

    # Contagem das principais categorias
    categorical = {
        coluna: dict(Counter(linha[coluna] for linha in rows))
        for coluna in [
            "Type",
            "Gender",
            "MaturitySize",
            "Vaccinated",
            "Sterilized",
            "Health",
            "AdoptionSpeed",
        ]
    }

    return {
        "arquivo": Path(path).name,
        "registros": len(rows),
        "numero_colunas": len(fields),
        "colunas": fields,
        "vazios_por_coluna": missing,
        "duplicatas_excedentes": len(rows) - len(set(tuples)),
        "definicao_duplicata": (
            "Linha identica nas 15 colunas; primeira ocorrencia preservada "
            "na contagem. Nao prova duplicidade de animal."
        ),
        "categorias": categorical,
        "numericas": numeric,
        "criterio_vazio": (
            "Campo vazio ou composto somente por espacos; "
            "Not Sure nao e contado como vazio."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Inspeciona o conjunto de dados PetFinder.my mini."
    )

    parser.add_argument(
        "csv",
        type=Path,
        help="Caminho para o arquivo CSV.",
    )

    parser.add_argument(
        "--saida",
        type=Path,
        default=Path("reports/inspecao.json"),
        help="Arquivo JSON que recebera os resultados.",
    )

    args = parser.parse_args()

    report = analisar(args.csv)

    args.saida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.saida.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        f"{report['registros']} registros; "
        f"{report['numero_colunas']} colunas; "
        f"relatorio em {args.saida}"
    )