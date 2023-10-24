import React, { useEffect } from "react";
import { Checkbox, PageSection, PageSectionVariants, ProgressStep, ProgressStepper, Text, TextContent, Toolbar, ToolbarContent, ToolbarItem } from "@patternfly/react-core";
import { LogViewer, LogViewerSearch } from "@patternfly/react-log-viewer";
import { useLogs } from "@app/context/LogsContext";
import { useTemplateContext } from "@app/context/TemplateProvider";
import axios from "axios";

const serviceLogColors = {
  liferay: `\u001b[38;2;255;68;255m`
};

const buildConsoleLogLine = ({
  message,
  projectId,
  serviceId,
  buildGroupUid,
  instanceId,
  timestamp
}) => {
  const build = buildGroupUid ? `build-${buildGroupUid} ` : "";
  return `\u001b[38;2;155;155;155m${timestamp} ${serviceLogColors[serviceId]}${build}[${instanceId}] \u001b[38;5;255m${message}`;
};

export const TemplateProgress: React.FunctionComponent = () => {

    const { logs, addLog } = useLogs();
    const [isTextWrapped, setIsTextWrapped] = React.useState(false);
    const [activeStep, setActiveStep] = React.useState(0);
    const { id, name, description, version, fileName, dynamicVariables, file} = useTemplateContext();

    useEffect(() => {
        // Simulate progress by changing the active step after a delay
        console.log("single time");
        const timer = setTimeout(() => {
            setActiveStep((prevStep) => (prevStep < 6 ? prevStep + 1 : prevStep));
        }, 2000);
        return () => clearTimeout(timer);
    }, [activeStep]);

    useEffect(() => {
      console.log("multiple time");
      onFileUpload();
    }, []);

    const onFileUpload = async () => {

      const formData = new FormData();
      formData.append("file", file);
      formData.append("id", id);
      formData.append("name", name);
      formData.append("description", description);
      formData.append("version", version);
      formData.append("fileName", fileName);
      formData.append("dynamicVariables", dynamicVariables);

      try {
        const response = await axios.post('http://localhost:8081/upload', formData);
        console.log(response);
        const intervalId = setInterval(() => {
          fetchData();
        }, 2000);
        
      } catch (error) {
        // Handle errors
        console.error(error);
      }

  };

  const fetchData = async () => {
    try {
      // Make your API call here
      const response = await fetch('http://localhost:8081/response');
      const data = await response.json();
      console.log("data ===== "+data);
      (data).map((item, index) => (
        addLog(buildConsoleLogLine(item))
      ));
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <React.Fragment>
      <PageSection variant={PageSectionVariants.light}>
        <TextContent>
            <Text component="h3">Create Template</Text>
            <Text component="p">Creating template is in progress and update the status below</Text>
        </TextContent>
      </PageSection>
      <PageSection variant={PageSectionVariants.darker}>
          <ProgressStepper aria-label="Basic progress stepper with description">
              <ProgressStep
              variant={activeStep === 0 ? 'info' : 'success'}
              description="This is the first thing to happen"
              id="basic-desc-step1"
              titleId="basic-desc-step1-title"
              aria-label="completed step, step with success"
              >
                File Upload
              </ProgressStep>
              <ProgressStep
              variant={activeStep === 1 ? 'info' : activeStep > 1 ? 'success' : 'pending'}
              isCurrent
              description="This is the second thing to happen"
              id="basic-desc-step2"
              titleId="basic-desc-step2-title"
              aria-label="step with info"
              >
                Json Conversion
              </ProgressStep>
              <ProgressStep
              variant={activeStep === 2 ? 'info' : activeStep > 2 ? 'success' : 'pending'}
              description="This is the last thing to happen"
              id="basic-desc-step3"
              titleId="basic-desc-step3-title"
              aria-label="pending step"
              >
                Dynamic Variable
              </ProgressStep>
              <ProgressStep
              variant={activeStep === 3 ? 'info' : activeStep > 3 ? 'success' : 'pending'}
              description="This is the last thing to happen"
              id="basic-desc-step3"
              titleId="basic-desc-step3-title"
              aria-label="pending step"
              >
                Conditions
              </ProgressStep>
              <ProgressStep
              variant={activeStep === 4 ? 'info' : activeStep > 4 ? 'success' : 'pending'}
              description="This is the last thing to happen"
              id="basic-desc-step3"
              titleId="basic-desc-step3-title"
              aria-label="pending step"
              >
                Components
              </ProgressStep>
              <ProgressStep
              variant={activeStep === 5 ? 'info' : activeStep > 5 ? 'success' : 'pending'}
              description="This is the last thing to happen"
              id="basic-desc-step3"
              titleId="basic-desc-step3-title"
              aria-label="pending step"
              >
                Review & Author
              </ProgressStep>
          </ProgressStepper>
      </PageSection>
      <PageSection variant={PageSectionVariants.light}>
          <LogViewer
            hasLineNumbers={true}
            height={500}
            data={logs}
            theme="dark"
            isTextWrapped={isTextWrapped}
            toolbar={
              <Toolbar>
                <ToolbarContent>
                  <ToolbarItem>
                    <LogViewerSearch placeholder="Search value" minSearchChars={3} />
                  </ToolbarItem>
                  <ToolbarItem>
                    <Checkbox
                      label="Wrap text"
                      aria-label="wrap text checkbox"
                      isChecked={isTextWrapped}
                      id="wrap-text-checkbox"
                      onChange={() => setIsTextWrapped}
                    />
                  </ToolbarItem>
                </ToolbarContent>
              </Toolbar>
            }
          />
      </PageSection>
    </React.Fragment> 
  );
};