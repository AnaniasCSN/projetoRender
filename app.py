from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Inicialização da aplicação Flask
app = Flask(__name__)

# CONFIGURAÇÃO DO BANCO DE DADOS
# Usaremos SQLite, um banco relacional consistente que salva tudo em um arquivo local
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'tarefas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização da extensão SQLAlchemy
db = SQLAlchemy(app)

# MODELO DE DADOS (Representa a Tabela no Banco de Dados)
class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    
    id = db.Column(db.Integer, primary_key=True)         # Chave Primária Autoincrement
    descricao = db.Column(db.String(100), nullable=False) # Texto obrigatório até 100 caracteres
    concluida = db.Column(db.Boolean, default=False)     # Status de conclusão

    # Converte o objeto do banco para um dicionário JSON legível
    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'concluida': self.concluida
        }

# CRIAR AS TABELAS AUTOMATICAMENTE NO BANCO
with app.app_context():
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    db.create_all()

# ROTAS DA APLICAÇÃO WEB

@app.route('/')
def index():
    return render_template('index.html')

# API GET: Buscar todas as tarefas persistidas
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Consulta SQL equivalente: SELECT * FROM tarefas ORDER BY id DESC;
    todas_tarefas = Tarefa.query.order_by(Tarefa.id.desc()).all()
    return jsonify([t.to_dict() for t in todas_tarefas])

# API POST: Inserir nova tarefa no Banco de Dados
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    
    if not data or 'task' not in data or not data['task'].strip():
        return jsonify({'error': 'Descrição inválida'}), 400
    
    # Criar um novo objeto da classe Tarefa
    nova_tarefa = Tarefa(descricao=data['task'].strip())
    
    # Gravar no Banco de Dados (Transação)
    db.session.add(nova_tarefa)
    db.session.commit() # Confirma as alterações no arquivo físico
    
    return jsonify({'message': 'Tarefa salva com sucesso!', 'task': nova_tarefa.to_dict()}), 201

# API DELETE: Remover uma tarefa persistida pelo ID
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Consulta SQL equivalente: SELECT * FROM tarefas WHERE id = task_id;
    tarefa = Tarefa.query.get(task_id)
    
    if not tarefa:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
        
    db.session.delete(tarefa)
    db.session.commit() # Confirma a remoção no arquivo
    
    return jsonify({'message': 'Tarefa removida do banco de dados'}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)