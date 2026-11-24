Nome: Eduardo Guedes Amorim
R.A: 191075
Prof: Vitor Vieira
link: https://github.com/Edudu1147/Techflow-tasks

# TechFlow Tasks

Sistema web de gerenciamento de tarefas desenvolvido para a **TechFlow Solutions**
(empresa fictícia) a pedido de uma startup de logística.

## Objetivo
Permitir acompanhar o fluxo de trabalho em tempo real, priorizar tarefas críticas
e monitorar o desempenho da equipe.

## Escopo inicial (v1.0)
- Cadastrar, listar, editar e excluir tarefas (CRUD).
- Cada tarefa possui título, descrição e status (`A Fazer`, `Em Progresso`, `Concluído`).
- Interface web simples e API REST.

## Metodologia
Abordagem **híbrida Scrum + Kanban**: sprints curtas para planejar o incremento e
quadro Kanban (GitHub Projects) para visualizar o fluxo.

## Mudança de escopo (v1.1)

**O que mudou:** após a primeira demonstração, o cliente informou que a equipe perdia
tempo decidindo o que fazer primeiro e que a gerência não tinha visibilidade do desempenho.
Foram adicionados:

1. **Prioridade** nas tarefas (`Baixa`, `Média`, `Alta`, `Crítica`) com filtro por prioridade.
2. **Painel de métricas** (`GET /api/metricas`) com total de tarefas, tarefas por status e
   prioridade, críticas em aberto e taxa de conclusão.

**Justificativa:** são os dois requisitos centrais do contrato ("priorizar tarefas críticas"
e "monitorar o desempenho da equipe") e entregam valor imediato ao cliente. Em um processo
ágil, mudanças como essa são bem-vindas: entram no backlog (novos cards no Kanban), são
estimadas e implementadas na sprint seguinte, sem refazer o que já funciona.

**Como foi gerenciada:** criados os cards 10 e 11 no quadro, commits `feat:` separados,
migração automática da tabela SQLite (coluna nova com valor padrão `Média`) e novos testes
que mantêm a CI verde.

## Como executar

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
PYTHONPATH=src python -m techflow.app               # Windows (PowerShell): $env:PYTHONPATH="src"; python -m techflow.app
```
Acesse http://127.0.0.1:5000. Para rodar os testes e o lint: `pytest` e `flake8 src tests`.

## Estrutura
```
src/techflow/   código (app, repositório, validação, template)
tests/          testes automatizados (pytest)
docs/           Kanban, diagramas UML e captura de tela
.github/workflows/ci.yml   pipeline de integração contínua
```

## API
| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/tarefas?prioridade=Crítica` | lista (filtro opcional) |
| POST | `/api/tarefas` | cria |
| GET/PUT/DELETE | `/api/tarefas/<id>` | consulta, atualiza, exclui |
| GET | `/api/metricas` | indicadores de desempenho |
