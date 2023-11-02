import { RESOURCES } from "./data";

function getUsers() {
  const users = localStorage.getItem("users");
  return users ? JSON.parse(users) : {};
}

function setCurrentUser(username) {
  const users = getUsers();
  localStorage.setItem("currentUser", JSON.stringify({
    ...users[username],
    username
  }));
}

export async function signup(username, password) {
  const users = getUsers();
  if (username in users) {
    return false;
  }
  users[username] = { password, createdAt: new Date().toISOString() };
  localStorage.setItem("users", JSON.stringify(users));
  setCurrentUser(username);
  return true;
}

export async function signin(username, password) {
  const users = getUsers();
  if (username in users && users[username].password === password) {
    setCurrentUser(username);
    return true;
  }
  return false;
}

export async function getCurrentUser() {
  const currentUser = localStorage.getItem("currentUser");
  return currentUser ? JSON.parse(currentUser) : "";
}

export async function signout() {
  return localStorage.removeItem("currentUser");
}

function getProjects() {
  const projects = localStorage.getItem("projects");
  return projects ? JSON.parse(projects) : [];
}

export async function getUserProjects() {
  const { username } = await getCurrentUser();
  if (!username) return [];
  const projects = getProjects();
  const userProjects = projects.filter(
    (project) => project.users.indexOf(username) !== -1
  );
  return userProjects;
}

export async function createProject(name, description) {
  const { username } = await getCurrentUser();
  const projects = getProjects();
  if (projects.find((project) => project.title === name)) {
    throw new Error("Project already exists");
  }
  projects.push({
    title: name,
    description: description,
    users: [username],
    creator: username,
    resources: {
      "HW Set 1": 0,
      "HW Set 2": 0,
      "HW Set 3": 0,
    },
  });
  localStorage.setItem("projects", JSON.stringify(projects));
}

export async function joinProject(projectName) {
  const { username } = await getCurrentUser();
  const projects = getProjects();
  const project = projects.find((project) => project.title === projectName);
  if (!project) {
    throw new Error("Project not found");
  }
  if (project.users.indexOf(username) !== -1) {
    throw new Error("Already joined");
  }
  project.users.push(username);
  localStorage.setItem("projects", JSON.stringify(projects));
}

export async function getResources() {
  const resources = localStorage.getItem("resources");
  return resources ? JSON.parse(resources) : RESOURCES;
}

export async function checkout(resource_name, quantity, project_name) {
  const resources = await getResources();
  const resource = resources.find(
    (resource) => resource.title === resource_name
  );

  if (resource.availability < quantity) {
    throw new Error("Too many to check out.");
  }
  resource.availability -= quantity;

  const projects = await getProjects();
  const project = projects.find((project) => project.title === project_name);
  project.resources[resource_name] += quantity;
  localStorage.setItem("resources", JSON.stringify(resources));
  localStorage.setItem("projects", JSON.stringify(projects));
}

export async function checkin(resource_name, quantity, project_name) {
  const resources = await getResources();
  const resource = resources.find(
    (resource) => resource.title === resource_name
  );

  if (resource.availability + quantity > resource.capacity) {
    throw new Error("Too many to check in.");
  }
  resource.availability += quantity;

  const projects = await getProjects();
  const project = projects.find((project) => project.title === project_name);
  project.resources[resource_name] -= quantity;
  localStorage.setItem("resources", JSON.stringify(resources));
  localStorage.setItem("projects", JSON.stringify(projects));
}
