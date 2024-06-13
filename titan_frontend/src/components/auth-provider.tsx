import { createContext, useContext, useState } from 'react';
import { fakeAuthProvider } from '../services/auth';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { AuthParams } from '@/api/auth';

interface AuthContextType {
  user: AuthParams;
  signin: (user: AuthParams) => void;
  signout: () => void;
}

const AuthContext = createContext<AuthContextType>(null!);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthParams | null>(null);

  const signin = (newUser: AuthParams) => {
    return fakeAuthProvider.signin(newUser, () => {
      setUser(newUser);
      console.log('successfully signin');
    });
  };

  const signout = () => {
    return fakeAuthProvider.signout(() => {
      setUser(null);
    });
  };

  const value = { user, signin, signout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthStatus() {
  const auth = useAuth();
  const navigate = useNavigate();

  if (!auth.user) {
    return <p>You are not logged in.</p>;
  }

  return (
    <p>
      Welcome {auth.user}!{' '}
      <button
        onClick={() => {
          auth.signout(() => navigate('/'));
        }}
      >
        Sign out
      </button>
    </p>
  );
}

export function RequireAuth({ children }: { children: JSX.Element }) {
  const auth = useAuth();
  const location = useLocation();

  if (!auth.user) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
