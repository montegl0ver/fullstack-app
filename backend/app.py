import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Railway автоматически подставит DATABASE_URL при подключении Postgres
db_url = os.getenv('DATABASE_URL', "sqlite:///test.db")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title} for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    if not data or 'title' not in data:
        return jsonify({"error": "No title"}), 400
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"id": new_task.id, "title": new_task.title}), 201

if __name__ == '__main__':
    # Порт 5000 стандартный, но Railway может назначить свой через переменную PORT
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
