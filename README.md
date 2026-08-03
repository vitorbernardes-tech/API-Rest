# Shape & Health Tracker API 🏋️‍♂️🥗

API RESTful desenvolvida para o gerenciamento de rotinas de treinos e controle nutricional de uma aplicação fictícia de saúde e bem-estar.

O objetivo principal deste projeto foi aplicar na prática conceitos fundamentais de desenvolvimento back-end, incluindo a estruturação de rotas HTTP, validação de dados em formato JSON, implementação de regras de negócio e persistência de informações em banco de dados relacional.

---

## 🚀 Funcionalidades e Regras de Negócio

### 🏋️ Gestão de Treinos
* Cadastro de exercícios, grupo muscular e carga (peso em kg).
* **Regra de validação:** A carga informada deve ser rigorosamente maior ou igual a 1 kg.

### 🥗 Gestão de Refeições
* Registro de refeições com nome e quantidade de alimentos (em gramas).
* **Regra de validação:** A quantidade em gramas não pode ser um valor negativo (deve ser maior ou igual a 0).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework Web:** Flask
* **Banco de Dados:** SQLite
* **Hospedagem / Deploy:** PythonAnywhere
* **Testes de API:** Postman


---

## Link para Acessar o API

(http://vitorbernardes.pythonanywhere.com/treino)
