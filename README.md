# 📚 Biblioteca Online — API REST em Python

> API REST para gerenciamento de uma biblioteca: cadastro de livros, usuários e controle de empréstimos e devoluções.

---

## 📋 Sobre o Projeto

Este projeto implementa uma **API REST para biblioteca online** utilizando **Flask** e conceitos de **Programação Orientada a Objetos**. A API permite cadastrar livros e usuários, além de gerenciar empréstimos e devoluções, controlando a disponibilidade de cada exemplar.

### 🎯 Objetivos

- Demonstrar a aplicação prática de **APIs REST** com Flask
- Implementar **Programação Orientada a Objetos** com encapsulamento
- Controlar o fluxo de **empréstimos e devoluções** com validações de negócio
- Organizar o projeto com separação entre **rotas** e **modelos**

---

## 🧱 Conceitos Aplicados

### Programação Orientada a Objetos

O projeto utiliza três classes principais com responsabilidades bem definidas:

- **`Livro`** — Representa um exemplar com controle de disponibilidade via atributo privado (`__disponivel`)
- **`Usuario`** — Representa um leitor com sua lista de livros emprestados
- **`ValidadorEmprestimo`** — Centraliza a validação de livro e usuário antes de operações de empréstimo ou devolução

### Encapsulamento

O atributo `__disponivel` da classe `Livro` é privado, acessado apenas através dos métodos `esta_disponivel()`, `emprestar()` e `devolver()`, garantindo integridade dos dados.

### API REST

As rotas seguem os princípios REST com uso adequado de métodos HTTP e códigos de status:

| Método | Rota | Descrição | Status |
|--------|------|-----------|--------|
| `POST` | `/livros` | Cadastrar livro | 201 / 400 |
| `GET` | `/livros` | Listar livros | 200 |
| `POST` | `/usuarios` | Cadastrar usuário | 201 / 400 |
| `POST` | `/emprestimos` | Realizar empréstimo | 200 / 400 / 404 |
| `POST` | `/devolver` | Devolver livro | 200 / 400 / 404 |

---

## 📁 Estrutura do Projeto

```
biblioteca-python-api/
│
├── README.md                  # Este arquivo
└── biblioteca/
    ├── app.py                 # Rotas e configuração Flask
    ├── models.py              # Classes Livro, Usuario e ValidadorEmprestimo
    └── teste.http             # Arquivo de testes das rotas
```

### Descrição dos Módulos

#### 🔹 `app.py`
Arquivo principal da aplicação que:
- Configura a aplicação Flask
- Define as rotas e métodos HTTP
- Utiliza o `ValidadorEmprestimo` para validar livro e usuário antes de cada operação
- Retorna respostas JSON com os códigos de status adequados

#### 🔹 `models.py`
Modelos de dados com Orientação a Objetos:
- `Livro(titulo, autor, isbn)` — Cria um livro com disponibilidade inicial `True`
- `livro.emprestar()` — Marca o livro como indisponível se estiver livre
- `livro.devolver()` — Marca o livro como disponível novamente
- `livro.to_dict()` — Serializa o objeto para JSON
- `Usuario(nome, id_usuario)` — Cria um usuário com lista de empréstimos vazia
- `usuario.pegar_emprestado(livro)` — Tenta realizar o empréstimo de um livro
- `usuario.devolver_livro(livro)` — Tenta devolver um livro previamente emprestado
- `ValidadorEmprestimo(livros, usuarios)` — Valida a existência de livro e usuário; utilizado pelas rotas `/emprestimos` e `/devolver`

#### 🔹 `teste.http`
Arquivo de testes HTTP para todas as rotas, utilizado com a extensão **REST Client** do VS Code. Os campos das requisições estão com aspas vazias `""` para serem preenchidos antes de executar.

---

## ⚙️ Instalação e Requisitos

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Dependências

O projeto utiliza apenas uma biblioteca externa:

```bash
flask
```

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/biblioteca-python-api.git
   cd biblioteca-python-api
   ```

2. **Instale as dependências:**
   ```bash
   pip install flask
   ```

---

## 🚀 Como Executar

1. Navegue até o diretório da aplicação:
   ```bash
   cd biblioteca
   ```

2. Execute o servidor Flask:
   ```bash
   python app.py
   ```

3. A API estará disponível em:
   ```
   http://127.0.0.1:5000
   ```

---

## 🧪 Como Testar com o REST Client (VS Code)

### Pré-requisito

Instale a extensão **REST Client** no VS Code:
1. Abra o VS Code
2. Vá em **Extensões** (`Ctrl+Shift+X`)
3. Pesquise por `REST Client` (autor: Huachao Mao)
4. Clique em **Install**

### Usando o arquivo `teste.http`

Com o servidor rodando, abra o arquivo `biblioteca/teste.http` no VS Code. Cada requisição está separada por `###` e possui campos com aspas vazias `""` para preencher antes de executar.

Preencha os valores desejados e clique em **Send Request** que aparece acima de cada bloco:

```http
### 1. Cadastrar um Livro
POST http://127.0.0.1:5000/livros
Content-Type: application/json

{
  "titulo": "O Senhor dos Anéis",
  "autor": "J.R.R. Tolkien",
  "isbn": "978-8533613379"
}
```

> ⚠️ **Importante:** Execute as requisições na ordem do arquivo. O empréstimo (passo 4) só funciona se o livro e o usuário já estiverem cadastrados.

### Ordem recomendada

1. **Cadastrar um Livro** — preencha `titulo`, `autor` e `isbn`
2. **Listar Livros** — confirme que o livro foi salvo
3. **Cadastrar um Usuário** — preencha `nome` e `id_usuario`
4. **Realizar Empréstimo** — use o mesmo `isbn` e `id_usuario` dos passos anteriores
5. **Tentar Emprestar de Novo** — sem alterar nada, execute novamente o passo 4 para ver o erro `400 - Livro Indisponível`
6. **Devolver Livro** — use o mesmo `isbn` e `id_usuario` do empréstimo
7. **Listar Livros Após Devolução** — confirme que o livro voltou a estar disponível

---

## 🧪 Exemplos de Uso

### 1. Cadastrar um Livro
```http
POST /livros
Content-Type: application/json

{
  "titulo": "O Senhor dos Anéis",
  "autor": "J.R.R. Tolkien",
  "isbn": "978-8533613379"
}
```
**Resposta:** `201 Created`
```json
{ "mensagem": "Livro cadastrado!" }
```

### 2. Listar Livros
```http
GET /livros
```
**Resposta:** `200 OK`
```json
[
  {
    "titulo": "O Senhor dos Anéis",
    "autor": "J.R.R. Tolkien",
    "isbn": "978-8533613379",
    "disponivel": true
  }
]
```

### 3. Cadastrar um Usuário
```http
POST /usuarios
Content-Type: application/json

{
  "nome": "João Silva",
  "id_usuario": "user-001"
}
```
**Resposta:** `201 Created`
```json
{ "mensagem": "Usuário cadastrado!" }
```

### 4. Realizar Empréstimo
```http
POST /emprestimos
Content-Type: application/json

{
  "isbn": "978-8533613379",
  "id_usuario": "user-001"
}
```
**Resposta:** `200 OK`
```json
{ "mensagem": "Empréstimo realizado!" }
```

### 5. Tentar Emprestar Livro Indisponível
```http
POST /emprestimos
Content-Type: application/json

{
  "isbn": "978-8533613379",
  "id_usuario": "user-002"
}
```
**Resposta:** `400 Bad Request`
```json
{ "erro": "Livro indisponível" }
```

### 6. Devolver Livro
```http
POST /devolver
Content-Type: application/json

{
  "isbn": "978-8533613379",
  "id_usuario": "user-001"
}
```
**Resposta:** `200 OK`
```json
{ "mensagem": "Livro devolvido com sucesso!" }
```

### 7. Tentar Devolver Livro Não Emprestado
```http
POST /devolver
Content-Type: application/json

{
  "isbn": "978-8533613379",
  "id_usuario": "user-001"
}
```
**Resposta:** `400 Bad Request`
```json
{ "erro": "Livro não foi emprestado por este usuário" }
```

---

## 💡 Casos de Teste Sugeridos

### Teste 1: Cadastro com dados incompletos
```
Enviar POST /livros sem o campo "isbn"
Resultado esperado: 400 Bad Request — "Dados incompletos"
```

### Teste 2: ISBN duplicado
```
Cadastrar o mesmo livro duas vezes
Resultado esperado: 400 Bad Request — "Livro já cadastrado"
```

### Teste 3: Empréstimo com livro inexistente
```
Enviar ISBN que não foi cadastrado
Resultado esperado: 404 Not Found — "Livro não encontrado"
```

### Teste 4: Livro indisponível
```
Emprestar o mesmo livro para dois usuários diferentes
Resultado esperado: 200 no primeiro, 400 no segundo
```

### Teste 5: Devolução bem-sucedida
```
Emprestar um livro e em seguida devolvê-lo
Resultado esperado: 200 em ambos; disponivel volta a ser true na listagem
```

### Teste 6: Devolução por usuário errado
```
Tentar devolver um livro que foi emprestado por outro usuário
Resultado esperado: 400 Bad Request — "Livro não foi emprestado por este usuário"
```

---

## 🔬 Detalhes de Implementação

### Armazenamento em Memória

Os dados são armazenados em dicionários Python (`livros` e `usuarios`) em tempo de execução. Ao reiniciar o servidor, os dados são perdidos. Isso mantém o projeto simples e focado nos conceitos principais.

### Validações

Antes de qualquer operação, a API verifica:
- **Campos obrigatórios** presentes no corpo da requisição
- **Duplicidade** de ISBN e ID de usuário no cadastro
- **Existência** do livro e do usuário antes do empréstimo ou devolução
- **Disponibilidade** do livro antes de concluir o empréstimo
- **Vínculo** entre usuário e livro antes de concluir a devolução

### Validador Centralizado

A classe `ValidadorEmprestimo` recebe as referências dos dicionários `livros` e `usuarios` no momento da instanciação e expõe o método `validar_livro_e_usuario(isbn, id_usuario)`. Esse método é reutilizado pelas rotas `/emprestimos` e `/devolver`, evitando duplicação de lógica.

### Serialização

O método `to_dict()` da classe `Livro` converte o objeto para um dicionário Python, permitindo que o Flask o serialize como JSON via `jsonify()`.

---

## 📄 Licença

Este projeto é de código aberto e está disponível para fins educacionais.

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela no repositório!**

</div>