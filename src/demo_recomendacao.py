"""Demonstração do Experimento B para um cenário específico.

Uso (na raiz do projeto):
    python src/demo_recomendacao.py Q01
    python src/demo_recomendacao.py Q17      # consulta sem candidatos
    python src/demo_recomendacao.py --listar

Mostra o pedido, os filtros aplicados, a quantidade de candidatos elegíveis e os
cinco primeiros resultados do k-NN, sem exibir as descrições originais.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ted03_recomendacao import CONSULTAS, ROOT, atendidas, filtrar, preparar  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("consulta", nargs="?", default="Q01")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--input", type=Path, default=ROOT / "data/processed/petfinder_mini_tratado.csv")
    a = ap.parse_args()

    if a.listar:
        for q in CONSULTAS:
            print(f"{q['id']}: {q['pedido']}")
        return

    q = next((c for c in CONSULTAS if c["id"].lower() == a.consulta.lower()), None)
    if q is None:
        sys.exit(f"Consulta {a.consulta} não encontrada. Use --listar.")

    _, _, _, catalogo, rec = preparar(a.input)
    cand = filtrar(catalogo, q["obrigatorio"])
    print(f"Pedido ({q['id']}): {q['pedido']}")
    print(f"Obrigatório:  {q['obrigatorio']}")
    print(f"Preferências: {q['preferencias']}")
    print(f"Candidatos elegíveis no catálogo de teste: {len(cand)}\n")
    if cand.empty:
        print("Nenhum perfil atende a todos os requisitos obrigatórios.")
        print("Nenhum animal é sugerido e os filtros não são relaxados.")
        return

    top = rec.knn(cand, q)
    top["preferencias_atendidas"] = atendidas(top, q["preferencias"])
    cols = ["linha_origem", *q["obrigatorio"], *q["preferencias"], "AgeBand",
            "preferencias_atendidas", "similaridade"]
    cols = list(dict.fromkeys(cols))
    print(top[cols].round({"similaridade": 3}).to_string(index=False))
    print(f"\n(preferências possíveis por perfil: {len(q['preferencias'])})")


if __name__ == "__main__":
    main()
