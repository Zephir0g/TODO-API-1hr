from flask import jsonify, render_template, request
from models import db, Task


def create_routes(app):

    @app.route('/')
    def index():
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks)

    # create task
    @app.route('/tasks', methods=['POST'])
    def create_task():
        data = request.get_json()

        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400

        is_done = data.get('is_done', False)
        new_task = Task(title=data['title'], is_done=is_done)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            'id': new_task.id,
            'title': new_task.title,
            'is_done': new_task.is_done
            }), 201

    # get tasks
    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = Task.query.all()
        tasks_list = [{
            'id': task.id,
            'title': task.title,
            'is_done': task.is_done
            } for task in tasks]

        return jsonify(tasks_list), 200

    # get task by id
    @app.route('/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        task = Task.query.get_or_404(task_id)

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify({
            'id': task.id,
            'title': task.title,
            'is_done': task.is_done
            }), 200

    # update task
    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        task = Task.query.get_or_404(task_id)

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        data = request.get_json()

        if 'title' in data:
            task.title = data['title']

        if 'is_done' in data:
            task.is_done = data['is_done']

        db.session.commit()

        return jsonify({
            'id': task.id,
            'title': task.title,
            'is_done': task.is_done
            }), 200

    # delete task
    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'}), 200
