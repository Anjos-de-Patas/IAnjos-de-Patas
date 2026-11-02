"""TED 03 - Experimento A: diagnóstico complementar.

Reproduz exatamente a divisão e o modelo de src/ted03.py e gera:
  1. métricas no treino final e no teste, para discutir sobreajuste;
  2. os termos de maior peso para cada espécie (coeficientes da Regressão Logística).

Uso (na raiz do projeto):
    python src/ted03_termos_relevantes.py

Saídas em reports/TED03/:
    sobreajuste.csv         - acurácia e F1 macro no treino final e no teste
    termos_relevantes.csv   - termos de maior peso para Gato e para Cão
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ted03 import ROOT, SEED, clean_text, logistic, metrics, normalized_group  # noqa: E402

TOP_N = 15


def main():
    df = pd.read_csv(ROOT / "data/processed/petfinder_mini_tratado.csv", encoding="utf-8-sig")
    df["texto"] = clean_text(df["Description"])
    df = df[df["texto"].ne("")].reset_index(drop=True)
    df["grupo"] = df["texto"].map(normalized_group)

    outer = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    tv_pos, te_pos = next(outer.split(df["texto"], df["Type"], df["grupo"]))
    trainval, test = df.iloc[tv_pos], df.iloc[te_pos]
    assert (len(trainval), len(test)) == (9225, 2303), "divisão diferente da registrada em ted03.py"

    modelo = logistic().fit(trainval["texto"], trainval["Type"])
    linhas = []
    for nome, parte in [("Treino final", trainval), ("Teste", test)]:
        m = metrics(parte["Type"], modelo.predict(parte["texto"]))
        linhas.append({"conjunto": nome, "registros": m["n"],
                       "acuracia": round(m["accuracy"], 4), "f1_macro": round(m["f1_macro"], 4)})
    sobre = pd.DataFrame(linhas)

    termos = modelo.named_steps["tfidf"].get_feature_names_out()
    coef = modelo.named_steps["model"].coef_[0]          # positivo -> classes_[1] (Dog)
    c0, c1 = modelo.named_steps["model"].classes_
    ordem = np.argsort(coef)
    top = pd.DataFrame([{"posicao": i + 1,
                         f"termo_{c0}": termos[ordem[i]], f"peso_{c0}": round(-coef[ordem[i]], 3),
                         f"termo_{c1}": termos[ordem[-(i + 1)]], f"peso_{c1}": round(coef[ordem[-(i + 1)]], 3)}
                        for i in range(TOP_N)])

    out = ROOT / "reports/TED03"
    out.mkdir(parents=True, exist_ok=True)
    sobre.to_csv(out / "sobreajuste.csv", index=False, encoding="utf-8-sig")
    top.to_csv(out / "termos_relevantes.csv", index=False, encoding="utf-8-sig")
    print("Treino x teste:\n", sobre.to_string(index=False))
    print(f"\nTermos de maior peso ({c0} x {c1}):\n", top.to_string(index=False))


if __name__ == "__main__":
    main()
