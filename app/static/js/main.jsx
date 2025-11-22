/* Combined single-file main.jsx for babel-standalone usage
   Replace your static/js/main.jsx with this file (no imports/exports).
   Note: uses global React, ReactDOM and Babel (as in your index.html).
*/

/* --- API (inlined) --- */
const api = (function(){
  const API_URL = '/api';
  async function request(path, opts) {
    const res = await fetch(API_URL + path, opts);
    let body;
    try { body = await res.json(); } catch(e) { body = null; }
    return { ok: res.ok, status: res.status, body };
  }
  function login(data){ return request('/login', { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)}); }
  function signup(data){ return request('/signup', { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data)}); }
  function getUser(token){ return request('/user/me', { headers:{'Authorization': `Bearer ${token}`} }); }
  function getPosts(token){ return request('/posts', { headers:{'Authorization': `Bearer ${token}`} }); }
  function createPost(token, post){ return request('/posts', { method:'POST', headers:{'Content-Type':'application/json','Authorization': `Bearer ${token}`}, body: JSON.stringify(post)}); }
  return { login, signup, getUser, getPosts, createPost };
})();

/* --- AppContext (inlined) --- */
import { AppProvider } from './context/AppContext.jsx';
import App from './App.jsx';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <AppProvider>
    <App />
  </AppProvider>
);