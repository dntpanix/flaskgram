import Login from './components/Login.jsx';
import Signup from './components/Signup.jsx';
import HomeFeed from './components/HomeFeed.jsx';
import CreatePost from './components/CreatePost.jsx';
import Profile from './components/Profile.jsx';
import { AppContext } from './context/AppContext.jsx';

export default function App() {
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
