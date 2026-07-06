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
def ver_treino():
    return jsonify(treinos)

@app.route('/treino/<int:id>', methods=['GET'])
def ver_treino_por_id(id):
    for treino in treinos:
        if treino['id'] == id:
            return jsonify(treino)

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

if __name__ == '__main__':
    app.run(port=5000, host='localhost/treino', debug=True)