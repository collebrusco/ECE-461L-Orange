const API_URL = "http://127.0.0.1:8888";

export async function signup(username, password) {
  const res = await fetch(`${API_URL}/users`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) {
    throw new Error("Failed to sign up.");
  }
}

export async function signin(username, password) {
  const res = await fetch(`${API_URL}/users/login`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
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
  const res = await fetch(`${API_URL}/resources`);
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export async function checkout(resource_name, quantity, project_name) {
  const res = await fetch(`${API_URL}/resources/${resource_name}/checkout`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ project_title: project_name, amount: quantity }),
  });
  if (!res.ok) {
    throw new Error("Failed to checkout.");
  }
}

export async function checkin(resource_name, quantity, project_name) {
  const res = await fetch(`${API_URL}/resources/${resource_name}/checkin`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ project_title: project_name, amount: quantity }),
  });
  if (!res.ok) {
    throw new Error("Failed to checkin.");
  }
}
