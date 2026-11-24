import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Circle

fig, ax = plt.subplots(figsize=(11, 7.5))
ax.set_xlim(0, 11); ax.set_ylim(0, 7.5); ax.axis("off")
ax.add_patch(Rectangle((2.6, 0.3), 6.6, 6.9, fill=False, lw=1.5))
ax.text(5.9, 6.9, "Sistema TechFlow Tasks", ha="center", fontsize=13, weight="bold")

def actor(x, y, nome):
    ax.add_patch(Circle((x, y + 0.9), 0.2, fill=False, lw=1.5))
    ax.plot([x, x], [y + 0.7, y + 0.1], "k", lw=1.5)
    ax.plot([x - 0.35, x + 0.35], [y + 0.55, y + 0.55], "k", lw=1.5)
    ax.plot([x, x - 0.3], [y + 0.1, y - 0.4], "k", lw=1.5)
    ax.plot([x, x + 0.3], [y + 0.1, y - 0.4], "k", lw=1.5)
    ax.text(x, y - 1.05, nome, ha="center", fontsize=11, weight="bold")

casos = {
 "criar": (4.6, 6.0, "Criar tarefa"),
 "validar": (7.6, 6.0, "Validar dados"),
 "quadro": (4.6, 4.9, "Visualizar quadro Kanban"),
 "mover": (4.6, 3.8, "Mover tarefa de status"),
 "editar": (4.6, 2.7, "Editar tarefa"),
 "excluir": (4.6, 1.6, "Excluir tarefa"),
 "filtrar": (7.6, 3.8, "Filtrar por prioridade *"),
 "prio": (7.6, 2.7, "Definir prioridade *"),
 "metricas": (7.6, 1.2, "Consultar métricas\nde desempenho *"),
}
for k, (x, y, t) in casos.items():
    ax.add_patch(Ellipse((x, y), 2.4, 0.8, fill=True, fc="#EAF1FF", ec="k", lw=1.2))
    ax.text(x, y, t, ha="center", va="center", fontsize=9.5)

actor(1.2, 3.6, "Membro da\nEquipe")
actor(10.0, 2.4, "Gestor")

def link(a, b, **kw):
    ax.plot([a[0], b[0]], [a[1], b[1]], "k", lw=1, **kw)

for k in ["criar", "quadro", "mover", "editar", "excluir"]:
    x, y, _ = casos[k]; link((1.6, 4.1), (x - 1.2, y))
for k in ["filtrar", "prio", "metricas"]:
    x, y, _ = casos[k]; link((9.6, 3.0), (x + 1.2, y))

ax.annotate("", xy=(6.4, 6.0), xytext=(5.8, 6.0), arrowprops=dict(arrowstyle="->", ls="--"))
ax.text(6.1, 6.2, "«include»", ha="center", fontsize=8.5)
ax.text(5.9, 0.45, "* funcionalidades adicionadas na mudança de escopo (v1.1)", ha="center", fontsize=9, style="italic")
plt.savefig("diagrama_casos_de_uso.png", dpi=150, bbox_inches="tight")
