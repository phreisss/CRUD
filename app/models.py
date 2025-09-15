from datetime import datetime
from app import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    cor = db.Column(db.String(7), default='#007bff')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    tarefas = db.relationship('Tarefa', back_populates='categoria', lazy='dynamic')

    def to_dict(self):
        return {'id': self.id, 'nome': self.nome, 'cor': self.cor, 'total_tarefas': self.tarefas.count()}

class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False, unique=True, index=True)
    concluida = db.Column(db.Boolean, default=False, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    prioridade = db.Column(db.String(10), default='media')
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    categoria = db.relationship('Categoria', back_populates='tarefas')

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'concluida': self.concluida,
            'prioridade': self.prioridade,
            'categoria': self.categoria.nome if self.categoria else None,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }

    @staticmethod
    def contar_por_status():
        total = Tarefa.query.count()
        concluidas = Tarefa.query.filter_by(concluida=True).count()
        return {'total': total, 'concluidas': concluidas, 'pendentes': total - concluidas}