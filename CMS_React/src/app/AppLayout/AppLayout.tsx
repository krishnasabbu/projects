import * as React from 'react';
import { Home } from './Home';
import { Login } from '@app/Pages/Login';
import { useAuth } from '@app/context/AuthProvider';

interface IAppLayout {
  children: React.ReactNode;
}

const AppLayout: React.FunctionComponent<IAppLayout> = ({ children }) => {

  const { token } = useAuth();

  if(token) {
    return <Login  />
  }

  return (
    <Home>
      {children}
    </Home>
  );
};

export { AppLayout };
