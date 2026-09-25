import { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import type { User } from 'firebase/auth';
import { firebaseAuth } from '../config/firebase';
import { login as authServiceLogin, register as authServiceRegister, logout as authServiceLogout } from '../services/auth';

interface AuthContextType {
  currentUser: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  role: string | null;
  login: typeof authServiceLogin;
  register: typeof authServiceRegister;
  logout: typeof authServiceLogout;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(firebaseAuth, async (user) => {
      if (user) {
        try {
          // Get the custom claims from the ID token
          const idTokenResult = await user.getIdTokenResult();
          setRole(idTokenResult.claims.role as string || null);
        } catch (error) {
          console.error("Error fetching custom claims:", error);
          setRole(null);
        }
      } else {
        setRole(null);
      }
      
      setCurrentUser(user);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const value = {
    currentUser,
    loading,
    isAuthenticated: !!currentUser,
    role,
    login: authServiceLogin,
    register: authServiceRegister,
    logout: authServiceLogout,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
