// AlertComponent.tsx
import React, { useState, useEffect } from 'react';
import { Alert, AlertVariant } from '@patternfly/react-core';
import './AlertComponent.css';

interface AlertComponentProps {
  variant: AlertVariant;
  message: string;
  show: boolean;
  onClose: () => void;
}

const AlertComponent: React.FC<AlertComponentProps> = ({ variant, message, show, onClose }) => {
  const [isAlertVisible, setIsAlertVisible] = useState(false);

  useEffect(() => {
    if (show) {
      setIsAlertVisible(true);

      // Automatically hide the alert after a certain duration (e.g., 5 seconds)
      const timeoutId = setTimeout(() => {
        onClose();
      }, 5000);

      return () => {
        // Clear the timeout on unmount or when show becomes false
        clearTimeout(timeoutId);
      };
    }
  }, [show, onClose]);

  return (
    <div className={`alert-container ${isAlertVisible ? 'visible' : 'hidden'}`}>
      {isAlertVisible && (
        <Alert
          variant={variant}
          title={message}
          actionClose={<span onClick={() => onClose()}>×</span>}
        />
      )}
    </div>
  );
};

export default AlertComponent;
