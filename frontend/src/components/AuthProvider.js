import React from "react";
import { signup, signin, getCurrentUser, signout } from "../lib/api";
import Loading from "./Loading";
import SignInUpDialog from "./SignInUpDialog";

export const AUTH_STATUS = {
  PENDING: 0,
  AUTHENTICATED: 1,
  UNAUTHENTICATED: 2,
};

const AuthContext = React.createContext(null);
export function useAuth() {
  return React.useContext(AuthContext);
}

export function RequireAuth({ children }) {
  const { status } = useAuth();
  return (
    <>
      {status === AUTH_STATUS.PENDING && <Loading />}
      {status === AUTH_STATUS.UNAUTHENTICATED && <SignInUpDialog />}
      {children}
    </>
  );
}

export default function AuthProvider({ children }) {
  const [status, setStatus] = React.useState(AUTH_STATUS.PENDING);
  const [user, setUser] = React.useState({});

  const updateUser = () => {
    getCurrentUser().then((user) => {
      setStatus(AUTH_STATUS.PENDING);
      setUser(user);
      if (user.username) {
        setStatus(AUTH_STATUS.AUTHENTICATED);
      } else {
        setStatus(AUTH_STATUS.UNAUTHENTICATED);
      }
    });
  };

  const doSignUp = React.useCallback((username, password) => {
    setStatus(AUTH_STATUS.PENDING);
    return signup(username, password).finally(updateUser);
  }, []);

  const doSignIn = React.useCallback((username, password) => {
    setStatus(AUTH_STATUS.PENDING);
    return signin(username, password).finally(updateUser);
  }, []);

  const doSignOut = React.useCallback(() => {
    setStatus(AUTH_STATUS.PENDING);
    return signout().finally(updateUser);
  }, []);

  React.useEffect(() => {
    updateUser();
  }, []);

  const value = React.useMemo(
    () => ({
      status,
      user,
      doSignUp,
      doSignIn,
      doSignOut,
    }),
    [status, user, doSignUp, doSignIn, doSignOut]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
