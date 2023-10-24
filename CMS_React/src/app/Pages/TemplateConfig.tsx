// DragAndDropTable.tsx
import React, { useEffect } from 'react';
import { Table, Caption, Thead, Tr, Th, Tbody, Td } from '@patternfly/react-table';
import { Card, CardBody, Chip, ChipGroup, DataList, DataListCell, DataListControl, DataListDragButton, DataListItem, DataListItemCells, DataListItemRow, DragDrop, Draggable, Droppable, Grid, GridItem, PageSection, PageSectionVariants, Text, TextContent, getUniqueId } from '@patternfly/react-core';
import { useTemplateContext } from '@app/context/TemplateProvider';

interface DynamicVariable {
    id: string,
    name: string;
    formatter: string;
    formula: string;
}

type Formatter = {
    id: string;
    name: string;
    formula: string;
    description: string;
};

export const TemplateConfig: React.FC = () => {
    const [ dragOver, setDragOver ] = React.useState(false); 
    const handleDragOverStart = () => setDragOver(true);
    const handleDragOverEnd = () => {
        setDragOver(false);
    }
    const {dynamicVariables, setDynamicVariables} = useTemplateContext();

    const formatterArray: Formatter[] = [
        { id: "1", name: "Date Formatter", formula: "", description: "" },
        { id: "2", name: "Currency Formatter", formula: "", description: "" }
    ];
    
    const handleDragStart = (event: React.DragEvent<HTMLDivElement>) => {
        event.dataTransfer.setData('text', event.currentTarget.id);
    }
    
    const enableDropping = (event: React.DragEvent<HTMLDivElement>) => { 
        event.preventDefault();
    }
        
    const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
        const targetElement = event.currentTarget;
        const id = event.dataTransfer.getData('text');
        targetElement.innerHTML = '<span class="pf-v5-c-chip__content"><span class="pf-v5-c-chip__text" id="1">'+id+'</span></span><span class="pf-v5-c-chip__actions"><button id="remove_1" aria-labelledby="remove_1 1" aria-disabled="false" aria-label="close" class="pf-v5-c-button pf-m-plain" type="button" data-ouia-component-type="PF5/Button" data-ouia-safe="true" data-ouia-component-id="close"><svg class="pf-v5-svg" viewBox="0 0 352 512" fill="currentColor" aria-hidden="true" role="img" width="1em" height="1em"><path d="M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z"></path></svg></button></span>';
        setDragOver(false);
        const formatter = findElementByValue(id);
        updateObject(targetElement.id, formatter?.name, formatter?.formula );
    }

    const findElementByValue = (valueToFind) => {
        return formatterArray.find((item) => item.name === valueToFind);
    };

    const updateObject = (id, newFormatter, newFormula) => {
        console.log("id ========= "+id);
        dynamicVariables.map((item) => (item.id === id ? { ...item, formatter: newFormatter, formula: newFormula } : item));
        const updatedData = dynamicVariables.map((item) =>
            item.id === id ? { ...item, formatter: newFormatter, formula: newFormula } : item
        );
        setDynamicVariables(updatedData);
        console.log(updatedData);
    };

    const deleteChip = (event: React.MouseEvent<Element, MouseEvent>) => {
        const targetElement = event.currentTarget;
        console.log("id==== "+targetElement.id);
        updateObject(targetElement.id, '', '');
        targetElement.innerHTML = '<span class="pf-v5-c-chip__content"><span class="pf-v5-c-chip__text" id="1">Drag Zone</span></span><span class="pf-v5-c-chip__actions"><button id="remove_1" aria-labelledby="remove_1 1" aria-disabled="false" aria-label="close" class="pf-v5-c-button pf-m-plain" type="button" data-ouia-component-type="PF5/Button" data-ouia-safe="true" data-ouia-component-id="close"><svg class="pf-v5-svg" viewBox="0 0 352 512" fill="currentColor" aria-hidden="true" role="img" width="1em" height="1em"><path d="M242.72 256l100.07-100.07c12.28-12.28 12.28-32.19 0-44.48l-22.24-22.24c-12.28-12.28-32.19-12.28-44.48 0L176 189.28 75.93 89.21c-12.28-12.28-32.19-12.28-44.48 0L9.21 111.45c-12.28 12.28-12.28 32.19 0 44.48L109.28 256 9.21 356.07c-12.28 12.28-12.28 32.19 0 44.48l22.24 22.24c12.28 12.28 32.2 12.28 44.48 0L176 322.72l100.07 100.07c12.28 12.28 32.2 12.28 44.48 0l22.24-22.24c12.28-12.28 12.28-32.19 0-44.48L242.72 256z"></path></svg></button></span>';
    }
      
    const uniqueId = getUniqueId();

    return (
        <React.Fragment>
            <PageSection variant={PageSectionVariants.light}>
                <TextContent>
                    <Text component="h3">Dynamic Variables Configuration</Text>
                    <Text component="p">Drag and Drop the formatter to the corresponding column</Text>
                </TextContent>
            </PageSection>
            <PageSection variant={PageSectionVariants.light}>
                <Card>
                    <CardBody>
                        <Grid>
                            <GridItem span={6}>
                                <Table aria-label="Simple table">
                                    <Caption>Dynamic Variables</Caption>
                                    <Thead>
                                        <Tr>
                                            <Th>Name</Th>
                                            <Th>Formatter</Th>
                                        </Tr>
                                    </Thead>
                                    <Tbody>
                                        {dynamicVariables.map((repo) => (
                                            <Tr key={repo.id}>
                                                <Td>{repo.name}</Td>
                                                <Td>
                                                    <ChipGroup>
                                                        <Chip id={repo.id}
                                                              key={`dropElement${repo.id}`}
                                                              onClick={deleteChip}
                                                              onDragOver={enableDropping}
                                                              onDrop={handleDrop}
                                                              onDragEnter={handleDragOverStart}
                                                              onDragLeave={handleDragOverEnd}>
                                                            {repo.formatter}
                                                        </Chip>
                                                    </ChipGroup>
                                                </Td>
                                            </Tr>
                                        ))}
                                    </Tbody>
                                </Table>
                            </GridItem>
                            <GridItem span={2}>

                            </GridItem>
                            <GridItem span={4}>
                                <Table aria-label="Simple table" variant='compact'>
                                    <Caption>Formatters</Caption>
                                    <Tbody>
                                        {formatterArray.map(({ id, name, description, formula }) => (
                                            <Tr key={id}>
                                                <Td>
                                                    <div id={name} draggable="true" onDragStart={handleDragStart}>
                                                        <DataListItem aria-labelledby={`draggable-${id}`}>
                                                            <DataListItemRow>
                                                                <DataListControl>
                                                                    <DataListDragButton
                                                                    aria-label="Reorder"
                                                                    aria-labelledby={`draggable-${id}`}
                                                                    aria-describedby={`description-${uniqueId}`}
                                                                    aria-pressed="false"
                                                                    />
                                                                </DataListControl>
                                                                <DataListItemCells
                                                                    dataListCells={[
                                                                    <DataListCell key={id}>
                                                                        <span id={name}>
                                                                            {name}
                                                                        </span>
                                                                    </DataListCell>
                                                                    ]}
                                                                />
                                                            </DataListItemRow>
                                                        </DataListItem>
                                                    </div> 
                                                </Td>
                                            </Tr>
                                        ))}
                                    </Tbody>
                                </Table>
                            </GridItem>
                        </Grid>
                    </CardBody>
                </Card>
            </PageSection>   
        </React.Fragment>  
    );
};
