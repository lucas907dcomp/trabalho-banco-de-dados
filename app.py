from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


# Função para conectar ao banco de dados
def conectar():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="lucas123",
            port="5432"
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


# Rota para inserir um usuário
@app.route('/usuario', methods=['POST'])
def inserir_usuario():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        dados = request.json
        nome = dados.get('nome')
        email = dados.get('email')
        data_nascimento = dados.get('data_nascimento')

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO usuario (nome, email, data_nascimento) 
                VALUES (%s, %s, %s)
            """, (nome, email, data_nascimento))
            conn.commit()

        return jsonify({'mensagem': 'Usuário inserido com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao inserir usuário: {e}'}), 500
    finally:
        conn.close()


# Rota para consultar todos os usuários
@app.route('/usuarios', methods=['GET'])
def consultar_usuarios():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuario")
            usuarios = cur.fetchall()
            return jsonify(usuarios)
    except Exception as e:
        return jsonify({'erro': f'Erro ao consultar usuários: {e}'}), 500
    finally:
        conn.close()


# Rota para atualizar um usuário
@app.route('/usuario/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        dados = request.json
        nome = dados.get('nome')
        email = dados.get('email')
        data_nascimento = dados.get('data_nascimento')

        with conn.cursor() as cur:
            cur.execute("""
                UPDATE usuario 
                SET nome = %s, email = %s, data_nascimento = %s 
                WHERE id = %s
            """, (nome, email, data_nascimento, id))
            conn.commit()

        return jsonify({'mensagem': 'Usuário atualizado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar usuário: {e}'}), 500
    finally:
        conn.close()


# Rota para deletar um usuário
@app.route('/usuario/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuario WHERE id = %s", (id,))
            conn.commit()

        return jsonify({'mensagem': 'Usuário deletado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao deletar usuário: {e}'}), 500
    finally:
        conn.close()

# Rota para inserir um autor
@app.route('/autor', methods=['POST'])
def inserir_autor():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        dados = request.json
        nome = dados.get('nome')
        data_nascimento = dados.get('data_nascimento')
        nacionalidade = dados.get('nacionalidade')

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO autor (nome, data_nascimento, nacionalidade) 
                VALUES (%s, %s, %s)
            """, (nome, data_nascimento, nacionalidade))
            conn.commit()

        return jsonify({'mensagem': 'Autor inserido com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao inserir autor: {e}'}), 500
    finally:
        conn.close()

# Rota para consultar todos os autores
@app.route('/autores', methods=['GET'])
def consultar_autores():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM autor")
            autores = cur.fetchall()
            return jsonify(autores)
    except Exception as e:
        return jsonify({'erro': f'Erro ao consultar autores: {e}'}), 500
    finally:
        conn.close()

@app.route('/autor/<int:id>', methods=['PUT'])
def atualizar_autor(id):
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        dados = request.json
        nome = dados.get('nome')
        data_nascimento = dados.get('data_nascimento')
        nacionalidade = dados.get('nacionalidade')


        if not data_nascimento or not nacionalidade:
            return jsonify({'erro': 'Os campos data_nascimento e nacionalidade são obrigatórios!'}), 400

        with conn.cursor() as cur:
            cur.execute("""
                UPDATE autor 
                SET nome = %s, data_nascimento = %s, nacionalidade = %s 
                WHERE id_autor = %s
            """, (nome, data_nascimento, nacionalidade, id))
            conn.commit()

        return jsonify({'mensagem': 'Autor atualizado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar autor: {e}'}), 500
    finally:
        conn.close()

# Rota para deletar um autor
@app.route('/autor/<int:id>', methods=['DELETE'])
def deletar_autor(id):
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM autor WHERE id_autor = %s", (id,))
            conn.commit()

        return jsonify({'mensagem': 'Autor deletado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao deletar autor: {e}'}), 500
    finally:
        conn.close()

# Rota para inserir um livro
@app.route('/livro', methods=['POST'])
def inserir_livro():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        dados = request.json
        titulo = dados.get('titulo')
        ano_publicacao = dados.get('ano_publicacao')
        id_editora = dados.get('id_editora')
        id_categoria = dados.get('id_categoria')

        numero_exemplares = dados.get('numero_exemplares', 0)

        with conn.cursor() as cur:
            cur.execute(""" 
                INSERT INTO livro (titulo, ano_publicacao, id_editora, id_categoria, numero_exemplares) 
                VALUES (%s, %s, %s, %s, %s)
            """, (titulo, ano_publicacao, id_editora, id_categoria, numero_exemplares))
            conn.commit()

        return jsonify({'mensagem': 'Livro inserido com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao inserir livro: {e}'}), 500
    finally:
        conn.close()


# Rota para atualizar um livro
@app.route('/livro/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        dados = request.json
        titulo = dados.get('titulo')
        ano_publicacao = dados.get('ano_publicacao')
        id_editora = dados.get('id_editora')
        id_categoria = dados.get('id_categoria')
        numero_exemplares = dados.get('numero_exemplares')

        with conn.cursor() as cur:

            cur.execute("SELECT * FROM livro WHERE id_livro = %s", (id,))
            livro = cur.fetchone()

            if not livro:
                return jsonify({'erro': 'Livro não encontrado'}), 404


            if titulo is not None:
                cur.execute("UPDATE livro SET titulo = %s WHERE id_livro = %s", (titulo, id))
            if ano_publicacao is not None:
                cur.execute("UPDATE livro SET ano_publicacao = %s WHERE id_livro = %s", (ano_publicacao, id))
            if id_editora is not None:
                cur.execute("UPDATE livro SET id_editora = %s WHERE id_livro = %s", (id_editora, id))
            if id_categoria is not None:
                cur.execute("UPDATE livro SET id_categoria = %s WHERE id_livro = %s", (id_categoria, id))
            if numero_exemplares is not None:
                cur.execute("UPDATE livro SET numero_exemplares = %s WHERE id_livro = %s", (numero_exemplares, id))

            conn.commit()

        return jsonify({'mensagem': 'Livro atualizado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar livro: {e}'}), 500
    finally:
        conn.close()



@app.route('/livros', methods=['GET'])
def consultar_livros():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM livro")
            livros = cur.fetchall()
            return jsonify(livros)
    except Exception as e:
        return jsonify({'erro': f'Erro ao consultar livros: {e}'}), 500
    finally:
        conn.close()


@app.route('/livro/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM livro WHERE id_livro = %s", (id,))
            conn.commit()

        return jsonify({'mensagem': 'Livro deletado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao deletar livro: {e}'}), 500
    finally:
        conn.close()


@app.route('/autor_livro', methods=['POST'])
def adicionar_autor_livro():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        dados = request.json
        id_autor = dados.get('id_autor')
        id_livro = dados.get('id_livro')

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO autor_livro (id_autor, id_livro) 
                VALUES (%s, %s)
            """, (id_autor, id_livro))
            conn.commit()

        return jsonify({'mensagem': 'Relação entre autor e livro adicionada com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao adicionar relação: {e}'}), 500
    finally:
        conn.close()


# Rota para consultar todas as relações autor-livro
@app.route('/autor_livros', methods=['GET'])
def consultar_autor_livros():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM autor_livro")
            autor_livros = cur.fetchall()
            return jsonify(autor_livros)
    except Exception as e:
        return jsonify({'erro': f'Erro ao consultar relações: {e}'}), 500
    finally:
        conn.close()


# Rota para atualizar uma relação entre autor e livro
@app.route('/autor_livro', methods=['PUT'])
def atualizar_autor_livro():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        dados = request.json
        id_autor = dados.get('id_autor')
        id_livro = dados.get('id_livro')

        if not id_autor or not id_livro:
            return jsonify({'erro': 'id_autor e id_livro são obrigatórios!'}), 400

        with conn.cursor() as cur:
            cur.execute("""
                UPDATE autor_livro 
                SET id_autor = %s, id_livro = %s
                WHERE id_autor = %s AND id_livro = %s
            """, (id_autor, id_livro, id_autor, id_livro))
            conn.commit()

        return jsonify({'mensagem': 'Relação entre autor e livro atualizada com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar relação: {e}'}), 500
    finally:
        conn.close()


# Rota para deletar uma relação entre autor e livro
@app.route('/autor_livro', methods=['DELETE'])
def deletar_autor_livro():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        dados = request.json
        id_autor = dados.get('id_autor')
        id_livro = dados.get('id_livro')

        if not id_autor or not id_livro:
            return jsonify({'erro': 'id_autor e id_livro são obrigatórios!'}), 400

        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM autor_livro 
                WHERE id_autor = %s AND id_livro = %s
            """, (id_autor, id_livro))
            conn.commit()

        return jsonify({'mensagem': 'Relação entre autor e livro deletada com sucesso!'})
    except Exception as e:
        return jsonify({'erro': f'Erro ao deletar relação: {e}'}), 500
    finally:
        conn.close()

# Rota para efetuar uma transação (consultar e atualizar)
@app.route('/transacao_autor/<int:id>', methods=['PUT'])
def transacao_autor(id):
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM autor WHERE id_autor = %s", (id,))
            autor = cur.fetchone()

            if not autor:
                return jsonify({'erro': 'Autor não encontrado'}), 404


            novo_nome = request.json.get('novo_nome')
            if not novo_nome:
                return jsonify({'erro': 'Novo nome é obrigatório'}), 400


            cur.execute("""
                UPDATE autor 
                SET nome = %s 
                WHERE id_autor = %s
            """, (novo_nome, id))
            conn.commit()

        return jsonify({'mensagem': 'Autor atualizado com sucesso!', 'autor': {'id_autor': id, 'novo_nome': novo_nome}})
    except Exception as e:
        return jsonify({'erro': f'Erro na transação: {e}'}), 500
    finally:
        conn.close()


@app.route('/emprestimo', methods=['POST'])
def realizar_emprestimo():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        dados = request.json
        id_livro = dados.get('id_livro')
        id_usuario = dados.get('id_usuario')


        with conn.cursor() as cur:
            cur.execute("SELECT numero_exemplares FROM livro WHERE id_livro = %s", (id_livro,))
            livro = cur.fetchone()

            if not livro:
                return jsonify({'erro': 'Livro não encontrado'}), 404

            numero_exemplares = livro[0]
            if numero_exemplares <= 0:
                return jsonify({'erro': 'Livro não disponível para empréstimo'}), 400


            cur.execute("INSERT INTO emprestimo (id_livro, id_usuario, data_emprestimo) VALUES (%s, %s, CURRENT_DATE)",
                        (id_livro, id_usuario))

            cur.execute("UPDATE livro SET numero_exemplares = numero_exemplares - 1 WHERE id_livro = %s", (id_livro,))
            conn.commit()

        return jsonify({'mensagem': 'Empréstimo realizado com sucesso!'})

    except Exception as e:
        return jsonify({'erro': f'Erro ao realizar o empréstimo: {e}'}), 500
    finally:
        conn.close()


@app.route('/emprestimos', methods=['GET'])
def consultar_emprestimos():
    conn = conectar()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar ao banco de dados'}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    e.id_emprestimo,
                    e.data_emprestimo,
                    e.data_devolucao,
                    e.id_usuario,
                    e.id_livro,
                    e.status,
                    l.titulo AS livro_titulo,
                    u.nome AS usuario_nome
                FROM emprestimo e
                LEFT JOIN livro l ON e.id_livro = l.id_livro
                LEFT JOIN usuario u ON e.id_usuario = u.id  -- Corrigido para id
            """)
            emprestimos = cur.fetchall()

            lista_emprestimos = []
            for emp in emprestimos:
                lista_emprestimos.append({
                    'id_emprestimo': emp[0],
                    'data_emprestimo': emp[1],
                    'data_devolucao': emp[2],
                    'id_usuario': emp[3],
                    'id_livro': emp[4],
                    'status': emp[5],
                    'livro_titulo': emp[6],
                    'usuario_nome': emp[7]
                })

            return jsonify(lista_emprestimos)

    except Exception as e:
        return jsonify({'erro': f'Erro ao consultar empréstimos: {e}'}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
