import { AppContext } from '../context/AppContext.jsx';

export default function Signup({setView}) {
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
}
