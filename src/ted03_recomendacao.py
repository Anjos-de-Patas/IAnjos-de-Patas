"""TED 03 - Experimento B: recuperação e ordenação de perfis por similaridade.

Execução (na raiz do projeto):
    python src/ted03_recomendacao.py

Formulação
    1. Requisitos obrigatórios eliminam os perfis que não os atendem (filtro rígido).
    2. Os candidatos restantes são ordenados por vizinhos mais próximos (k-NN,
       distância de cosseno) em relação à preferência representada numericamente.
    Não há variável-alvo: o método é não paramétrico e baseado em instâncias.

Comparadores (mesmos filtros obrigatórios nos três):
    - ordem original: primeiros elegíveis na sequência da base (linha_origem);
    - regra explícita: mais preferências opcionais atendidas primeiro;
    - k-NN: OneHotEncoder (peso 3) + TF-IDF da descrição (peso 1), cosseno.

Limites: as consultas foram escritas pela equipe e convertidas manualmente em
atributos; não se avalia a interpretação de frases em português, nem
compatibilidade, temperamento ou disponibilidade atual. AdoptionSpeed não é usado.

Saídas em reports/TED03_recomendacao/:
    consultas_avaliacao.json, resultados.json, resultados_por_consulta.csv,
    top5_resultados.csv (sem descrições) e figures/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import unicodedata
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.sparse as sp
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GroupShuffleSplit
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder, normalize

ROOT = Path(__file__).resolve().parents[1]
SEED = 42
TOP_K = 5
PESO_CATEGORICO = 3.0
PESO_TEXTO = 1.0

# Campos estruturados usados como filtros e/ou preferências.
CAMPOS = ["Type", "Gender", "MaturitySize", "FurLength", "Vaccinated",
          "Sterilized", "Health", "Color1", "Breed1", "AgeBand"]

# Cenários de avaliação escritos pela equipe. "pedido" é a frase em português;
# a conversão para atributos foi feita manualmente (não pelo chatbot).
CONSULTAS = [
    {"id": "Q01", "pedido": "Quero uma gata pequena e vacinada; de preferência castrada e de pelo curto.",
     "obrigatorio": {"Type": "Cat", "Gender": "Female", "MaturitySize": "Small", "Vaccinated": "Yes"},
     "preferencias": {"Sterilized": "Yes", "FurLength": "Short"}},
    {"id": "Q02", "pedido": "Procuro um cachorro filhote; se possível vacinado e de porte médio.",
     "obrigatorio": {"Type": "Dog", "AgeBand": "0-6 meses"},
     "preferencias": {"Vaccinated": "Yes", "MaturitySize": "Medium"}},
    {"id": "Q03", "pedido": "Uma cadela adulta castrada; prefiro pelagem curta e cor preta.",
     "obrigatorio": {"Type": "Dog", "Gender": "Female", "AgeBand": "acima de 24 meses", "Sterilized": "Yes"},
     "preferencias": {"FurLength": "Short", "Color1": "Black"}},
    {"id": "Q04", "pedido": "Gato macho saudável; de preferência jovem e já vacinado.",
     "obrigatorio": {"Type": "Cat", "Gender": "Male", "Health": "Healthy"},
     "preferencias": {"AgeBand": "7-24 meses", "Vaccinated": "Yes"}},
    {"id": "Q05", "pedido": "Cachorro de porte grande, vacinado; se der, castrado e de pelo médio.",
     "obrigatorio": {"Type": "Dog", "MaturitySize": "Large", "Vaccinated": "Yes"},
     "preferencias": {"Sterilized": "Yes", "FurLength": "Medium"}},
    {"id": "Q06", "pedido": "Gatinho filhote de pelo longo; tanto faz o sexo, prefiro branco.",
     "obrigatorio": {"Type": "Cat", "AgeBand": "0-6 meses", "FurLength": "Long"},
     "preferencias": {"Color1": "White"}},
    {"id": "Q07", "pedido": "Cão sem raça definida, vacinado e castrado; preferência por cor marrom e porte médio.",
     "obrigatorio": {"Type": "Dog", "Breed1": "Mixed Breed", "Vaccinated": "Yes", "Sterilized": "Yes"},
     "preferencias": {"Color1": "Brown", "MaturitySize": "Medium"}},
    {"id": "Q08", "pedido": "Gata adulta; prefiro castrada, vacinada e de pelo curto.",
     "obrigatorio": {"Type": "Cat", "Gender": "Female", "AgeBand": "acima de 24 meses"},
     "preferencias": {"Sterilized": "Yes", "Vaccinated": "Yes", "FurLength": "Short"}},
    {"id": "Q09", "pedido": "Cachorro pequeno; se possível macho, jovem e vacinado.",
     "obrigatorio": {"Type": "Dog", "MaturitySize": "Small"},
     "preferencias": {"Gender": "Male", "AgeBand": "7-24 meses", "Vaccinated": "Yes"}},
    {"id": "Q10", "pedido": "Gato vacinado e castrado; preferência por cor cinza.",
     "obrigatorio": {"Type": "Cat", "Vaccinated": "Yes", "Sterilized": "Yes"},
     "preferencias": {"Color1": "Gray"}},
    {"id": "Q11", "pedido": "Cadela filhote; de preferência vacinada e de cor preta.",
     "obrigatorio": {"Type": "Dog", "Gender": "Female", "AgeBand": "0-6 meses"},
     "preferencias": {"Vaccinated": "Yes", "Color1": "Black"}},
    {"id": "Q12", "pedido": "Cachorro de pelo longo; preferência por porte pequeno e castrado.",
     "obrigatorio": {"Type": "Dog", "FurLength": "Long"},
     "preferencias": {"MaturitySize": "Small", "Sterilized": "Yes"}},
    {"id": "Q13", "pedido": "Gato da raça Domestic Short Hair; prefiro fêmea jovem e vacinada.",
     "obrigatorio": {"Type": "Cat", "Breed1": "Domestic Short Hair"},
     "preferencias": {"Gender": "Female", "AgeBand": "7-24 meses", "Vaccinated": "Yes"}},
    {"id": "Q14", "pedido": "Cão macho adulto, saudável; de preferência castrado, vacinado e grande.",
     "obrigatorio": {"Type": "Dog", "Gender": "Male", "AgeBand": "acima de 24 meses", "Health": "Healthy"},
     "preferencias": {"Sterilized": "Yes", "Vaccinated": "Yes", "MaturitySize": "Large"}},
    {"id": "Q15", "pedido": "Gato de porte médio; preferência por cor creme e pelo médio.",
     "obrigatorio": {"Type": "Cat", "MaturitySize": "Medium"},
     "preferencias": {"Color1": "Cream", "FurLength": "Medium"}},
    {"id": "Q16", "pedido": "Cachorro jovem vacinado; preferência por fêmea dourada.",
     "obrigatorio": {"Type": "Dog", "AgeBand": "7-24 meses", "Vaccinated": "Yes"},
     "preferencias": {"Gender": "Female", "Color1": "Golden"}},
    {"id": "Q17", "pedido": "Gata filhote, grande, de pelo longo, castrada e com ferimento grave.",
     "obrigatorio": {"Type": "Cat", "Gender": "Female", "AgeBand": "0-6 meses", "MaturitySize": "Large",
                     "FurLength": "Long", "Sterilized": "Yes", "Health": "Serious Injury"},
     "preferencias": {"Color1": "White"}},
]


def faixa_idade(meses: int) -> str:
    if meses <= 6:
        return "0-6 meses"
    if meses <= 24:
        return "7-24 meses"
    return "acima de 24 meses"


def grupo_descricao(texto, linha) -> str:
    """Descrições iguais (NFKC, casefold, espaços) formam o mesmo grupo.
    Descrição vazia não agrupa registros diferentes."""
    t = " ".join(unicodedata.normalize("NFKC", str(texto or "")).casefold().split())
    if not t:
        return f"vazio-{linha}"
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def carregar(caminho: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho, encoding="utf-8-sig")
    df["Description"] = df["Description"].fillna("").astype(str)
    df["AgeBand"] = df["Age"].map(faixa_idade)
    df["grupo"] = [grupo_descricao(t, l) for t, l in zip(df["Description"], df["linha_origem"])]
    return df


class Recomendador:
    """Vetorização ajustada no subconjunto de ajuste; índice k-NN montado sobre os candidatos."""

    def __init__(self, ajuste: pd.DataFrame):
        self.ohe = OneHotEncoder(handle_unknown="ignore").fit(ajuste[CAMPOS].astype(str))
        self.tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=25000,
                                     sublinear_tf=True, strip_accents="unicode").fit(ajuste["Description"])

    def vetorizar(self, registros: pd.DataFrame, texto: pd.Series | None = None):
        cat = normalize(self.ohe.transform(registros[CAMPOS].astype(str))) * PESO_CATEGORICO
        txt = self.tfidf.transform(registros["Description"] if texto is None else texto) * PESO_TEXTO
        return normalize(sp.hstack([cat, txt]).tocsr())

    def vetor_consulta(self, consulta: dict, texto_livre: str = ""):
        campos = {**consulta["preferencias"], **consulta["obrigatorio"]}
        linha = pd.DataFrame([{c: campos.get(c, "__ausente__") for c in CAMPOS}])
        linha["Description"] = texto_livre
        return self.vetorizar(linha)

    def knn(self, candidatos: pd.DataFrame, consulta: dict, k: int = TOP_K, texto_livre: str = ""):
        if candidatos.empty:
            return candidatos.assign(similaridade=[])
        X = self.vetorizar(candidatos)
        nn = NearestNeighbors(n_neighbors=min(k, len(candidatos)), metric="cosine").fit(X)
        dist, idx = nn.kneighbors(self.vetor_consulta(consulta, texto_livre))
        out = candidatos.iloc[idx[0]].copy()
        out["similaridade"] = 1 - dist[0]
        return out


def filtrar(catalogo: pd.DataFrame, obrigatorio: dict) -> pd.DataFrame:
    mask = np.ones(len(catalogo), dtype=bool)
    for campo, valor in obrigatorio.items():
        mask &= catalogo[campo].astype(str).eq(valor).to_numpy()
    return catalogo[mask].sort_values("linha_origem")


def atendidas(df: pd.DataFrame, preferencias: dict) -> np.ndarray:
    if df.empty:
        return np.zeros(0)
    return np.sum([df[c].astype(str).eq(v).to_numpy() for c, v in preferencias.items()], axis=0)


def ordem_original(cand, consulta, k=TOP_K):
    return cand.head(k)


def regra_explicita(cand, consulta, k=TOP_K):
    c = cand.assign(_n=atendidas(cand, consulta["preferencias"]))
    return c.sort_values(["_n", "linha_origem"], ascending=[False, True]).head(k).drop(columns="_n")


def avaliar(top: pd.DataFrame, consulta: dict) -> dict:
    if top.empty:
        return {"aderencia": None, "todas_preferencias": None, "obrigatorios_ok": None}
    n_pref = len(consulta["preferencias"])
    hits = atendidas(top, consulta["preferencias"])
    obrig = np.all([top[c].astype(str).eq(v).to_numpy() for c, v in consulta["obrigatorio"].items()], axis=0)
    return {"aderencia": float(np.mean(hits / n_pref)),
            "todas_preferencias": float(np.mean(hits == n_pref)),
            "obrigatorios_ok": float(np.mean(obrig))}


def figuras(por_consulta: pd.DataFrame, agregado: dict, pasta: Path):
    pasta.mkdir(parents=True, exist_ok=True)
    nomes = {"ordem_original": "Ordem original", "regra": "Ordenação por regras", "knn": "k-NN + vetorização"}

    fig, ax = plt.subplots(figsize=(8, 4.4))
    vals = [agregado[m]["aderencia_media"] * 100 for m in nomes]
    bars = ax.bar(list(nomes.values()), vals, color=["#9aa5b1", "#3b7dd8", "#1f4e99"])
    for b, v in zip(bars, vals):
        ax.annotate(f"{v:.2f}%".replace(".", ","), (b.get_x() + b.get_width() / 2, v),
                    xytext=(0, 4), textcoords="offset points", ha="center", fontsize=9)
    ax.set_ylim(0, 110)
    ax.set_ylabel("Preferências atendidas no top-5 (%)")
    ax.set_title("Aderência operacional média (consultas com candidatos)")
    fig.tight_layout(); fig.savefig(pasta / "01_aderencia_media.png", dpi=160); plt.close(fig)

    validas = por_consulta[por_consulta["candidatos"] > 0]
    x = np.arange(len(validas)); w = 0.27
    fig, ax = plt.subplots(figsize=(10, 4.8))
    for j, (m, rot) in enumerate(nomes.items()):
        ax.bar(x + (j - 1) * w, validas[f"aderencia_{m}"] * 100, w, label=rot,
               color=["#9aa5b1", "#3b7dd8", "#1f4e99"][j])
    ax.set_xticks(x, validas["id"])
    ax.set_ylim(0, 105)
    ax.set_ylabel("Preferências atendidas no top-5 (%)")
    ax.set_title("Comparação por cenário - catálogo de teste")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False)
    fig.tight_layout(); fig.savefig(pasta / "02_comparacao_por_cenario.png", dpi=160); plt.close(fig)


def preparar(entrada: Path):
    df = carregar(entrada)
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED)
    i_aj, i_te = next(gss.split(df, groups=df["grupo"]))
    ajuste, teste = df.iloc[i_aj].copy(), df.iloc[i_te].copy()
    assert not set(ajuste["grupo"]) & set(teste["grupo"]), "grupo de descrição compartilhado"
    catalogo = teste[~teste["duplicata_excedente"]].copy()
    return df, ajuste, teste, catalogo, Recomendador(ajuste)


def executar(entrada: Path, saida: Path):
    df, ajuste, teste, catalogo, rec = preparar(entrada)
    metodos = {"ordem_original": ordem_original, "regra": regra_explicita, "knn": rec.knn}

    linhas, top_rows = [], []
    for q in CONSULTAS:
        cand = filtrar(catalogo, q["obrigatorio"])
        linha = {"id": q["id"], "candidatos": len(cand),
                 "n_obrigatorios": len(q["obrigatorio"]), "n_preferencias": len(q["preferencias"])}
        for nome, fn in metodos.items():
            top = fn(cand, q)
            m = avaliar(top, q)
            linha.update({f"aderencia_{nome}": m["aderencia"], f"todas_{nome}": m["todas_preferencias"],
                          f"obrigatorios_{nome}": m["obrigatorios_ok"], f"retornados_{nome}": len(top)})
            for pos, (_, r) in enumerate(top.iterrows(), 1):
                top_rows.append({"consulta": q["id"], "metodo": nome, "posicao": pos,
                                 "linha_origem": int(r["linha_origem"]),
                                 **{c: r[c] for c in CAMPOS},
                                 "preferencias_atendidas": int(atendidas(r.to_frame().T, q["preferencias"])[0]),
                                 "similaridade": round(float(r["similaridade"]), 4) if "similaridade" in r else None})
        linhas.append(linha)
    por_consulta = pd.DataFrame(linhas)
    validas = por_consulta[por_consulta["candidatos"] > 0]

    agregado = {}
    for nome in metodos:
        agregado[nome] = {
            "aderencia_media": float(validas[f"aderencia_{nome}"].mean()),
            "todas_preferencias_media": float(validas[f"todas_{nome}"].mean()),
            "obrigatorios_respeitados": float(validas[f"obrigatorios_{nome}"].mean()),
        }
    resultados = {
        "titulo": "TED 03 - Experimento B: recuperação e ordenação por similaridade",
        "seed": SEED, "top_k": TOP_K,
        "pesos": {"categorico": PESO_CATEGORICO, "texto": PESO_TEXTO},
        "campos": CAMPOS, "campos_excluidos": ["AdoptionSpeed", "indicadores auxiliares de qualidade"],
        "base": {"registros": len(df), "colunas_originais": 21},
        "divisao": {"estrategia": "GroupShuffleSplit 80/20 por grupo de descrição normalizada",
                    "ajuste": len(ajuste), "catalogo_teste": len(teste),
                    "catalogo_sem_duplicatas_exibidas": len(catalogo),
                    "grupos_compartilhados": len(set(ajuste["grupo"]) & set(teste["grupo"]))},
        "cenarios": {"definidos": len(CONSULTAS), "com_candidatos": int(len(validas)),
                     "sem_candidatos": int((por_consulta["candidatos"] == 0).sum())},
        "metricas": agregado,
        "empates_regra_knn": int((validas["aderencia_regra"] == validas["aderencia_knn"]).sum()),
        "alerta": ("Métricas operacionais calculadas sobre os mesmos campos usados para filtrar e ordenar; "
                   "não medem relevância percebida, compatibilidade ou sucesso de adoção."),
        "bibliotecas": {"python": platform.python_version(), "scikit-learn": sklearn.__version__,
                        "pandas": pd.__version__, "numpy": np.__version__},
    }

    saida.mkdir(parents=True, exist_ok=True)
    (saida / "consultas_avaliacao.json").write_text(json.dumps(CONSULTAS, ensure_ascii=False, indent=2), encoding="utf-8")
    (saida / "resultados.json").write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    por_consulta.round(4).to_csv(saida / "resultados_por_consulta.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(top_rows).to_csv(saida / "top5_resultados.csv", index=False, encoding="utf-8-sig")
    figuras(por_consulta, agregado, saida / "figures")
    return resultados, por_consulta


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, default=ROOT / "data/processed/petfinder_mini_tratado.csv")
    ap.add_argument("--out", type=Path, default=ROOT / "reports/TED03_recomendacao")
    a = ap.parse_args()
    res, por = executar(a.input, a.out)
    pd.set_option("display.width", 160)
    print(json.dumps({k: res[k] for k in ("divisao", "cenarios", "metricas", "empates_regra_knn")},
                     ensure_ascii=False, indent=2))
    print(por[["id", "candidatos", "aderencia_ordem_original", "aderencia_regra", "aderencia_knn", "todas_knn"]]
          .round(3).to_string(index=False))


if __name__ == "__main__":
    main()
