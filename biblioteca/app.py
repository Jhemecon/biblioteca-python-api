from flask import Flask, jsonify, request
from models import Livro, Usuario

app = Flask(__name__)

livros = []
usuarios = []


@app.route('/livros', methods=['POST'])
def cadastrar_livro():

    dados = request.json

    livro = Livro(
        dados['titulo'],
        dados['autor'],
        dados['isbn']
    )

    livros.append(livro)

    return jsonify({
        "mensagem": "Livro cadastrado!"
    })


@app.route('/livros', methods=['GET'])
def listar_livros():

    lista = []

    for livro in livros:
        lista.append(livro.to_dict())

    return jsonify(lista)


@app.route('/usuarios', methods=['POST'])
def cadastrar_usuario():

    dados = request.json

    usuario = Usuario(
        dados['nome'],
        dados['id_usuario']
    )

    usuarios.append(usuario)

    return jsonify({
        "mensagem": "Usuário cadastrado!"
    })


@app.route('/emprestimos', methods=['POST'])
def emprestar_livro():

    dados = request.json

    isbn = dados['isbn']
    id_usuario = dados['id_usuario']

    livro_encontrado = None
    usuario_encontrado = None

    for livro in livros:
        if livro.isbn == isbn:
            livro_encontrado = livro

    for usuario in usuarios:
        if usuario.id_usuario == id_usuario:
            usuario_encontrado = usuario

    if livro_encontrado is None:
        return jsonify({
            "erro": "Livro não encontrado"
        }), 404

    if usuario_encontrado is None:
        return jsonify({
            "erro": "Usuário não encontrado"
        }), 404

    if usuario_encontrado.pegar_emprestado(livro_encontrado):

        return jsonify({
            "mensagem": "Empréstimo realizado!"
        })

    return jsonify({
        "erro": "Livro indisponível"
    }), 400


if __name__ == '__main__':
    app.run(debug=True)
