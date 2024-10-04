import sqlite3
import json

import models

def create_database():
    # Connexion à la base de données SQLite (ou création de la base si elle n'existe pas)
    conn = sqlite3.connect('taskisy.db')
    cursor = conn.cursor()
    
    # Création des tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER,
        name TEXT NOT NULL
    );
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        id_project INTEGER,
        id_user INTEGER,
        done BOOLEAN NOT NULL,
        FOREIGN KEY (id_project) REFERENCES projects (id)
    );
    ''')
    
    return conn, cursor

def insert_project_and_tasks(cursor, project_name, tasks, id_user):
    # Insertion du projet
    cursor.execute('''
    INSERT INTO projects (id_user, name) VALUES (?, ?)
    ''', (id_user, project_name))
    
    # Récupérer l'ID du projet nouvellement inséré
    project_id = cursor.lastrowid
    
    # Insertion des tâches
    for task in tasks:
        cursor.execute('''
        INSERT INTO tasks (title, id_project, id_user, done) VALUES (?, ?, ?, ?)
        ''', (task.title, project_id, id_user, task.done))

'''
#lire le fichier JSON
data = json.load(open('result.json'))

project_name = data['project']
id_user = 1
tasks = [models.responseModel.TaskModel(title=task['title'], done=task['done']) for task in data['tasks']]

conn, cursor = create_database()
insert_project_and_tasks(cursor, project_name, tasks, id_user)

# Commit et fermeture de la connexion
conn.commit()
conn.close()
print("Database created and data inserted successfully.")
'''

#récuperer une tâche de la base de données
def get_task_by_id(id_task):
    conn = sqlite3.connect('taskisy.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT title, done FROM tasks WHERE id = ?
    ''', (id_task,))
    
    task = cursor.fetchone()
    
    conn.close()
    
    return task

#récuperer toutes les tâches de la base de données
def get_all_tasks():
    conn = sqlite3.connect('taskisy.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT title, done FROM tasks
    ''')
    
    tasks = cursor.fetchall()
    
    conn.close()
    
    return tasks


#récuperer toutes les tâches d'un projet de la base de données
def get_tasks_by_project(project_id):
    conn = sqlite3.connect('taskisy.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT title, done FROM tasks WHERE id_project = ?
    ''', (project_id,))
    
    tasks = cursor.fetchall()
    
    conn.close()
    
    return tasks

#récuperer tous les projets de la base de données
def get_all_projects():
    conn = sqlite3.connect('taskisy.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, name FROM projects
    ''')
    
    projects = cursor.fetchall()
    
    conn.close()
    
    return projects

#récuperer un projet de la base de données
def get_project_by_id(id_project):
    conn = sqlite3.connect('taskisy.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT name FROM projects WHERE id = ?
    ''', (id_project,))
    
    project = cursor.fetchone()
    
    conn.close()
    
    return project


'''
all_tasks = get_all_tasks()
print("All tasks:")
for task in all_tasks:
    print(task)
'''