import React, { useState } from 'react';
import {
  Card,
  CardBody,
  Button,
  Page,
  PageSection,
  Modal,
  Text,
  TextContent,
  TextVariants,
  ModalVariant,
  ButtonVariant,
  Checkbox,
} from '@patternfly/react-core';
import EditIcon from '@patternfly/react-icons/dist/js/icons/edit-icon';
import { Table, Caption, Thead, Tr, Th, Tbody, Td } from '@patternfly/react-table';

interface Role {
  id: number;
  name: string;
}

interface ModulePermission {
  id: number;
  module: string;
  permissions: string[];
}

const rolesData: Role[] = [
  { id: 1, name: 'Admin' },
  { id: 2, name: 'Editor' },
  // Add more roles as needed
];

const modulesPermissionsData: ModulePermission[] = [
  {
    id: 1,
    module: 'Dashboard',
    permissions: ['View', 'Edit'],
  },
  {
    id: 2,
    module: 'Users',
    permissions: ['View', 'Edit', 'Delete'],
  },
  // Add more modules and permissions as needed
];

export const Roles: React.FC = () => {
  const [selectedRole, setSelectedRole] = useState<Role | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSettingsClick = (role: Role) => {
    setSelectedRole(role);
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setSelectedRole(null);
  };

  const renderModulesPermissionsGrid = () => {
    const selectedRoleData = modulesPermissionsData.find((data) => data.id === selectedRole?.id);

    if (!selectedRoleData) {
      return null;
    }

    return (
      <Table
        aria-label="Simple table"
        variant='compact'
      >
        <Caption>Roles and Permission Assign page</Caption>
        <Thead>
          <Tr>
            <Th></Th>
            <Th>View</Th>
            <Th>Create</Th>
            <Th>Update</Th>
            <Th>Delete</Th>
          </Tr>
        </Thead>
        <Tbody>
            <Tr>
              <Td>Users</Td>
              <Td><Checkbox id=''></Checkbox></Td>
              <Td><Checkbox id=''></Checkbox></Td>
              <Td><Checkbox id=''></Checkbox></Td>
              <Td><Checkbox id=''></Checkbox></Td>
            </Tr>
        </Tbody>
      </Table>
    );
  };

  return (
    <Page>
      <PageSection>
        {rolesData.map((role) => (
          <Card key={role.id} style={{ marginBottom: '16px' }}>
            <CardBody>
              <TextContent>
                <Text component={TextVariants.h3}>{role.name}</Text>
              </TextContent>
              <Button
                variant={ButtonVariant.link}
                onClick={() => handleSettingsClick(role)}
                icon={<EditIcon />}
              >
                Settings
              </Button>
            </CardBody>
          </Card>
        ))}
      </PageSection>

      <Modal
        variant={ModalVariant.medium}
        title={`Settings for ${selectedRole?.name || ''}`}
        isOpen={isModalOpen}
        onClose={handleModalClose}
        actions={[
          <Button key="confirm" variant={ButtonVariant.primary} onClick={handleModalClose}>
            Close
          </Button>,
        ]}
      >
        {renderModulesPermissionsGrid()}
      </Modal>
    </Page>
  );
};
