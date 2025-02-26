import { useState } from 'react';

function Login() {
  const [isLogin, setIsLogin] = useState(true); // Toggle between login and registration
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState(''); // For registration

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isLogin) {
      console.log('Login attempt:', { email, password });
    } else {
      console.log('Registration attempt:', { name, email, password });
    }
    // Later: Connect to back-end API
  };

  return (
    <div className="mt-4">
      <h2>{isLogin ? 'Login' : 'Register'}</h2>
      <form onSubmit={handleSubmit}>
        {!isLogin && (
          <div className="mb-3">
            <label>Name:</label>
            <input
              type="text"
              className="form-control"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required={!isLogin}
            />
          </div>
        )}
        <div className="mb-3">
          <label>Email:</label>
          <input
            type="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label>Password:</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          {isLogin ? 'Login' : 'Register'}
        </button>
        <button
          type="button"
          className="btn btn-link"
          onClick={() => setIsLogin(!isLogin)}
        >
          {isLogin ? 'Need to register?' : 'Already have an account?'}
        </button>
      </form>
    </div>
  );
}

export default Login;