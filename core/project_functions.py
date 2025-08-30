from core.utils import load_json, save_json
from core.user_functions import add_notification

def get_all_projects():
    return load_json('projects.json')

def get_project_by_id(proj_id):
    projects = load_json('projects.json')
    for proj in projects:
        if proj['id'] == proj_id:
            return proj
    return None

def get_projects_by_owner(owner_id):
    projects = load_json('projects.json')
    return [p for p in projects if p['owner'] == owner_id]

def add_project(owner_id, title, desc, skills, timeline):
    projects = load_json('projects.json')
    new_id = max([p['id'] for p in projects], default=0) + 1
    proj = {
        "id": new_id,
        "title": title,
        "desc": desc,
        "required_skills": skills,
        "timeline": timeline,
        "owner": owner_id,
        "participants": [owner_id],
        "join_requests": []
    }
    projects.append(proj)
    save_json('projects.json', projects)

    users = load_json('users.json')
    for u in users:
        if u['id'] == owner_id:
            u.setdefault('projects_posted', [])
            u['projects_posted'].append(new_id)
            break
    save_json('users.json', users)
    return proj


def edit_project(proj_id, title, desc, skills, timeline, tasks=None):
    projects = load_json('projects.json')
    for proj in projects:
        if proj['id'] == proj_id:
            proj['title'] = title
            proj['desc'] = desc
            proj['required_skills'] = skills
            proj['timeline'] = timeline
            if tasks is not None:
                proj['tasks'] = tasks
            break
    save_json('projects.json', projects)


# def edit_project(proj_id, title, desc, skills, timeline):
#     projects = load_json('projects.json')
#     for proj in projects:
#         if proj['id'] == proj_id:
#             proj['title'] = title
#             proj['desc'] = desc
#             proj['required_skills'] = skills
#             proj['timeline'] = timeline
#             break
#     save_json('projects.json', projects)

def send_join_request(user_id, proj_id):
    projects = load_json('projects.json')
    for proj in projects:
        if proj['id'] == proj_id:
            if user_id not in proj.get('join_requests', []) and user_id not in proj.get('participants', []):
                proj.setdefault('join_requests', []).append(user_id)
                add_notification(proj['owner'], f"User {user_id} requested to join your project '{proj['title']}'")
            break
    save_json('projects.json', projects)

# def handle_join_request(owner_id, proj_id, requester_id, accept):
#     projects = load_json('projects.json')
#     for proj in projects:
#         if proj['id'] == proj_id and proj['owner'] == owner_id:
#             if requester_id in proj.get('join_requests', []):
#                 proj['join_requests'].remove(requester_id)
#                 if accept:
#                     proj.setdefault('participants', []).append(requester_id)
#                     add_notification(requester_id, f"Your join request for project '{proj['title']}' was accepted!")
#                 else:
#                     add_notification(requester_id, f"Your join request for project '{proj['title']}' was rejected.")
#             break
#     save_json('projects.json', projects)

def handle_join_request(owner_id, proj_id, requester_id, accept):
    projects = load_json('projects.json')
    users = load_json('users.json')
    for proj in projects:
        if proj['id'] == proj_id and proj['owner'] == owner_id:
            if requester_id in proj.get('join_requests', []):
                proj['join_requests'].remove(requester_id)
                if accept:
                    if requester_id not in proj.get('participants', []):
                        proj['participants'].append(requester_id)
                    for user in users:
                        if user['id'] == requester_id:
                            user.setdefault('joined_projects', [])
                            if proj_id not in user['joined_projects']:
                                user['joined_projects'].append(proj_id)
                            break
                    add_notification(requester_id, f"Your join request for project '{proj['title']}' was accepted!")
                else:
                    add_notification(requester_id, f"Your join request for project '{proj['title']}' was rejected.")
            break
    save_json('projects.json', projects)
    save_json('users.json', users)
