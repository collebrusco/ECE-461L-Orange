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
  const [user, setUser] = React.useState("");

  const doSignUp = React.useCallback((username, password) => {
    setStatus(AUTH_STATUS.PENDING);
    return signup(username, password).then((ok) => {
      setStatus(AUTH_STATUS.PENDING);
      if (ok) {
        setStatus(AUTH_STATUS.AUTHENTICATED);
      } else {
        setStatus(AUTH_STATUS.UNAUTHENTICATED);
      }
      return ok;
    });
  }, []);

  const doSignIn = React.useCallback((username, password) => {
    setStatus(AUTH_STATUS.PENDING);
    return signin(username, password).then((ok) => {
      setStatus(AUTH_STATUS.PENDING);
      if (ok) {
        setStatus(AUTH_STATUS.AUTHENTICATED);
      } else {
        setStatus(AUTH_STATUS.UNAUTHENTICATED);
      }
      return ok;
    });
  }, []);

  const doSignOut = React.useCallback(() => {
    setStatus(AUTH_STATUS.PENDING);
    return signout().then(() => {
      setStatus(AUTH_STATUS.UNAUTHENTICATED);
    });
  }, []);

  React.useEffect(() => {
    getCurrentUser().then((user) => {
      setStatus(AUTH_STATUS.PENDING);
      if (user) {
        setUser(user);
        setStatus(AUTH_STATUS.AUTHENTICATED);
      } else {
        setStatus(AUTH_STATUS.UNAUTHENTICATED);
      }
    });
  });

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
