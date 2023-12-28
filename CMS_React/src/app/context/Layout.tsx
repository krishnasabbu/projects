// Layout.tsx
import React, { ReactNode } from 'react';
import AlertComponent from '@app/utils/AlertComponent';
import { AlertVariant } from '@patternfly/react-core';
import './AlertComponent.css';

interface LayoutProps {
  children: ReactNode;
  alertProps: {
    variant: AlertVariant;
    message: string;
    show: boolean;
    onClose: () => void;
  };
}

const Layout: React.FC<LayoutProps> = ({ children, alertProps }) => {
  return (
    <div>
      {/* Your navigation or header components can go here */}
      
      {/* Show the AlertComponent based on the state */}
      <AlertComponent {...alertProps} />
      
      {/* Render the content of the page */}
      {children}
      
      {/* Your footer or other components can go here */}
    </div>
  );
};

export default Layout;
