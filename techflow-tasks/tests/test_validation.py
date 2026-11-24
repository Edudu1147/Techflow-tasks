import pytest

from techflow.validation import ValidationError, validar_tarefa


def test_tarefa_valida_recebe_valores_padrao():
    r = validar_tarefa({"titulo": "  Criar login  "})
    assert r == {"titulo": "Criar login", "descricao": "", "status": "A Fazer",
                 "prioridade": "Média"}


def test_titulo_obrigatorio():
    with pytest.raises(ValidationError):
        validar_tarefa({"titulo": "   "})


def test_titulo_muito_longo():
    with pytest.raises(ValidationError):
        validar_tarefa({"titulo": "x" * 101})


def test_status_invalido():
    with pytest.raises(ValidationError):
        validar_tarefa({"titulo": "a", "status": "Pausado"})


def test_atualizacao_parcial_aceita_campos_ausentes():
    assert validar_tarefa({"status": "Concluído"}, parcial=True) == {"status": "Concluído"}


def test_corpo_nao_objeto():
    with pytest.raises(ValidationError):
        validar_tarefa(["x"])


def test_prioridade_valida():
    assert validar_tarefa({"titulo": "a", "prioridade": "Crítica"})["prioridade"] == "Crítica"


def test_prioridade_invalida():
    with pytest.raises(ValidationError):
        validar_tarefa({"titulo": "a", "prioridade": "Urgentíssima"})
