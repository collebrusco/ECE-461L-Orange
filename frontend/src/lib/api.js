function getUsers() {
  const users = localStorage.getItem("users");
  return users ? JSON.parse(users) : {};
}

export async function signup(username, password) {
  const users = getUsers();
  if (username in users) {
    return false;
  }
  users[username] = password;
  localStorage.setItem("users", JSON.stringify(users));
  localStorage.setItem("currentUser", username);
  return true;
}

export async function signin(username, password) {
  const users = getUsers();
  if (username in users && users[username] === password) {
    localStorage.setItem("currentUser", username);
    return true;
  }
  return false;
}

export async function getCurrentUser() {
  return localStorage.getItem("currentUser") || "";
}

export async function signout() {
  return localStorage.removeItem("currentUser");
}

function getProjects() {
  const projects = localStorage.getItem("projects");
  return projects ? JSON.parse(projects) : [];
}

export async function getUserProjects() {
  const username = await getCurrentUser();
  if (!username) return [];
  const projects = getProjects();
  const userProjects = projects.filter(project => project.users.indexOf(username) !== -1);
  return userProjects;
}

export async function createProject(name, id, description) {
  const username = await getCurrentUser();
  const projects = getProjects();
  projects.push({
    id: id,
    title: name,
    description: description,
    users: [username],
    creator: username,
    "resources list": [
      {
        "Type A": 100,
      },
      {
        "Type B": 100,
      },
      {
        "Type C": 100,
      },
    ],
  });
  localStorage.setItem("projects", JSON.stringify(projects));
}

export async function joinProject(projectID) {
  const username = await getCurrentUser();
  const projects = getProjects();
  const project = projects.find(project => project.id === projectID);
  if (!project) {
    throw new Error("Project not found");
  }
  project.users.push(username);
  localStorage.setItem("projects", JSON.stringify(projects));
}
