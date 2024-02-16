from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import random

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'mysql-qcm-service',  # Nom du service Kubernetes
    'port': 3306,  # Port spécifié dans la configuration du service
    'user': 'root',
    'password': '123456',
    'database': 'qcm',
}

def get_cursor():
    connection = mysql.connector.connect(**db_config)
    return connection.cursor(buffered=True), connection

# Helper function to fetch questions and correct answers from the database
def fetch_questions():
    cursor, connection = get_cursor()
    cursor.execute("SELECT question, option1, option2, option3, option4, correct_answer FROM quiz_questions LIMIT 3")
    #cursor.execute("SELECT question, option1, option2, option3, option4, correct_answer FROM quiz_questions ORDER BY RAND() LIMIT 2")
    rows = cursor.fetchall()
    questions = [{'question': row[0], 'options': row[1:5], 'correct_answer': row[5]} for row in rows]
    cursor.close()
    connection.close()
    return questions

def store_score_in_database(user_id, score):
    data = request.json
    cursor, connection = get_cursor()
    cursor.execute("INSERT INTO resultat (username, score) VALUES (%s, %s)", (user_id, score))
    connection.commit()
    cursor.close()
    connection.close()

# Route to add a new question
@app.route('/add_question', methods=['POST'])
def add_question():
    data = request.get_json()
    question_data = (
        data.get('question', ''),
        data.get('option1', ''),
        data.get('option2', ''),
        data.get('option3', ''),
        data.get('option4', ''),
        data.get('correct_answer', '')
    )

    cursor, connection = get_cursor()
    cursor.execute("INSERT INTO quiz_questions (question, option1, option2, option3, option4, correct_answer) VALUES (%s, %s, %s, %s, %s, %s)", question_data)
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'Question ajoutée avec succès!'})


# Route to get all quiz questions
@app.route('/quiz', methods=['GET'])
def quiz():
    questions = fetch_questions()
    return jsonify({'questions': questions})

# Route to submit answers and get the score
@app.route('/submit', methods=['POST'])
def submit():
    user_data = request.get_json()
    user_id = user_data.get('user_id')
    user_answers = user_data.get('answers', [])

    questions_with_answers = fetch_questions()
    total_questions = len(questions_with_answers)

    correct_answers = 0

    for user_answer in user_answers:
        q_index = user_answer.get('questionIndex', None)
        a_index = user_answer.get('answerIndex', None)

        if (
            q_index is not None
            and 0 <= q_index < total_questions
            and a_index is not None
            and 0 <= a_index < len(questions_with_answers[q_index]['options'])
            and questions_with_answers[q_index]['options'][a_index] == questions_with_answers[q_index]['correct_answer']
        ):
            correct_answers += 1

    score = (correct_answers / total_questions) * 100

    # Store the score in the database
    store_score_in_database(user_id, score)
    return jsonify({'message': score})



# Route to list results by summing scores for each user
@app.route('/list_results', methods=['GET'])
def list_results():
    cursor, connection = get_cursor()

    cursor.execute("""
        SELECT users.id, users.username, COALESCE(SUM(resultat.score), 0) as total_score
        FROM users
        LEFT JOIN resultat ON users.id = resultat.username
        GROUP BY users.id, users.username
        ORDER BY total_score DESC
    """)

    rows = cursor.fetchall()
    results = [{'username': row[1], 'total_score': row[2]} for row in rows]

    cursor.close()
    connection.close()

    return jsonify({'results': results})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
