"""TED 04 - figura-síntese de Data Storytelling.

Lê os resultados já gerados nas TEDs 02 e 03 (reports/) e produz
reports/TED04/figures/01_sintese_resultados.png. Não treina modelos.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
a = json.loads((ROOT / "reports/TED03/resultados.json").read_text(encoding="utf-8"))
b = json.loads((ROOT / "reports/TED03_recomendacao/resultados.json").read_text(encoding="utf-8"))

DESTAQUE, CONTEXTO, TEXTO, GRADE = "#8A4F24", "#B9AFA6", "#2B2B2B", "#E6E1DC"

def pct(v):
    return v * 100 if v <= 1 else v

t = a["teste"]; m = b["metricas"]
painel_a = [("Linha de base\n(classe majoritária)", pct(t["baseline_maioria"]["f1_macro"]), False),
            ("Regressão Logística\n(teste)", pct(t["modelo_selecionado"]["f1_macro"]), True),
            ("Sem termos de espécie\n(sensibilidade)", pct(t["teste_com_termos_de_especie_ocultos"]["f1_macro"]), False)]
painel_b = [("Ordem original", pct(m["ordem_original"]["aderencia_media"]), False),
            ("Regra explícita", pct(m["regra"]["aderencia_media"]), True),
            ("k-NN + vetorização", pct(m["knn"]["aderencia_media"]), True)]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=200)
for ax, dados, titulo, rotulo in [
    (axes[0], painel_a, "A · Classificação da espécie pela descrição", "F1-score macro (%)"),
    (axes[1], painel_b, "B · Ordenação por preferências (top-5)", "Preferências atendidas (%)")]:
    nomes = [d[0] for d in dados]; vals = [d[1] for d in dados]
    cores = [DESTAQUE if d[2] else CONTEXTO for d in dados]
    barras = ax.bar(nomes, vals, color=cores, width=0.55, edgecolor="white", linewidth=2)
    for bar, v in zip(barras, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 2, f"{v:.2f}%".replace(".", ","),
                ha="center", va="bottom", fontsize=10, color=TEXTO, fontweight="bold")
    ax.set_ylim(0, 110); ax.set_title(titulo, loc="left", fontsize=11, color=TEXTO, fontweight="bold")
    ax.set_ylabel(rotulo, fontsize=9, color=TEXTO)
    ax.yaxis.grid(True, color=GRADE, linewidth=0.8); ax.set_axisbelow(True)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRADE)
    ax.tick_params(axis="x", labelsize=8.5, colors=TEXTO, length=0); ax.tick_params(axis="y", labelsize=8, colors="#6B6B6B", length=0)
plt.tight_layout()
destino = ROOT / "reports/TED04/figures/01_sintese_resultados.png"
destino.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(destino, facecolor="white")
print("Figura salva em", destino)
