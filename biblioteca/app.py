from flask import Flask, jsonify, request
from models import Livro, Usuario, ValidadorEmprestimo

app = Flask(__name__)

livros = {}
usuarios = {}
validador = ValidadorEmprestimo(livros, usuarios)

@app.route('/')
def index():
    return "API da Biblioteca Online funcionando!"
    
@app.route('/livros', methods=['POST'])
def cadastrar_livro():
    dados = request.json
    
    campos_obrigatorios = ['titulo', 'autor', 'isbn']
    if not dados or not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Dados incompletos. Informe titulo, autor e isbn."}), 400

    isbn = dados['isbn']
    if isbn in livros:
        return jsonify({"erro": "Livro já cadastrado"}), 400

    livro = Livro(dados['titulo'], dados['autor'], isbn)
    livros[isbn] = livro

    return jsonify({"mensagem": "Livro cadastrado!"}), 201

@app.route('/livros', methods=['GET'])
def listar_livros():
    lista = [livro.to_dict() for livro in livros.values()]
    return jsonify(lista)

@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    dados = request.json
    
    if not dados or 'nome' not in dados or 'id_usuario' not in dados:
        return jsonify({"erro": "Nome e id_usuario são obrigatórios"}), 400

    id_usuario = dados['id_usuario']
    if id_usuario in usuarios:
        return jsonify({"erro": "Usuário já existe"}), 400

    usuario = Usuario(dados['nome'], id_usuario)
    usuarios[id_usuario] = usuario

    return jsonify({"mensagem": "Usuário cadastrado!"}), 201

@app.route('/emprestimos', methods=['POST'])
def emprestar_livro():
    dados = request.json
    
    livro_encontrado, usuario_encontrado, erro, status = validador.validar_livro_e_usuario(
        dados.get('isbn'), 
        dados.get('id_usuario')
    )
    
    if erro:
        return jsonify(erro), status

    if usuario_encontrado.pegar_emprestado(livro_encontrado):
        return jsonify({"mensagem": "Empréstimo realizado!"}), 200

    return jsonify({"erro": "Livro indisponível"}), 400

@app.route('/devolver', methods=['POST'])
def devolver_livro():
    dados = request.json
    
    livro_encontrado, usuario_encontrado, erro, status = validador.validar_livro_e_usuario(
        dados.get('isbn'), 
        dados.get('id_usuario')
    )
    
    if erro:
        return jsonify(erro), status

    if usuario_encontrado.devolver_livro(livro_encontrado):
        return jsonify({"mensagem": "Livro devolvido com sucesso!"}), 200

    return jsonify({"erro": "Livro não foi emprestado por este usuário"}), 400

if __name__ == '__main__':
    app.run(debug=True)