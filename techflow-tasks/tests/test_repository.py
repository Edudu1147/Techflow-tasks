import pytest

from techflow.repository import TaskRepository


@pytest.fixture
def repo(tmp_path):
    return TaskRepository(str(tmp_path / "teste.db"))


def nova(titulo="Tarefa", prioridade="Média", status="A Fazer"):
    return {"titulo": titulo, "descricao": "", "status": status, "prioridade": prioridade}


def test_criar_e_obter(repo):
    t = repo.criar(nova("A"))
    assert t["id"] == 1
    assert repo.obter(1)["titulo"] == "A"


def test_listar_em_ordem(repo):
    repo.criar(nova("A"))
    repo.criar(nova("B"))
    assert [t["titulo"] for t in repo.listar()] == ["A", "B"]


def test_atualizar(repo):
    repo.criar(nova())
    t = repo.atualizar(1, {"status": "Concluído"})
    assert t["status"] == "Concluído"


def test_atualizar_inexistente(repo):
    assert repo.atualizar(99, {"status": "Concluído"}) is None


def test_excluir(repo):
    repo.criar(nova())
    assert repo.excluir(1) is True
    assert repo.excluir(1) is False
    assert repo.obter(1) is None


def test_filtrar_por_prioridade(repo):
    repo.criar(nova("A", "Baixa"))
    repo.criar(nova("B", "Crítica"))
    assert [t["titulo"] for t in repo.listar("Crítica")] == ["B"]


def test_metricas(repo):
    repo.criar(nova("A", "Crítica"))
    repo.criar(nova("B", "Crítica", "Concluído"))
    repo.criar(nova("C", "Baixa", "Em Progresso"))
    repo.criar(nova("D", "Alta", "Concluído"))
    m = repo.metricas()
    assert m["total"] == 4
    assert m["criticas_abertas"] == 1
    assert m["taxa_conclusao"] == 50.0
    assert m["por_status"]["Concluído"] == 2
    assert m["por_prioridade"]["Crítica"] == 2


def test_metricas_sem_tarefas(repo):
    assert repo.metricas()["taxa_conclusao"] == 0.0


def test_migracao_banco_antigo(tmp_path):
    import sqlite3
    caminho = str(tmp_path / "antigo.db")
    conn = sqlite3.connect(caminho)
    conn.execute("""CREATE TABLE tarefas (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL, descricao TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'A Fazer')""")
    conn.execute("INSERT INTO tarefas (titulo) VALUES ('legada')")
    conn.commit()
    conn.close()
    assert TaskRepository(caminho).obter(1)["prioridade"] == "Média"
