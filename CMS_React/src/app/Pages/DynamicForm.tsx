import React, { useState } from 'react';
import {
  Button,
  Form,
  FormGroup,
  TextInput,
  Title,
  ActionGroup,
} from '@patternfly/react-core';

interface DynamicFormProps {
    fields: string[];
  }
  
const DynamicForm: React.FC<DynamicFormProps> = ({ fields }) => {
    const [formValues, setFormValues] = useState<{ [key: string]: string }>(
        {}
    );

    const handleInputChange = (field: string, value: string) => {
        setFormValues((prevValues) => ({ ...prevValues, [field]: value }));
    };

    return (
        <Form>
            {fields.map((field) => (
                <FormGroup key={field} label={field} isRequired>
                    <TextInput
                        type="text"
                        id={field}
                        name={field}
                        value={formValues[field] || ''}
                        onChange={(value) => handleInputChange(field, value)}
                    />
                </FormGroup>
            ))}
        </Form>
    );
};
  