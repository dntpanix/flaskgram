import { AppContext } from '../context/AppContext.jsx';

export default function HomeFeed({setView}) {
  const { posts, loadPosts } = React.useContext(AppContext);

  React.useEffect(() => {
    loadPosts();
  }, []);

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
}
