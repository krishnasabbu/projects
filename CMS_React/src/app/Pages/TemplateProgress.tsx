import React, { useEffect } from "react";
import { PageSection, PageSectionVariants, ProgressStep, ProgressStepper, Text, TextContent } from "@patternfly/react-core";
import { LogViewer, LogViewerSearch } from "@patternfly/react-log-viewer";

export const TemplateProgress: React.FunctionComponent = () => {

    const [activeStep, setActiveStep] = React.useState(0);

    useEffect(() => {
        // Simulate progress by changing the active step after a delay
        const timer = setTimeout(() => {
            console.log("activeStep ==== "+activeStep);
            setActiveStep((prevStep) => (prevStep < 3 ? prevStep + 1 : prevStep));
        }, 2000);

        return () => clearTimeout(timer);
    }, [activeStep]);

    return (
      <React.Fragment>
        <PageSection variant={PageSectionVariants.light}>
          <TextContent>
              <Text component="h3">Uplaod Functional Requirement Document (FRD)</Text>
              <Text component="p">This is a demo that showcases PatternFly cards.</Text>
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
                First step
                </ProgressStep>
                <ProgressStep
                variant={activeStep === 1 ? 'info' : activeStep > 1 ? 'success' : 'pending'}
                isCurrent
                description="This is the second thing to happen"
                id="basic-desc-step2"
                titleId="basic-desc-step2-title"
                aria-label="step with info"
                >
                Second step
                </ProgressStep>
                <ProgressStep
                variant={activeStep === 2 ? 'info' : activeStep > 2 ? 'success' : 'pending'}
                description="This is the last thing to happen"
                id="basic-desc-step3"
                titleId="basic-desc-step3-title"
                aria-label="pending step"
                >
                Third step
                </ProgressStep>
            </ProgressStepper>
        </PageSection>
      </React.Fragment> 
    );
};