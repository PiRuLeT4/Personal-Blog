import os
import json

DATA_DIR = 'blog_data'
USERS_FILE = 'USERS.json'

def load_all_posts():
    posts = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(DATA_DIR, filename), 'r') as f:
                posts.append(json.load(f))
    return sorted(posts, key=lambda x: x['date'])

def load_post(post_id):
    try:
        with open(os.path.join(DATA_DIR, f'{post_id}.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_post(data):
    with open(os.path.join(DATA_DIR, f"{data['id']}.json"), 'w') as f:
        json.dump(data, f, indent=4)

def delete_post(post_id):
    os.remove(os.path.join(DATA_DIR, f"{post_id}.json"))

def edit_post(id, data):
    with open(os.path.join(DATA_DIR, f"{data['id']}.json"), 'w') as f:
        pass

def add_post(data):
    new_id = next_id()
    data['id'] = new_id
    save_post(data)
    return new_id

def next_id():
    existing = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            name = filename[:-5]  # quit .json
            if name.isdigit():
                existing.append(int(name))
    if not existing:
        return 1
    return max(existing) + 1

def save_user(username, password):
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    if username in users:
        return False #.. username alredy exists
    
    users[username] = password
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
    
    return True #.. user successfully saved

            

def validate_user(username, password):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
        return username in users and users[username] == password
    