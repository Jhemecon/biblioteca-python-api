class Livro:
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.__disponivel = True

    def esta_disponivel(self):
        return self.__disponivel

    def emprestar(self):
        if self.__disponivel:
            self.__disponivel = False
            return True
        return False

    def devolver(self):
        self.__disponivel = True

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "disponivel": self.esta_disponivel()
        }


class Usuario:
    def __init__(self, nome, id_usuario):
        self.nome = nome
        self.id_usuario = id_usuario
        self.livros_emprestados = []

    def pegar_emprestado(self, livro):
        if livro.emprestar():
            self.livros_emprestados.append(livro)
            return True
        return False

    def devolver_livro(self, livro):
        if livro in self.livros_emprestados:
            livro.devolver()
            self.livros_emprestados.remove(livro)
            return True
        return False


class ValidadorEmprestimo:
    def __init__(self, livros, usuarios):
        self.livros = livros
        self.usuarios = usuarios

    def validar_livro_e_usuario(self, isbn, id_usuario):
        livro_encontrado = self.livros.get(isbn)
        usuario_encontrado = self.usuarios.get(id_usuario)

        if not livro_encontrado:
            return None, None, {"erro": "Livro não encontrado"}, 404

        if not usuario_encontrado:
            return None, None, {"erro": "Usuário não encontrado"}, 404

        return livro_encontrado, usuario_encontrado, None, None