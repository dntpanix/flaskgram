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
const AppContext = React.createContext();

function AppProvider({children}) {
  const [token, setToken] = React.useState(localStorage.getItem('fg_token'));
  const [user, setUser] = React.useState(null);
  const [posts, setPosts] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');

  React.useEffect(() => {
    if (token) {
      localStorage.setItem('fg_token', token);
      loadProfile();
      loadPosts();
    } else {
      localStorage.removeItem('fg_token');
      setUser(null);
      setPosts([]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  async function loadProfile() {
    if (!token) return;
    const res = await api.getUser(token);
    if (res.ok) setUser(res.body);
  }

  async function loadPosts() {
    if (!token) return;
    const res = await api.getPosts(token);
    if (res.ok) setPosts(res.body.posts || []);
  }

  async function doLogin(credentials) {
    setError(''); setLoading(true);
    const res = await api.login(credentials);
    if (res.ok) {
      setToken(res.body.token);
      setError('');
      setLoading(false);
      return { ok: true };
    } else {
      setError(res.body?.msg || 'Login failed');
      setLoading(false);
      return { ok: false, msg: res.body?.msg };
    }
  }

  async function doSignup(data) {
    setError(''); setLoading(true);
    const res = await api.signup(data);
    setLoading(false);
    if (res.ok) return { ok: true };
    setError(res.body?.msg || 'Signup failed');
    return { ok: false, msg: res.body?.msg };
  }

  async function doCreatePost(post) {
    setError(''); setLoading(true);
    const res = await api.createPost(token, post);
    setLoading(false);
    if (res.ok) {
      await loadPosts();
      return { ok: true, post: res.body.post };
    } else {
      setError(res.body?.msg || 'Failed to create post');
      return { ok: false, msg: res.body?.msg };
    }
  }

  function logout() { setToken(null); }

  return (
    <AppContext.Provider value={{
      token, user, posts, loading, error,
      setToken, setUser, setPosts,
      doLogin, doSignup, loadPosts, loadProfile, doCreatePost, logout
    }}>
      {children}
    </AppContext.Provider>
  );
}

/* --- Components (inlined) --- */

/* Login */
const Login = function({setView}) {
  const { doLogin, loading, error } = React.useContext(AppContext);
  const [form, setForm] = React.useState({ email: '', password: '' });

  const submit = async () => {
    const res = await doLogin(form);
    if (res.ok) setView('home');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="bg-white border border-gray-300 p-10 mb-3">
          <div className="text-center mb-8">
            <h1 className="font-bold text-4xl mb-8" style={{ fontFamily: 'Satisfy, cursive' }}>FlaskGram</h1>
          </div>

          {error && (<div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4 text-sm">{error}</div>)}

          <div className="space-y-2">
            <input type="email" placeholder="Email" value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded text-sm bg-gray-50 focus:outline-none focus:border-gray-400"/>
            <input type="password" placeholder="Password" value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded text-sm bg-gray-50 focus:outline-none focus:border-gray-400"/>
            <button onClick={submit} disabled={loading}
              className="w-full bg-blue-500 text-white py-2 rounded font-semibold text-sm hover:bg-blue-600 disabled:bg-blue-300 mt-3">
              {loading ? 'Loading...' : 'Log In'}
            </button>
          </div>
        </div>

        <div className="bg-white border border-gray-300 p-5 text-center">
          <p className="text-sm">
            Don't have an account?
            <button onClick={() => setView('signup')} className="text-blue-500 font-semibold"> Sign up</button>
          </p>
        </div>
      </div>
    </div>
  );
};

/* Signup */
const Signup = function({setView}) {
  const { doSignup, loading, error } = React.useContext(AppContext);
  const [form, setForm] = React.useState({ username:'', email:'', password:'', confirm_password: '' });

  const submit = async () => {
    if (form.password !== form.confirm_password) {
      alert('Passwords do not match'); return;
    }
    const res = await doSignup(form);
    if (res.ok) setView('login');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="bg-white border border-gray-300 p-10 mb-3">
          <div className="text-center mb-8">
            <h1 className="font-bold text-4xl mb-8" style={{ fontFamily: 'Satisfy, cursive' }}>FlaskGram</h1>
          </div>

          {error && (<div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4 text-sm">{error}</div>)}

          <div className="space-y-2">
            <input placeholder="Username" value={form.username}
              onChange={(e)=>setForm({...form, username: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded text-sm bg-gray-50"/>
            <input type="email" placeholder="Email" value={form.email}
              onChange={(e)=>setForm({...form, email: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded text-sm bg-gray-50"/>
            <input type="password" placeholder="Password" value={form.password}
              onChange={(e)=>setForm({...form, password: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded text-sm bg-gray-50"/>
            <input type="password" placeholder="Confirm Password" value={form.confirm_password}
              onChange={(e)=>setForm({...form, confirm_password: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded text-sm bg-gray-50"/>
            <button onClick={submit} disabled={loading}
              className="w-full bg-blue-500 text-white py-2 rounded font-semibold text-sm hover:bg-blue-600 disabled:bg-blue-300 mt-3">
              {loading ? 'Loading...' : 'Sign Up'}
            </button>
          </div>
        </div>

        <div className="bg-white border border-gray-300 p-5 text-center">
          <p className="text-sm">
            Have an account?
            <button onClick={() => setView('login')} className="text-blue-500 font-semibold"> Log in</button>
          </p>
        </div>
      </div>
    </div>
  );
};

/* HomeFeed */
const HomeFeed = function({setView}) {
  const { posts, loadPosts } = React.useContext(AppContext);

  React.useEffect(() => { loadPosts(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="max-w-xl mx-auto">
        {posts.length === 0 ? (
          <div className="bg-white border border-gray-300 rounded-lg p-8 text-center">
            <div className="mx-auto mb-4 text-gray-400" style={{fontSize:48}}>📷</div>
            <h3 className="font-semibold text-xl mb-2">No Posts Yet</h3>
            <p className="text-gray-500 mb-4">Start by creating your first post!</p>
            <button onClick={() => setView('create')} className="bg-blue-500 text-white px-6 py-2 rounded font-semibold hover:bg-blue-600">
              Create Post
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            {posts.map((post, idx) => (
              <div key={idx} className="bg-white border border-gray-300 rounded-lg">
                <div className="flex items-center justify-between p-3">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white font-semibold">
                      {post.author?.username?.[0]?.toUpperCase() || 'U'}
                    </div>
                    <span className="font-semibold text-sm">{post.author?.username || 'User'}</span>
                  </div>
                </div>

                <div className="w-full aspect-square bg-gray-100 flex items-center justify-center">
                  {post.image_url ? (<img src={post.image_url} alt={post.caption} className="w-full h-full object-cover" />) : (<div style={{fontSize:32}}>📷</div>)}
                </div>

                <div className="p-3">
                  <div className="flex items-center gap-4 mb-3">
                    <button className="hover:text-gray-500">♥</button>
                    <button className="hover:text-gray-500">💬</button>
                    <button className="hover:text-gray-500">✈️</button>
                    <button className="hover:text-gray-500 ml-auto">🔖</button>
                  </div>

                  {post.likes > 0 && (<p className="font-semibold text-sm mb-2">{post.likes} likes</p>)}
                  {post.caption && (<p className="text-sm"><span className="font-semibold mr-2">{post.author?.username || 'User'}</span>{post.caption}</p>)}
                  {post.timestamp && (<p className="text-xs text-gray-400 mt-2">{new Date(post.timestamp).toLocaleDateString()}</p>)}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

/* CreatePost */
const CreatePost = function({setView}) {
  const { doCreatePost, loading } = React.useContext(AppContext);
  const [post, setPost] = React.useState({ caption: '', image_url: '' });
  const submit = async () => {
    const res = await doCreatePost(post);
    if (res.ok) setView('home');
  };

  return (
    <div className="max-w-xl mx-auto">
      <div className="bg-white border border-gray-300 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Create New Post</h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold mb-2">Image URL</label>
            <input type="url" placeholder="https://example.com/image.jpg" value={post.image_url}
              onChange={(e)=>setPost({...post, image_url: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-gray-400"/>
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2">Caption</label>
            <textarea placeholder="Write a caption..." value={post.caption}
              onChange={(e)=>setPost({...post, caption: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-gray-400 resize-none" rows="4"/>
          </div>

          <button onClick={submit} disabled={loading} className="w-full bg-blue-500 text-white py-2 rounded font-semibold hover:bg-blue-600 disabled:bg-blue-300">
            {loading ? 'Posting...' : 'Share'}
          </button>
        </div>
      </div>
    </div>
  );
};

/* Profile */
const Profile = function({setView}) {
  const { user, posts, logout } = React.useContext(AppContext);

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white border border-gray-300 rounded-lg p-8">
        <div className="flex items-center gap-8 mb-8">
          <div className="w-32 h-32 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white text-4xl font-bold">
            {user?.username?.[0]?.toUpperCase() || 'U'}
          </div>

          <div className="flex-1">
            <div className="flex items-center gap-4 mb-4">
              <h2 className="text-2xl">{user?.username || 'Username'}</h2>
              <button className="bg-gray-100 px-4 py-1 rounded font-semibold text-sm hover:bg-gray-200">Edit Profile</button>
              <button onClick={logout} className="bg-gray-100 px-4 py-1 rounded font-semibold text-sm hover:bg-gray-200">Logout</button>
            </div>

            <div className="flex gap-8 mb-4">
              <span><strong>{posts.length}</strong> posts</span>
              <span><strong>{user?.followers || 0}</strong> followers</span>
              <span><strong>{user?.following || 0}</strong> following</span>
            </div>

            <div>
              <p className="font-semibold">{user?.name || user?.username}</p>
              <p className="text-sm text-gray-600">{user?.email}</p>
            </div>
          </div>
        </div>

        <div className="border-t pt-6">
          <h3 className="text-center text-gray-400 text-sm font-semibold mb-4">POSTS</h3>
          <div className="grid grid-cols-3 gap-1">
            {posts.filter(p => p.author?.username === user?.username).map((post, idx) => (
              <div key={idx} className="aspect-square bg-gray-100 flex items-center justify-center">
                {post.image_url ? (<img src={post.image_url} alt={post.caption} className="w-full h-full object-cover" />) : (<div style={{fontSize:32}}>📷</div>)}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

/* --- App --- */
function App() {
  const { token } = React.useContext(AppContext);
  const [view, setView] = React.useState(token ? 'home' : 'login');

  if (!token && view === 'signup') return <Signup setView={setView} />;
  if (!token) return <Login setView={setView} />;

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-300 sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
          <h1 className="font-bold text-2xl" style={{ fontFamily: 'Satisfy, cursive' }}>FlaskGram</h1>
          <div className="flex items-center gap-6">
            <button onClick={() => setView('home')} className={view === 'home' ? 'text-black' : 'text-gray-400'}>Home</button>
            <button onClick={() => setView('create')} className={view === 'create' ? 'text-black' : 'text-gray-400'}>Create</button>
            <button onClick={() => setView('profile')} className={view === 'profile' ? 'text-black' : 'text-gray-400'}>Profile</button>
          </div>
        </div>
      </header>

      <main>
        {view === 'home' && <HomeFeed setView={setView} />}
        {view === 'create' && <CreatePost setView={setView} />}
        {view === 'profile' && <Profile setView={setView} />}
      </main>
    </div>
  );
}

/* --- Mount --- */
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <AppProvider>
    <App />
  </AppProvider>
);
