from flask import Flask, jsonify, request
from models import Livro, Usuario

app = Flask(__name__)

livros = {}
usuarios = {}

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
    
    isbn = dados.get('isbn')
    id_usuario = dados.get('id_usuario')

    livro_encontrado = livros.get(isbn)
    usuario_encontrado = usuarios.get(id_usuario)

    if not livro_encontrado:
        return jsonify({"erro": "Livro não encontrado"}), 404

    if not usuario_encontrado:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    if usuario_encontrado.pegar_emprestado(livro_encontrado):
        return jsonify({"mensagem": "Empréstimo realizado!"}), 200

    return jsonify({"erro": "Livro indisponível"}), 400

if __name__ == '__main__':
    app.run(debug=True)
