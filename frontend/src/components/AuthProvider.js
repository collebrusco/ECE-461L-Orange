import React from "react";
import { useLocation, Navigate } from "react-router-dom";
import { signup, signin, getCurrentUser, signout } from "../lib/api";

const AuthContext = React.createContext(null);
export const authStatus = {
  pending: 0,
  authenticated: 1,
  unautenticated: 2,
};

export default function AuthProvider({ children }) {
  const [status, setStatus] = React.useState(authStatus.pending);

  const doSignUp = React.useCallback((username, password) => {
    setStatus(authStatus.pending);
    return signup(username, password).then((ok) => {
      setStatus(authStatus.pending);
      if (ok) {
        setStatus(authStatus.authenticated);
      } else {
        setStatus(authStatus.unautenticated);
      }
      return ok;
    });
  }, []);

  const doSignIn = React.useCallback((username, password) => {
    setStatus(authStatus.pending);
    return signin(username, password).then((ok) => {
      setStatus(authStatus.pending);
      if (ok) {
        setStatus(authStatus.authenticated);
      } else {
        setStatus(authStatus.unautenticated);
      }
      return ok;
    });
  }, []);

  const doSignOut = React.useCallback(() => {
    setStatus(authStatus.pending);
    return signout().then(() => {
      setStatus(authStatus.unautenticated);
    });
  }, []);

  React.useEffect(() => {
    setStatus(authStatus.pending);
    getCurrentUser().then((user) => {
      setStatus(authStatus.pending);
      if (user) {
        setStatus(authStatus.authenticated);
      } else {
        setStatus(authStatus.unautenticated);
      }
    });
  }, []);

  const value = React.useMemo(
    () => ({
      status,
      doSignUp,
      doSignIn,
      doSignOut,
    }),
    [status, doSignUp, doSignIn, doSignOut]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return React.useContext(AuthContext);
}

export function RequireAuth({ children }) {
  const { status } = useAuth();
  const location = useLocation();

  if (status === authStatus.authenticated) {
    return children;
  }

  return <Navigate to="/signin" state={{ from: location }} replace />;
}
