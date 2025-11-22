export const API_URL = '/api';

async function request(path, opts) {
  const res = await fetch(API_URL + path, opts);
  let body;
  try { body = await res.json(); } catch(e) { body = null; }
  return { ok: res.ok, status: res.status, body };
}

export function login(data) {
  return request('/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
}

export function signup(data) {
  return request('/signup', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
}

export function getUser(token) {
  return request('/user/me', {
    headers: {'Authorization': `Bearer ${token}`}
  });
}

export function getPosts(token) {
  return request('/posts', {
    headers: {'Authorization': `Bearer ${token}`}
  });
}

export function createPost(token, post) {
  return request('/posts', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
    body: JSON.stringify(post)
  });
}
