function getUsers() {
  const users = localStorage.getItem('users');
  return users ? JSON.parse(users) : {};
}

export async function signup(username, password) {
  const users = getUsers();
  if (username in users) {
    return false;
  }
  users[username] = password;
  localStorage.setItem('users', JSON.stringify(users));
  localStorage.setItem('currentUser', username);
  return true;
}

export async function signin(username, password) {
  const users = getUsers();
  if (username in users && users[username] === password) {
    localStorage.setItem('currentUser', username);
    return true;
  }
  return false;
}

export async function getCurrentUser() {
  return localStorage.getItem('currentUser');
}

export async function signout() {
  return localStorage.removeItem('currentUser');
}
