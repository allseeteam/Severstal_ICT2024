import { createContext, useContext, useEffect, useState } from 'react';
import { fakeAuthProvider } from '../services/auth';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { AuthParams } from '@/api/auth';
import { useToast } from './ui/use-toast';
import { useLocalStorage } from 'usehooks-ts';

interface AuthContextType {
  user: AuthParams;
  signin: (user: AuthParams) => void;
  signout: () => void;
}

const AuthContext = createContext<AuthContextType>(null!);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthParams | null>(null);
  const navigate = useNavigate();
  const location = useLocation();
  const { toast } = useToast();
  const [tokenValue, setTokenValue, removeTokenValue] = useLocalStorage(
    'test-auth',
    ''
  );

  useEffect(() => {
    console.log({ tokenValue });
    if (tokenValue) {
      setUser({
        username: 'test',
        password: '123',
      });
      console.log({ location });
      navigate(location.state?.from?.pathname ?? location.pathname);
    }
  }, [tokenValue]);

  const signin = (newUser: AuthParams) => {
    return fakeAuthProvider.signin(
      newUser,
      (token: string) => {
        setUser(newUser);
        setTokenValue(token);
        console.log('successfully signin');
      },
      (error: any) => {
        toast({
          title: 'Login error',
          description: error,
          variant: 'destructive',
        });
      }
    );
  };

  const signout = () => {
    return fakeAuthProvider.signout(() => {
      setUser(null);
      removeTokenValue();
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
