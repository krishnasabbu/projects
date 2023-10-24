
import { NavLink, Navigate, useLocation } from 'react-router-dom';

const AuthGuard = ({ children }) => {
  //const { isAuthenticated } = useAuth();
  const { pathname } = useLocation();

  console.log("pathName =========== "+pathname);

  if (true) return <>{children}</>;

  return <NavLink replace to="/login" state={{ from: pathname }} />;
};

export default AuthGuard;
