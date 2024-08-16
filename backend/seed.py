from app import app, db
from models import User, Task, Tag, TaskTag

with app.app_context():
    db.create_all()

    # Create some users
    user1 = User(username='john_doe', email='john@example.com')
    user1.set_password('password123')
    user2 = User(username='jane_doe', email='jane@example.com')
    user2.set_password('password456')

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Create some tasks
    task1 = Task(title='Task 1', description='First task', user_id=user1.id)
    task2 = Task(title='Task 2', description='Second task', user_id=user1.id)
    task3 = Task(title='Task 3', description='Third task', user_id=user2.id)

    db.session.add(task1)
    db.session.add(task2)
    db.session.add(task3)
    db.session.commit()

    # Create some tags
    tag1 = Tag(name='Important')
    tag2 = Tag(name='Urgent')

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.commit()

    # Create relationships between tasks and tags
    task_tag1 = TaskTag(task_id=task1.id, tag_id=tag1.id)
    task_tag2 = TaskTag(task_id=task2.id, tag_id=tag2.id)

    db.session.add(task_tag1)
    db.session.add(task_tag2)
    db.session.commit()

    print("Database seeded!")
