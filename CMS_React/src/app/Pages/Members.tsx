import React from 'react';
import { Button, MenuToggle, PageSection, PageSectionVariants, Text, TextContent, ToggleGroup, ToggleGroupItem, ToggleGroupItemProps } from '@patternfly/react-core';
import {
  Table,
  TableText,
  Thead,
  Tr,
  Th,
  Tbody,
  Td,
  ActionsColumn,
  IAction
} from '@patternfly/react-table';
import { useTemplateContext } from '@app/context/TemplateProvider';
import { User } from '@app/utils/type';

export const Members: React.FunctionComponent = () => {
  // In real usage, this data would come from some external source like an API via props.
  const { users, setUsers } = useTemplateContext();

  const defaultActions = (repo: User): IAction[] => [
    {
      title: 'Assign Role',
      onClick: () => console.log(`clicked on Some action`)
    }
  ];

  return (
    <React.Fragment>
      <PageSection variant={PageSectionVariants.light}>
          <TextContent>
              <Text component="h1">Members List</Text>
          </TextContent>
      </PageSection>
      <PageSection variant={PageSectionVariants.light}>
        <Table aria-label="Actions table">
          <Thead>
            <Tr>
              <Th>Id</Th>
              <Th>Name</Th>
              <Th>User Name</Th>
              <Th>Email</Th>
              <Td></Td>
            </Tr>
          </Thead>
          <Tbody>
            {users.map((user) => {
              // Arbitrary logic to determine which rows get which actions in this example
              let rowActions: IAction[] | null = defaultActions(user);
              return (
                <Tr key={user.id}>
                  <Td dataLabel={user.id}>{user.id}</Td>
                  <Td dataLabel={user.name}>{user.name}</Td>
                  <Td dataLabel={user.userName}>{user.userName}</Td>
                  <Td dataLabel={user.email}>{user.email}</Td>
                  <Td isActionCell>
                    {rowActions ? (
                      <ActionsColumn
                        items={rowActions}
                      />
                    ) : null}
                  </Td>
                </Tr>
              );
            })}
          </Tbody>
        </Table>
      </PageSection>
    </React.Fragment>
  );
};