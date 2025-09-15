import os
from app import create_app, db
from app.models import Tarefa, Categoria
from app.config import configuracoes

# Obter configuração do ambiente ou usar padrão
nome_config = os.environ.get('FLASK_CONFIG') or 'padrao'
app = create_app(configuracoes[nome_config])

@app.shell_context_processor
def contexto_shell():
    """Disponibilizar variáveis no shell do Flask"""
    return {
        'db': db, 
        'Tarefa': Tarefa, 
        'Categoria': Categoria
    }

@app.cli.command()
def inicializar_bd():
    """Inicializar o banco de dados"""
    db.create_all()
    print('Banco de dados inicializado!')

@app.cli.command()
def popular_bd():
    """Adicionar dados iniciais ao banco"""
    # Categorias
    if Categoria.query.count() == 0:
        categorias = [
            Categoria(nome='Pessoal', cor='#28a745'),
            Categoria(nome='Trabalho', cor='#007bff'),
            Categoria(nome='Estudos', cor='#ffc107'),
            Categoria(nome='Casa', cor='#dc3545')
        ]
        
        for categoria in categorias:
            db.session.add(categoria)
    
    # Tarefas de exemplo
    if Tarefa.query.count() == 0:
        tarefas_exemplo = [
            Tarefa(descricao='Estudar Flask', prioridade='alta', categoria_id=3),
            Tarefa(descricao='Fazer compras', prioridade='media', categoria_id=4),
            Tarefa(descricao='Reunião às 15h', prioridade='alta', categoria_id=2),
            Tarefa(descricao='Exercitar-se', prioridade='baixa', categoria_id=1)
        ]
        
        for tarefa in tarefas_exemplo:
            db.session.add(tarefa)
    
    db.session.commit()
    print('Dados iniciais adicionados!')

if __name__ == '__main__':
    app.run(debug=True)