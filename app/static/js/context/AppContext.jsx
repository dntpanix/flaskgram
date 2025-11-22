import * as api from '../api/api.js';

export const AppContext = React.createContext();

export function AppProvider({children}) {
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

  function logout() {
    setToken(null);
  }

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
