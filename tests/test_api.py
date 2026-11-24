def test_criar_listar(client):
    r = client.post("/api/tarefas", json={"titulo": "Login"})
    assert r.status_code == 201
    assert r.get_json()["status"] == "A Fazer"
    assert len(client.get("/api/tarefas").get_json()) == 1


def test_criar_invalida(client):
    r = client.post("/api/tarefas", json={"titulo": ""})
    assert r.status_code == 400
    assert "erro" in r.get_json()


def test_corpo_ausente(client):
    assert client.post("/api/tarefas").status_code == 400


def test_atualizar_status(client):
    client.post("/api/tarefas", json={"titulo": "A"})
    r = client.put("/api/tarefas/1", json={"status": "Em Progresso"})
    assert r.get_json()["status"] == "Em Progresso"


def test_nao_encontrada(client):
    assert client.get("/api/tarefas/9").status_code == 404
    assert client.put("/api/tarefas/9", json={"status": "Concluído"}).status_code == 404
    assert client.delete("/api/tarefas/9").status_code == 404


def test_excluir(client):
    client.post("/api/tarefas", json={"titulo": "A"})
    assert client.delete("/api/tarefas/1").status_code == 204
    assert client.get("/api/tarefas").get_json() == []


def test_pagina_inicial(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "TechFlow Tasks" in r.get_data(as_text=True)


def test_prioridade_padrao_e_filtro(client):
    client.post("/api/tarefas", json={"titulo": "A"})
    client.post("/api/tarefas", json={"titulo": "B", "prioridade": "Crítica"})
    assert client.get("/api/tarefas/1").get_json()["prioridade"] == "Média"
    criticas = client.get("/api/tarefas?prioridade=Crítica").get_json()
    assert [t["titulo"] for t in criticas] == ["B"]


def test_prioridade_invalida_na_api(client):
    r = client.post("/api/tarefas", json={"titulo": "A", "prioridade": "X"})
    assert r.status_code == 400


def test_endpoint_metricas(client):
    client.post("/api/tarefas", json={"titulo": "A", "prioridade": "Crítica"})
    client.put("/api/tarefas/1", json={"status": "Concluído"})
    m = client.get("/api/metricas").get_json()
    assert m["total"] == 1
    assert m["taxa_conclusao"] == 100.0
