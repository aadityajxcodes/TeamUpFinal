from core.utils import load_json, save_json

def get_user_by_username(username):
    users = load_json('users.json')
    for user in users:
        if user['username'] == username:
            return user
    return None

def get_user_by_id(user_id):
    users = load_json('users.json')
    for user in users:
        if user['id'] == user_id:
            return user
    return None

def register_user(username, password, full_name, skills, contact, bio):
    users = load_json('users.json')
    if any(u['username'] == username for u in users):
        return None  # Username taken

    new_id = max([u["id"] for u in users], default=0) + 1
    user = {
        "id": new_id,
        "username": username,
        "password": password,  # TODO: add hashing for production
        "full_name": full_name,
        "skills": skills,
        "contact": contact,
        "bio": bio,
        "projects_posted": [],
        "notifications": []
    }
    users.append(user)
    save_json('users.json', users)
    return user

def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user and user['password'] == password:
        return user
    return None

def add_notification(user_id, message):
    users = load_json('users.json')
    for user in users:
        if user['id'] == user_id:
            user.setdefault('notifications', [])
            user['notifications'].append({"message": message, "read": False})
            break
    save_json('users.json', users)

def mark_notifications_read(user_id):
    users = load_json('users.json')
    for user in users:
        if user['id'] == user_id:
            for note in user.get('notifications', []):
                note['read'] = True
            break
    save_json('users.json', users)
