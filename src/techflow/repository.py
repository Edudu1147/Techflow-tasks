"""Persistência das tarefas em SQLite."""
import sqlite3


class TaskRepository:
    """Operações CRUD sobre a tabela de tarefas."""

    def __init__(self, caminho):
        self.caminho = caminho
        self._criar_tabela()

    def _conectar(self):
        conn = sqlite3.connect(self.caminho)
        conn.row_factory = sqlite3.Row
        return conn

    def _criar_tabela(self):
        with self._conectar() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'A Fazer'
                )""")
            # Migração (mudança de escopo v1.1): adiciona a coluna de prioridade
            colunas = [c["name"] for c in conn.execute("PRAGMA table_info(tarefas)")]
            if "prioridade" not in colunas:
                conn.execute(
                    "ALTER TABLE tarefas ADD COLUMN prioridade TEXT NOT NULL DEFAULT 'Média'")

    def criar(self, dados):
        """Insere uma tarefa e retorna o registro criado."""
        with self._conectar() as conn:
            cur = conn.execute(
                "INSERT INTO tarefas (titulo, descricao, status, prioridade) VALUES (?, ?, ?, ?)",
                (dados["titulo"], dados["descricao"], dados["status"], dados["prioridade"]))
            return self._obter(conn, cur.lastrowid)

    def listar(self, prioridade=None):
        """Retorna as tarefas ordenadas por id, opcionalmente filtradas por prioridade."""
        with self._conectar() as conn:
            if prioridade:
                linhas = conn.execute(
                    "SELECT * FROM tarefas WHERE prioridade = ? ORDER BY id",
                    (prioridade,)).fetchall()
            else:
                linhas = conn.execute("SELECT * FROM tarefas ORDER BY id").fetchall()
            return [dict(linha) for linha in linhas]

    def obter(self, id_):
        """Retorna uma tarefa ou None se não existir."""
        with self._conectar() as conn:
            return self._obter(conn, id_)

    @staticmethod
    def _obter(conn, id_):
        linha = conn.execute("SELECT * FROM tarefas WHERE id = ?", (id_,)).fetchone()
        return dict(linha) if linha else None

    def atualizar(self, id_, dados):
        """Atualiza os campos informados. Retorna a tarefa ou None."""
        if not dados:
            return self.obter(id_)
        colunas = ", ".join(f"{c} = ?" for c in dados)
        with self._conectar() as conn:
            conn.execute(f"UPDATE tarefas SET {colunas} WHERE id = ?",
                         (*dados.values(), id_))
            return self._obter(conn, id_)

    def excluir(self, id_):
        """Remove a tarefa. Retorna True se algo foi removido."""
        with self._conectar() as conn:
            return conn.execute("DELETE FROM tarefas WHERE id = ?", (id_,)).rowcount > 0

    def metricas(self):
        """Calcula indicadores de desempenho da equipe."""
        tarefas = self.listar()
        total = len(tarefas)
        por_status = {}
        por_prioridade = {}
        for t in tarefas:
            por_status[t["status"]] = por_status.get(t["status"], 0) + 1
            por_prioridade[t["prioridade"]] = por_prioridade.get(t["prioridade"], 0) + 1
        concluidas = por_status.get("Concluído", 0)
        criticas_abertas = sum(
            1 for t in tarefas if t["prioridade"] == "Crítica" and t["status"] != "Concluído")
        return {
            "total": total,
            "por_status": por_status,
            "por_prioridade": por_prioridade,
            "criticas_abertas": criticas_abertas,
            "taxa_conclusao": round(100 * concluidas / total, 1) if total else 0.0,
        }
