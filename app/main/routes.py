
from flask import render_template, request, redirect, url_for, flash, current_app
from sqlalchemy.exc import IntegrityError
from app import db
from app.main import bp
from app.models import Tarefa, Categoria

@bp.route('/', methods=['GET', 'POST'])
def index():
    editando_id = request.args.get('editar', type=int)
    
    if request.method == 'POST':
        return processar_formulario()
    
    tarefas = Tarefa.query.order_by(Tarefa.data_criacao.desc()).all()
    categorias = Categoria.query.all()
    tarefa_editando = Tarefa.query.get(editando_id) if editando_id else None
    stats = Tarefa.contar_por_status()
    
    return render_template('main/index.html',
                           tarefas=tarefas,
                           categorias=categorias,
                           tarefa_editando=tarefa_editando,
                           stats=stats)

def processar_formulario():
    id_tarefa = request.form.get('editando_id', type=int)
    descricao = request.form.get('descricao', '').strip()
    prioridade = request.form.get('prioridade', 'media')
    categoria_id = request.form.get('categoria_id', type=int)

    if not descricao:
        flash('Descrição obrigatória!', 'error')
        return redirect(url_for('main.index'))

    if id_tarefa:
        tarefa = Tarefa.query.get_or_404(id_tarefa)
        tarefa.descricao = descricao
        tarefa.prioridade = prioridade
        tarefa.categoria_id = categoria_id
        msg = 'Tarefa atualizada!'
    else:
        tarefa = Tarefa(descricao=descricao, prioridade=prioridade, categoria_id=categoria_id)
        db.session.add(tarefa)
        msg = 'Tarefa adicionada!'

    try:
        db.session.commit()
        flash(msg, 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Erro: tarefa já existe!', 'error')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao salvar tarefa!', 'error')
        current_app.logger.error(e)

    return redirect(url_for('main.index'))

@bp.route('/excluir/<int:id>')
def excluir(id):
    tarefa = Tarefa.query.get_or_404(id)
    try:
        db.session.delete(tarefa)
        db.session.commit()
        flash('Tarefa excluída!', 'success')
    except:
        db.session.rollback()
        flash('Erro ao excluir tarefa!', 'error')
    return redirect(url_for('main.index'))