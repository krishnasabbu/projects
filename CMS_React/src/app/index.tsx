import * as React from 'react';
import '@patternfly/react-core/dist/styles/base.css';
import { BrowserRouter as Router } from 'react-router-dom';
import { AppLayout } from '@app/AppLayout/AppLayout';
import { AppRoutes } from '@app/routes';
import '@app/app.css';
import TemplateProvider from './context/TemplateProvider';
import AuthProvider from './context/AuthProvider';


const App: React.FunctionComponent = () => (
  <Router>
    <AuthProvider>
      <TemplateProvider>
        <AppLayout>
          <AppRoutes />
        </AppLayout>
      </TemplateProvider>
    </AuthProvider>
  </Router>
);

export default App;
