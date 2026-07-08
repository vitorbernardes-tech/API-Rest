from sqlite3 import connect
import sqlite3
from typing import Any

from flask import Flask, jsonify, request

app = Flask(__name__)

treinos = [
    {'id': 1,
      'grupo_muscular': 'Costas',
      'carga_kg': 20,
      'exercicio': 'Remada Curvada'
    },

    {'id': 2,
      'grupo_muscular': 'Ombro',
      'carga_kg': 5,
      'exercicio': 'Desenvolvimento'
    },

    {'id': 3,
      'grupo_muscular': 'Perna',
      'carga_kg': 40,
      'exercicio': 'Agachamento'    
    },
]

refeicoes = [
    {'id': 1,
      'calorias estimadas': 200,
      'alimento': 'Ovos mexidos',
      'quantidade de gramas': 2
    },

    {'id': 2,
      'calorias estimadas': 300,
      'alimento': 'Frango grelhado',
      'quantidade de gramas': 150
    },

    {'id': 3,
      'calorias estimadas': 400,
      'alimento': 'Salmão assado',
      'quantidade de gramas': 200    
    },
]

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

    cursor.execute("INSERT INTO treinos (grupo_muscular, carga_kg, exercicio)  VALUES (?, ?, ?)",
                   (data['grupo_muscular'], data['carga_kg'], data['exercicio']))
    
    conn.commit()
    conn.close()

    return jsonify({'message': 'Treino criado com sucesso'}), 201

@app.route('/treino/<int:id>', methods=['GET'])
def ver_treino_por_id(id):
    for treino in treinos:
        if treino['id'] == id:
            return jsonify(treino)
    return jsonify({'message': 'Treino não encontrado'}), 404

@app.route('/treino/<int:id>', methods=['PUT'])
def trocar_treino(id):
    treino_trocado = request.get_json()
    for nome, treino in enumerate(treinos):
        if treino['id'] == id:
            treinos[nome].update(treino_trocado)
            return jsonify(treinos[nome])
    return jsonify({'message': 'Treino não encontrado'}), 404

@app.route('/treino', methods=['POST'])
def criar_treino():
    data = request.get_json()
    data['id'] = len(treinos) + 1
    treinos.append(data)
    return jsonify(data), 201

@app.route('/treino/<int:id>', methods=['DELETE'])
def excluir_treino(id):
    for nome, treino in enumerate(treinos):
        if treino['id'] == id:
            del treinos[nome]
            return jsonify({'message': 'Treino excluído com sucesso'})
    return jsonify({'message': 'Treino não encontrado'}), 404

@app.route('/refeicao', methods=['GET'])
def ver_refeicao():
    return jsonify(refeicoes)

@app.route('/refeicao/<int:id>', methods=['GET'])
def ver_refeicao_por_id(id):
    for refeicao in refeicoes:
        if refeicao['id'] == id:
            return jsonify(refeicao)
    return jsonify({'message': 'Refeição não encontrada'}), 404

@app.route('/refeicao/<int:id>', methods=['PUT'])
def trocar_refeicao(id):    
    refeicao_trocada = request.get_json()
    for nome, refeicao in enumerate(refeicoes):
        if refeicao['id'] == id:
            refeicoes[nome].update(refeicao_trocada)
            return jsonify(refeicoes[nome])
    return jsonify({'message': 'Refeição não encontrada'}), 404

@app.route('/refeicao', methods=['POST'])
def criar_refeicao():   
    data = request.get_json()
    if data.get('quantidade de gramas', 0) <= 0:
        return jsonify({'message': 'A quantidade de gramas deve ser um valor positivo'}), 400

    data['id'] = len(refeicoes) + 1
    refeicoes.append(data)
    return jsonify(data), 201
        
@app.route('/refeicao/<int:id>', methods=['DELETE'])
def excluir_refeicao(id):       
    for nome, refeicao in enumerate(refeicoes):
        if refeicao['id'] == id:
            del refeicoes[nome]
            return jsonify({'message': 'Refeição excluída com sucesso'})
    return jsonify({'message': 'Refeição não encontrada'}), 404 

def init_db():
    conn = sqlite3.connect('treinos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo_muscular TEXT NOT NULL,
            carga_kg REAL NOT NULL,
            exercicio TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(port=5000, host='localhost', debug=True)
