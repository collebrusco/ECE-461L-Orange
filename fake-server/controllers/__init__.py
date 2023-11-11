import time

class Controller:
    def __init__(self):
        self._users = {}
        self._projects = {}
        self._resources = {
            "HW Set 1": {
                "availability": 100,
                "capacity": 100,
            },
            "HW Set 2": {
                "availability": 100,
                "capacity": 100,
            },
            "HW Set 3": {
                "availability": 100,
                "capacity": 100,
            }
        }

    def register(self, username, password):
        if username in self._users:
            return
        self._users[username] = {
            "password": password,
            "created_at": time.time()
        }
        return username

    def login(self, username, password):
        if username not in self._users:
            return
        if self._users[username]["password"] != password:
            return
        return username

    def get_profile(self, username):
        if username not in self._users:
            return
        user = self._users[username]
        return {
            "username": username,
            "created_at": user["created_at"]
        }

    def create_project(self, title, description, creator):
        if title in self._projects or \
            not description or \
            creator not in self._users:
            return
        self._projects[title] = {
            "description": description,
            "creator": creator,
            "users": set([creator]),
            "resources": {"HW Set 1": 0, "HW Set 2": 0, "HW Set 3": 0},
        }
        return {
            **self._projects[title],
            "users": [creator]
        }

    def get_user_projects(self, username):
        if username not in self._users:
            return
        projects = []
        for title, project in self._projects.items():
            if username not in project["users"]:
                continue
            projects.append({
                "title": title,
                **project,
                "users": list(project["users"])
            })
        return projects

    def join_project(self, project_title, username):
        if username not in self._users or \
            username in self._projects[project_title]["users"]:
            return False
        self._projects[project_title]["users"].add(username)
        return True

    def get_resources(self):
        resources = []
        for title, resource in self._resources.items():
            resources.append({
                "title": title,
                **resource
            })
        return resources

    def checkout(self, resource_title, project_title, username, amount):
        if resource_title not in self._resources or \
            project_title not in self._projects or \
            username not in self._users:
            return False
        resource = self._resources[resource_title]
        project = self._projects[project_title]
        if username not in project["users"] or \
            resource["availability"] < amount:
            return False

        resource["availability"] -= amount
        project["resources"][resource_title] += amount
        return True

    def checkin(self, resource_title, project_title, username, amount):
        if resource_title not in self._resources or \
            project_title not in self._projects or \
            username not in self._users:
            return False
        resource = self._resources[resource_title]
        project = self._projects[project_title]
        if username not in project["users"] or \
            project["resources"][resource_title] < amount:
            return False

        resource["availability"] += amount
        project["resources"][resource_title] -= amount
        return True

controller = Controller()
