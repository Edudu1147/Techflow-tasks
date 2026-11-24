"""Aplicação Flask: API REST e interface web."""
import os

from flask import Flask, jsonify, render_template, request

from .repository import TaskRepository
from .validation import ValidationError, validar_tarefa


def create_app(db_path=None):
    """Fábrica da aplicação (facilita testes com banco temporário)."""
    app = Flask(__name__)
    repo = TaskRepository(db_path or os.environ.get("TECHFLOW_DB", "techflow.db"))

    @app.errorhandler(ValidationError)
    def erro_validacao(e):
        return jsonify(erro=str(e)), 400

    def nao_encontrada():
        return jsonify(erro="Tarefa não encontrada."), 404

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/tarefas")
    def listar():
        return jsonify(repo.listar(request.args.get("prioridade")))

    @app.get("/api/metricas")
    def metricas():
        return jsonify(repo.metricas())

    @app.post("/api/tarefas")
    def criar():
        dados = validar_tarefa(request.get_json(silent=True))
        return jsonify(repo.criar(dados)), 201

    @app.get("/api/tarefas/<int:id_>")
    def obter(id_):
        tarefa = repo.obter(id_)
        return jsonify(tarefa) if tarefa else nao_encontrada()

    @app.put("/api/tarefas/<int:id_>")
    def atualizar(id_):
        dados = validar_tarefa(request.get_json(silent=True), parcial=True)
        tarefa = repo.atualizar(id_, dados)
        return jsonify(tarefa) if tarefa else nao_encontrada()

    @app.delete("/api/tarefas/<int:id_>")
    def excluir(id_):
        if repo.excluir(id_):
            return "", 204
        return nao_encontrada()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
