import React from "react";
import { PageSection, PageSectionVariants, Form,
    FormGroup,
    TextInput,
    HelperText,
    HelperTextItem,
    FormHelperText, 
    TextArea} from '@patternfly/react-core';
import { useTemplateContext } from "@app/context/TemplateProvider";

export const TemplateForm: React.FunctionComponent = () => {

  const { id, name, updateId, updateName, description, updateDescription, version, updateVersion } = useTemplateContext();

  return (
      <React.Fragment>
        <PageSection variant={PageSectionVariants.light}>
          <Form>
              <FormGroup
                label="Message Template Id"
                isRequired
                fieldId="simple-form-name-01"
              >
                <TextInput
                  isRequired
                  type="text"
                  id="simple-form-name-01"
                  name="simple-form-name-01"
                  aria-describedby="simple-form-name-01-helper"
                  value={id}
                  onChange={(_event, value) => updateId(value)}
                />
                <FormHelperText>
                  <HelperText>
                    <HelperTextItem>Alert Number : 101</HelperTextItem>
                  </HelperText>
                </FormHelperText>
              </FormGroup>
              <FormGroup label="Template Name" isRequired fieldId="simple-form-email-01">
                <TextInput
                  isRequired
                  type="text"
                  id="simple-form-email-01"
                  name="simple-form-email-01"
                  value={name}
                  onChange={(_event, value) => updateName(value)}
                />
                <FormHelperText>
                  <HelperText>
                    <HelperTextItem>Template  : Over draft Non-sufficent funds</HelperTextItem>
                  </HelperText>
                </FormHelperText>
              </FormGroup>
              <FormGroup
                label="Template Description"
                isRequired
                fieldId="simple-form-name-01"
              >
                <TextArea value={description} onChange={(_event, value) => updateDescription(value)} aria-label="text area example" />
                <FormHelperText>
                  <HelperText>
                    <HelperTextItem>Description</HelperTextItem>
                  </HelperText>
                </FormHelperText>
              </FormGroup>
              <FormGroup label="Version" isRequired fieldId="simple-form-phone-01">
                <TextInput
                  isRequired
                  type="text"
                  id="simple-form-phone-01"
                  name="simple-form-phone-01"
                  placeholder="5.0"
                  value={version}
                  onChange={(_event, value) => updateVersion(value)}
                />
              </FormGroup>
          </Form>
        </PageSection>
      </React.Fragment>
  );
};