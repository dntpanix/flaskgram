import { AppContext } from '../context/AppContext.jsx';

export default function Profile({setView}) {
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
}
