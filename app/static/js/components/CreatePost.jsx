import { AppContext } from '../context/AppContext.jsx';

export default function CreatePost({setView}) {
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
}
