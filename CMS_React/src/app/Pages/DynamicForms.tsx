import React, {useRef } from 'react';
import {
  Button,
  TextInput,
  FormGroup,
  Form,
  Stack,
  StackItem,
  Panel,
  PanelMain,
  PanelMainBody,
  PageSection,
  PageSectionVariants,
  TextContent,
  Text,
} from '@patternfly/react-core';
import { useTemplateContext } from "@app/context/TemplateProvider";
import { DynamicVariable } from '@app/utils/type';


export const DynamicForm: React.FC = () => {
  const {dynamicVariables, setDynamicVariables, formDynamicVariables, setFormDynamicVariables} = useTemplateContext();
  const inputRefs = useRef<Array<{ name: HTMLInputElement | null; formula: HTMLInputElement | null }>>(
    []
  );
  console.log("form data ==== "+dynamicVariables);
  console.log("form data ==== "+formDynamicVariables);

  const handleSave = () => {
    // Gather values from the input fields
    const updatedFormList: DynamicVariable[] = inputRefs.current.map((ref, index) => ({
      id: index + '',
      name: ref.name?.value || '',
      formula: ref.formula?.value || '',
      formatter: '',
    }));

    // Update the state with the gathered values
    setFormDynamicVariables(updatedFormList);

    // If you want to convert the form data list to JSON
    const jsonData = JSON.stringify(updatedFormList);
    console.log('JSON Data List:', jsonData);
  };

  const handleAddForm = () => {
    // Add a new form with default values
    setFormDynamicVariables((prevList) => [...prevList, { name: '', formula: '' }]);

    // Initialize the refs for the new form
    inputRefs.current.push({ name: null, formula: null });
  };

  const panelStyle: React.CSSProperties = {
    border: `2px solid #f3b6b6`,
    backgroundColor: '#f0f0f0',
  };

  return (
    <React.Fragment>
      <PageSection variant={PageSectionVariants.light}>
          
      </PageSection>
      <Form>
        {formDynamicVariables.map((formData, index) => (
            <PageSection variant={PageSectionVariants.light} style={panelStyle} className='custom-panel'>
              <TextContent>
                  <Text component="h5">For muliple formatter values provide with comma seperated</Text>
              </TextContent>
              <Stack key={index} gutter="md">
                <StackItem>
                  <FormGroup label="Name" fieldId={`field1_${index}`}>
                    <TextInput
                      type="text"
                      id={`field1_${index}`}
                      ref={(el) => (inputRefs.current[index] = { ...inputRefs.current[index], name: el })}
                      defaultValue={formData.name}
                    />
                  </FormGroup>
                </StackItem>
                <StackItem>
                  <FormGroup label="Formula" fieldId={`field2_${index}`}>
                    <TextInput
                      type="text"
                      id={`field2_${index}`}
                      ref={(el) => (inputRefs.current[index] = { ...inputRefs.current[index], formula: el })}
                      defaultValue={formData.formula}
                    />
                  </FormGroup>
                </StackItem>
              </Stack>
            </PageSection>
        ))}

        <Button variant="secondary" onClick={handleAddForm}>
          Add Formatter
        </Button>
        <Button variant="primary" onClick={handleSave}>
          Save
        </Button>
      </Form>
    </React.Fragment>
  );
};
