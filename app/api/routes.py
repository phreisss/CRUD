from flask import request, jsonify, current_app
from sqlalchemy.exc import IntegrityError
from app import db
from app.api import bp
from app.models import Tarefa, Categoria

@bp.route('/tarefas', methods=['GET'])
def get_tarefas():
    """API: Listar todas as tarefas"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    busca = request.args.get('busca', '')
    
    query = Tarefa.query
    
    if busca:
        query = query.filter(Tarefa.descricao.contains(busca))
    
    tarefas = query.order_by(Tarefa.data_criacao.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'tarefas': [tarefa.to_dict() for tarefa in tarefas.items],
        'total': tarefas.total,
        'pages': tarefas.pages,
        'page': page,
        'per_page': per_page
    })

@bp.route('/tarefas/<int:id>', methods=['GET'])
def get_tarefa(id):
    """API: Obter uma tarefa específica"""
    tarefa = Tarefa.query.get_or_404(id)
    return jsonify(tarefa.to_dict())

@bp.route('/tarefas', methods=['POST'])
def create_tarefa():
    """API: Criar nova tarefa"""
    data = request.get_json() or {}
    
    if 'descricao' not in data or not data['descricao'].strip():
        return jsonify({'error': 'Descrição é obrigatória'}), 400
    
    try:
        tarefa = Tarefa(
            descricao=data['descricao'].strip(),
            prioridade=data.get('prioridade', 'media'),
            categoria_id=data.get('categoria_id')
        )
        db.session.add(tarefa)
        db.session.commit()
        
        return jsonify(tarefa.to_dict()), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Tarefa já existe'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro API criar tarefa: {e}')
        return jsonify({'error': 'Erro interno'}), 500

@bp.route('/tarefas/<int:id>', methods=['PUT'])
def update_tarefa(id):
    """API: Atualizar tarefa"""
    tarefa = Tarefa.query.get_or_404(id)
    data = request.get_json() or {}
    
    try:
        if 'descricao' in data:
            if not data['descricao'].strip():
                return jsonify({'error': 'Descrição não pode estar vazia'}), 400
            tarefa.descricao = data['descricao'].strip()
        
        if 'concluida' in data:
            tarefa.concluida = bool(data['concluida'])
        
        if 'prioridade' in data:
            tarefa.prioridade = data['prioridade']
        
        if 'categoria_id' in data:
            tarefa.categoria_id = data['categoria_id']
        
        db.session.commit()
        return jsonify(tarefa.to_dict())
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Descrição já existe'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro API atualizar tarefa: {e}')
        return jsonify({'error': 'Erro interno'}), 500

@bp.route('/tarefas/<int:id>', methods=['DELETE'])
def delete_tarefa(id):
    """API: Excluir tarefa"""
    tarefa = Tarefa.query.get_or_404(id)
    
    try:
        db.session.delete(tarefa)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro API excluir tarefa: {e}')
        return jsonify({'error': 'Erro interno'}), 500

@bp.route('/tarefas/stats', methods=['GET'])
def get_stats():
    """API: Estatísticas das tarefas"""
    return jsonify(Tarefa.contar_por_status())

@bp.route('/categorias', methods=['GET'])
def get_categorias():
    """API: Listar categorias"""
    categorias = Categoria.query.all()
    return jsonify([categoria.to_dict() for categoria in categorias])

@bp.route('/categorias', methods=['POST'])
def create_categoria():
    """API: Criar categoria"""
    data = request.get_json() or {}
    
    if 'nome' not in data or not data['nome'].strip():
        return jsonify({'error': 'Nome é obrigatório'}), 400
    
    try:
        categoria = Categoria(
            nome=data['nome'].strip(),
            cor=data.get('cor', '#007bff')
        )
        db.session.add(categoria)
        db.session.commit()
        
        return jsonify(categoria.to_dict()), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Categoria já existe'}), 400

@bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso não encontrado'}), 404

@bp.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Requisição inválida'}), 400