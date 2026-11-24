"""Validação de entradas de tarefas."""

STATUS_VALIDOS = ("A Fazer", "Em Progresso", "Concluído")
PRIORIDADES_VALIDAS = ("Baixa", "Média", "Alta", "Crítica")
TAMANHO_MAX_TITULO = 100


class ValidationError(ValueError):
    """Erro lançado quando os dados enviados são inválidos."""


def validar_tarefa(dados, parcial=False):
    """Valida e normaliza os dados de uma tarefa.

    Se ``parcial`` for True (atualização), campos ausentes são aceitos.
    Retorna um novo dicionário com os dados limpos.
    """
    if not isinstance(dados, dict):
        raise ValidationError("O corpo da requisição deve ser um objeto JSON.")

    limpo = {}

    if "titulo" in dados or not parcial:
        titulo = dados.get("titulo")
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValidationError("O título é obrigatório.")
        titulo = titulo.strip()
        if len(titulo) > TAMANHO_MAX_TITULO:
            raise ValidationError(
                f"O título deve ter no máximo {TAMANHO_MAX_TITULO} caracteres.")
        limpo["titulo"] = titulo

    if "descricao" in dados:
        descricao = dados["descricao"]
        if not isinstance(descricao, str):
            raise ValidationError("A descrição deve ser um texto.")
        limpo["descricao"] = descricao.strip()
    elif not parcial:
        limpo["descricao"] = ""

    if "status" in dados:
        if dados["status"] not in STATUS_VALIDOS:
            raise ValidationError(
                "Status inválido. Use: " + ", ".join(STATUS_VALIDOS) + ".")
        limpo["status"] = dados["status"]
    elif not parcial:
        limpo["status"] = STATUS_VALIDOS[0]

    if "prioridade" in dados:
        if dados["prioridade"] not in PRIORIDADES_VALIDAS:
            raise ValidationError(
                "Prioridade inválida. Use: " + ", ".join(PRIORIDADES_VALIDAS) + ".")
        limpo["prioridade"] = dados["prioridade"]
    elif not parcial:
        limpo["prioridade"] = "Média"

    return limpo
