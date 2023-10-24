import React from "react";
import { Tabs, Tab, TabTitleText, TabTitleIcon, PageSection, PageSectionVariants, TextContent, Text, Button } from '@patternfly/react-core';
import UsersIcon from '@patternfly/react-icons/dist/esm/icons/users-icon';
import BoxIcon from '@patternfly/react-icons/dist/esm/icons/box-icon';
import DatabaseIcon from '@patternfly/react-icons/dist/esm/icons/database-icon';
import ServerIcon from '@patternfly/react-icons/dist/esm/icons/server-icon';
import LaptopIcon from '@patternfly/react-icons/dist/esm/icons/laptop-icon';
import ProjectDiagramIcon from '@patternfly/react-icons/dist/esm/icons/project-diagram-icon';
import { ApplicationsIcon, CogIcon, CropIcon, ForumbeeIcon, KeyIconConfig, Page4Icon, Page4IconConfig, UploadIcon } from "@patternfly/react-icons";
import { TemplateForm } from "./TemplateForm";
import { FileDetails } from "./FileDetails";
import { TemplateProgress } from "./TemplateProgress";
import {TemplateConfig} from "./TemplateConfig";
import { Document } from "./Model";
import { Review } from "./Review";
import { useHistory } from 'react-router-dom';


export const Template: React.FunctionComponent = () => {
    const [activeTabKey, setActiveTabKey] = React.useState<number>(0);
    const [backButton, setBackButton] = React.useState<Boolean>(false);
    const [showNext, setShowNext] = React.useState<Boolean>(true);
    const [showSubmit, setShowSubmit] = React.useState<Boolean>(false);

    const history = useHistory();

    const handleClick = () => {
        const currentKey = activeTabKey + 1;
        setActiveTabKey(activeTabKey + 1);
        if(currentKey > 0) {
            setBackButton(true);
        }
        updateButtons(currentKey);
        console.log("active Key === "+activeTabKey);
    };

    const handleBackClick = () => {
        console.log("key === "+activeTabKey)
        const currentKey = activeTabKey - 1;
        updateButtons(currentKey);
        setActiveTabKey(activeTabKey - 1);
        if(currentKey < 1) {
            setBackButton(false);
        }
    }

    const updateButtons = (key) => {
        if(key === 3) {
            setShowNext(false);
            setShowSubmit(true);
        }else {
            setShowNext(true);
            setShowSubmit(false);
        }
    }

    const handleSubmit = () => {
        history.push('/submit');
    }

    return (
        <React.Fragment>
            <PageSection variant={PageSectionVariants.light}>
                <TextContent>
                    <Text component="h1">Create Template</Text>
                    <Text component="p">This is a demo that showcases PatternFly cards.</Text>
                </TextContent>
            </PageSection>
            <PageSection>
                <Tabs
                    activeKey={activeTabKey}
                    aria-label="Tabs in the icons and text example"
                    role="region"
                    >
                    <Tab
                        eventKey={0}
                        title={
                        <>
                            <TabTitleIcon>
                                <ApplicationsIcon />
                            </TabTitleIcon>{' '}
                            <TabTitleText>Tempalte Details</TabTitleText>{' '}
                        </>
                        }
                        aria-label="icons and text content"
                    >
                        <TemplateForm></TemplateForm>
                    </Tab>
                    <Tab
                        eventKey={1}
                        title={
                        <>
                            <TabTitleIcon>
                            <UploadIcon />
                            </TabTitleIcon>{' '}
                            <TabTitleText>FRD</TabTitleText>{' '}
                        </>
                        }
                    >
                        <FileDetails></FileDetails>
                    </Tab>
                    <Tab
                        eventKey={2}
                        title={
                        <>
                            <TabTitleIcon>
                            <CogIcon />
                            </TabTitleIcon>{' '}
                            <TabTitleText>Configuration</TabTitleText>{' '}
                        </>
                        }
                    >
                        <TemplateConfig></TemplateConfig>
                        
                    </Tab>
                    <Tab
                        eventKey={3}
                        title={
                        <>
                            <TabTitleIcon>
                            <ServerIcon />
                            </TabTitleIcon>{' '}
                            <TabTitleText>Review & Submit</TabTitleText>{' '}
                        </>
                        }
                    >
                        <Review></Review>
                    </Tab>
                    {/* <Tab
                        eventKey={4}
                        title={
                        <>
                            <TabTitleIcon>
                            <LaptopIcon />
                            </TabTitleIcon>{' '}
                            <TabTitleText>System</TabTitleText>{' '}
                        </>
                        }
                    >
                        <TemplateProgress></TemplateProgress>
                    </Tab>
                    <Tab
                        eventKey={5}
                        title={
                        <>
                            <TabTitleIcon>
                            <ProjectDiagramIcon />
                            </TabTitleIcon>{' '}
                            <TabTitleText>Network</TabTitleText>{' '}
                        </>
                        }
                    >
                        Network
                    </Tab> */}
                </Tabs>
            </PageSection>
            <PageSection variant={PageSectionVariants.light}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', float: 'right' }}>
                    <div>
                        {backButton && <Button variant="secondary" onClick={handleBackClick} >Back</Button> }
                        &nbsp;&nbsp;
                        { showNext && <Button variant="primary" onClick={handleClick}>Next</Button>}
                        { showSubmit && <Button variant="primary" onClick={handleSubmit}>Submit</Button>}
                    </div>
                </div>
            </PageSection>
        </React.Fragment>
    );
};