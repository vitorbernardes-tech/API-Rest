from sqlite3 import connect
import sqlite3
from typing import Any

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/treino', methods=['GET'])
def ver_treinos_do_banco():
    conn = sqlite3.connect('treinos.db')

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    grupo_muscular = request.args.get('grupo_muscular')
    
    if grupo_muscular: 
        cursor.execute("SELECT * FROM treinos WHERE grupo_muscular = ?", (grupo_muscular,))
    else:
        cursor.execute("SELECT * FROM treinos")

    treinos_db = cursor.fetchall()
    conn.close()

    lista_de_treinos = [dict(linha) for linha in treinos_db]
    return jsonify(lista_de_treinos)

@app.route('/treino', methods=['POST'])
def criar_treino_no_banco():
    data = request.get_json()

    conn = sqlite3.connect('treinos.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO treinos (grupo_muscular, carga_kg, exercicio) VALUES (?, ?, ?)",
                   (data['grupo_muscular'], data['carga_kg'], data['exercicio']))
 
    conn.commit()
    conn.close()

    return jsonify({'message': 'Treino criado com sucesso no banco de dados'}), 201

@app.route('/treino/<int:id>', methods=['GET'])
def ver_treino_por_id(id):
    conn = sqlite3.connect('treinos.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM treinos WHERE id = ?", (id,))
    treino_db = cursor.fetchone()
    conn.close()

    if treino_db:
        return jsonify(dict(treino_db))
    return jsonify({'message': 'Treino não encontrado'}), 404

@app.route('/treino/<int:id>', methods=['PUT'])
def trocar_treino(id):
    treino_trocado = request.get_json()
    conn = sqlite3.connect('treinos.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE treinos SET grupo_muscular = ?, carga_kg = ?, exercicio = ? WHERE id = ?",
                   (treino_trocado['grupo_muscular'], treino_trocado['carga_kg'], treino_trocado['exercicio'], id))
    conn.commit()
    linhas_afetadas = cursor.rowcount
    conn.close()

    if linhas_afetadas == 0:
        return jsonify({'message': 'Treino não encontrado'}), 404

    return jsonify({'message': 'Treino atualizado com sucesso no banco de dados'})

@app.route('/treino/<int:id>', methods=['DELETE'])
def excluir_treino_no_banco(id):
    conn = sqlite3.connect('treinos.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM treinos WHERE id = ?", (id,))

    conn.commit()
    linhas_afetadas = cursor.rowcount
    conn.close()

    if linhas_afetadas == 0:
        return jsonify({'message': 'Treino não encontrado'}), 404

    return jsonify({'message': 'Treino excluído com sucesso do banco de dados'})

@app.route('/refeicao', methods=['GET'])
def ver_refeicao_do_banco():
    conn = sqlite3.connect('treinos.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM refeicoes")
    refeicoes_db = cursor.fetchall()
    conn.close()

    lista_de_refeicoes = [dict(linha) for linha in refeicoes_db]
    return jsonify(lista_de_refeicoes)

@app.route('/refeicao/<int:id>', methods=['GET'])
def ver_refeicao_por_id(id):
    conn = sqlite3.connect('treinos.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM refeicoes WHERE id = ?", (id,))
    refeicao_db = cursor.fetchone()
    conn.close()

    if refeicao_db:
        return jsonify(dict(refeicao_db))
    return jsonify({'message': 'Refeição não encontrada'}), 404

@app.route('/refeicao/<int:id>', methods=['PUT'])
def trocar_refeicao(id):    
    refeicao_trocada = request.get_json()
    conn = sqlite3.connect('treinos.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE refeicoes SET nome = ?, quantidade_de_gramas = ? WHERE id = ?",
                   (refeicao_trocada['nome'], refeicao_trocada['quantidade_de_gramas'], id))
    conn.commit()
    linhas_afetadas = cursor.rowcount
    conn.close()

    if linhas_afetadas == 0:
        return jsonify({'message': 'Refeição não encontrada'}), 404

    return jsonify({'message': 'Refeição atualizada com sucesso no banco de dados'})

@app.route('/refeicao', methods=['POST'])
def criar_refeicao_no_banco():   
    data = request.get_json()

    if data.get('quantidade_de_gramas', 0) <= 0:
        return jsonify({'message': 'A quantidade de gramas deve ser um valor positivo'}), 400

    conn = sqlite3.connect('treinos.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO refeicoes (nome, quantidade_de_gramas) VALUES (?, ?)",
                   (data['nome'], data['quantidade_de_gramas']))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Refeição criada com sucesso no banco de dados'}), 201
        
@app.route('/refeicao/<int:id>', methods=['DELETE'])
def excluir_refeicao_no_banco(id):       
    conn = sqlite3.connect('treinos.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM refeicoes WHERE id = ?", (id,))
    conn.commit()
    linhas_afetadas = cursor.rowcount
    conn.close()

    if linhas_afetadas == 0:
        return jsonify({'message': 'Refeição não encontrada'}), 404

    return jsonify({'message': 'Refeição excluída com sucesso do banco de dados'})

def init_db():
    conn = sqlite3.connect('treinos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo_muscular TEXT,
            carga_kg REAL,
            exercicio TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS refeicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade_de_gramas REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(port=5000, host='localhost', debug=True)
