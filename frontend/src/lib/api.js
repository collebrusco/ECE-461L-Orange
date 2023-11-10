import { RESOURCES } from "./data";

console.log(process.env.REACT_APP_ENV);
const API_URL = process.env.REACT_APP_ENV === 'development' ? "http://127.0.0.1:8888" : 'https://teamorange.duckdns.org/api';


export async function signup(username, password) {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);
  const res = await fetch(`${API_URL}/users`, {
    method: "POST",
    credentials: "include",
    body: formData,
  });
  if (!res.ok) {
    throw new Error("Failed to sign up.");
  }
}

export async function signin(username, password) {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);
  const res = await fetch(`${API_URL}/users/login`, {
    method: "POST",
    credentials: "include",
    body: formData,
  });
  if (!res.ok) {
    throw new Error("Failed to sign in.");
  }
}

export async function getCurrentUser() {
  const res = await fetch(`${API_URL}/users/profile`, {
    credentials: "include",
  });
  if (!res.ok) {
    return {};
  }
  return res.json();
}

export async function signout() {
  const res = await fetch(`${API_URL}/users/logout`, {
    method: "POST",
    credentials: "include",
  });
  if (!res.ok) {
    throw new Error("Failed to sign out.");
  }
}

function getProjects() {
  const projects = localStorage.getItem("projects");
  return projects ? JSON.parse(projects) : [];
}

export async function getUserProjects() {
  const res = await fetch(`${API_URL}/projects`, {
    credentials: "include",
  });
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export async function createProject(name, description) {
  const res = await fetch(`${API_URL}/projects`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title: name, description }),
  });
  if (!res.ok) {
    const data = await res.json();
    console.error(data.msg);
    throw new Error(data.msg);
  }
}

export async function joinProject(projectName) {
  const res = await fetch(`${API_URL}/projects/${projectName}/users`, {
    method: "POST",
    credentials: "include",
  });
  if (!res.ok) {
    throw new Error("Failed to join project.");
  }
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
