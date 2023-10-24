import { useTemplateContext } from "@app/context/TemplateProvider";
import { Card, DescriptionList, DescriptionListDescription, DescriptionListTerm, PageSection, PageSectionVariants, Text, TextContent } from "@patternfly/react-core";
import React from "react";

export const Review: React.FunctionComponent = () => {

    const { id, name, description, version, fileName, dynamicVariables} = useTemplateContext();

    return (
        <React.Fragment>
            <PageSection variant={PageSectionVariants.light}>
                <TextContent>
                    <Text component="h3">Review & Submit</Text>
                    <Text component="p">Validate the values and submit</Text>
                </TextContent>
            </PageSection>
            <DescriptionList columnModifier={{ lg: '2Col' }}>
                <Card component="div">
                    <DescriptionListTerm>Tempalte Id</DescriptionListTerm>
                    <DescriptionListDescription>{id}</DescriptionListDescription>
                </Card>
                <Card component="div">
                    <DescriptionListTerm>Tempalte Name</DescriptionListTerm>
                    <DescriptionListDescription>
                        {name}
                    </DescriptionListDescription>
                </Card>
                <Card component="div">
                    <DescriptionListTerm>Template Description</DescriptionListTerm>
                    <DescriptionListDescription>{description}</DescriptionListDescription>
                </Card>
                <Card component="div">
                    <DescriptionListTerm>Vesion</DescriptionListTerm>
                    <DescriptionListDescription>
                        {version}
                    </DescriptionListDescription>
                </Card>
                <Card component="div">
                    <DescriptionListTerm>File Name</DescriptionListTerm>
                    <DescriptionListDescription>
                        {fileName}
                    </DescriptionListDescription>
                </Card>
        </DescriptionList>
      </React.Fragment>
    );
}