import * as React from 'react';
import { Badge, Bullseye, Button, Card, CardBody, CardHeader, CardTitle, Dropdown, DropdownItem, DropdownList, EmptyState, EmptyStateActions, EmptyStateFooter, EmptyStateHeader, EmptyStateIcon, EmptyStateVariant, Gallery, MenuToggle, MenuToggleCheckbox, MenuToggleElement, NavItem, OverflowMenu, OverflowMenuControl, OverflowMenuDropdownItem, OverflowMenuItem, PageSection, PageSectionVariants, Pagination, Select, SelectList, SelectOption, Text, TextContent, Title, Toolbar, ToolbarContent, ToolbarFilter, ToolbarItem } from '@patternfly/react-core';
import { data } from './ProjectData.jsx';
import { EllipsisVIcon, EyeIcon, PlusCircleIcon, TrashIcon } from '@patternfly/react-icons';
import { NavLink } from 'react-router-dom';

const Dashboard: React.FunctionComponent = () => {
  const totalItemCount = data.length;

  const [cardData, setCardData] = React.useState(data);
  const [selectedItems, setSelectedItems] = React.useState<number[]>([]);
  const [isLowerToolbarDropdownOpen, setIsLowerToolbarDropdownOpen] = React.useState(false);
  const [page, setPage] = React.useState(1);
  const [perPage, setPerPage] = React.useState(10);
  const [filters, setFilters] = React.useState<Record<string, string[]>>({ products: [] });
  const [state, setState] = React.useState({});

  interface ProductType {
    id: number;
    name: string;
    icon: string;
    description: string;
    status: string;
  }
  
  const onToolbarDropdownToggle = () => {
    setIsLowerToolbarDropdownOpen(!isLowerToolbarDropdownOpen);
  };

  const onCardKebabDropdownToggle = (
    event: React.MouseEvent<HTMLButtonElement, MouseEvent> | React.MouseEvent<HTMLDivElement, MouseEvent>,
    key: string
  ) => {
    setState({
      [key]: !state[key as keyof Object]
    });
  };

  const deleteItem = (item: ProductType) => {
    const filter = (getter) => (val) => getter(val) !== item.id;

    setCardData(cardData.filter(filter(({ id }) => id)));

    setSelectedItems(selectedItems.filter(filter((id) => id)));
  };

  const onSetPage = (_event: any, pageNumber: number) => {
    setPage(pageNumber);
  };

  const onPerPageSelect = (_event: any, perPage: number) => {
    setPerPage(perPage);
    setPage(1);
  };

  const onNameSelect = (event: any, selection = '') => {
    const checked = event.target.checked;
    const prevSelections = filters.products;

    console.log("checked === "+event.target.checked);
    console.log("selection === "+selection);
    console.log("selection === "+JSON.stringify(prevSelections));

    setFilters({
      ...filters,
      products: checked ? [...prevSelections, selection] : prevSelections.filter(
        (value) => value !== selection)
    });
  };

  const onDelete = (type = '', _id = '') => {
    if (type) {
      setFilters(filters);
    } else {
      setFilters({ products: [] });
    }
  };

  const renderPagination = () => {
    const defaultPerPageOptions = [
      {
        title: '1',
        value: 1
      },
      {
        title: '5',
        value: 5
      },
      {
        title: '10',
        value: 10
      }
    ];

    return (
      <Pagination
        itemCount={totalItemCount}
        page={page}
        perPage={perPage}
        perPageOptions={defaultPerPageOptions}
        onSetPage={onSetPage}
        onPerPageSelect={onPerPageSelect}
        variant="top"
        isCompact
      />
    );
  };

  const buildFilterDropdown = () => {
    const filterDropdownItems = (
      <SelectList>
        <SelectOption
          hasCheckbox
          key="Active"
          value="Active"
          isSelected={filters.products.includes('Active')}
        >
          Active
        </SelectOption>
        <SelectOption hasCheckbox key="In-Active" value="In-Active" isSelected={filters.products.includes('In-Active')}>
          In-Active
        </SelectOption>
      </SelectList>
    );

    return (
      <ToolbarFilter
        categoryName="Products"
        chips={filters.products}
        deleteChip={(type, id) => onDelete(type as string, id as string)}
      >
        <Select
          aria-label="Products"
          role="menu"
          toggle={(toggleRef) => (
            <MenuToggle ref={toggleRef} onClick={onToolbarDropdownToggle} isExpanded={isLowerToolbarDropdownOpen}>
              Filter by Status
              {filters.products.length > 0 && <Badge isRead>{filters.products.length}</Badge>}
            </MenuToggle>
          )}
          onSelect={(event, value) => onNameSelect(event, value.toString())}
          onOpenChange={(isOpen) => {
            setIsLowerToolbarDropdownOpen(isOpen);
          }}
          selected={filters.products}
          isOpen={isLowerToolbarDropdownOpen}
        >
          {filterDropdownItems}
        </Select>
      </ToolbarFilter>
    );
  };

  const toolbarItems = (
    <React.Fragment>
      <ToolbarItem>{buildFilterDropdown()}</ToolbarItem>
      <ToolbarItem variant="pagination" align={{ default: 'alignRight' }}>
        {renderPagination()}
      </ToolbarItem>
    </React.Fragment>
  );

  const filtered =
    filters.products.length > 0
      ? data.filter((card: { status: string }) => filters.products.length === 0 || filters.products.includes(card.status))
      : cardData.slice((page - 1) * perPage, perPage === 1 ? page * perPage : page * perPage - 1);

  return (
    <React.Fragment>
        <PageSection variant={PageSectionVariants.light}>
          <TextContent>
            <Text component="h1">Projects</Text>
            <Text component="p">This is a demo that showcases PatternFly cards.</Text>
          </TextContent>
          <Toolbar id="toolbar-group-types" clearAllFilters={onDelete}>
            <ToolbarContent>{toolbarItems}</ToolbarContent>
          </Toolbar>
        </PageSection>
        <PageSection isFilled>
          <Gallery hasGutter aria-label="Selectable card container">
            <Card isCompact>
              <Bullseye>
                <EmptyState variant={EmptyStateVariant.xs}>
                  <EmptyStateHeader
                    headingLevel="h2"
                    titleText="Add a new card to your page"
                    icon={<EmptyStateIcon icon={PlusCircleIcon} />}
                  />
                  <EmptyStateFooter>
                    <EmptyStateActions>
                      <NavLink to="/template">
                        <Button variant="link">Add card</Button>
                      </NavLink>
                    </EmptyStateActions>
                  </EmptyStateFooter>
                </EmptyState>
              </Bullseye>
            </Card>
            {filtered.map((product, key) => (
              <Card isCompact isClickable isSelectable key={product.name} id={product.name.replace(/ /g, '-')}>
                <CardHeader
                  actions={{
                    actions: (
                      <>
                        <Dropdown
                          isOpen={!!state[key] ?? false}
                          onOpenChange={(isOpen) => setState({ [key]: isOpen })}
                          toggle={(toggleRef: React.Ref<MenuToggleElement>) => (
                            <MenuToggle
                              ref={toggleRef}
                              aria-label={`${product.name} actions`}
                              variant="plain"
                              onClick={(e) => {
                                onCardKebabDropdownToggle(e, key.toString());
                              }}
                              isExpanded={!!state[key]}
                            >
                              <EllipsisVIcon />
                            </MenuToggle>
                          )}
                          popperProps={{ position: 'right' }}
                        >
                          <DropdownList>
                            <DropdownItem
                              key="trash"
                              onClick={() => {
                                deleteItem(product);
                              }}
                            >
                              <EyeIcon />
                              View
                            </DropdownItem>
                            <DropdownItem
                              key="trash"
                              onClick={() => {
                                deleteItem(product);
                              }}
                            >
                              <TrashIcon />
                              Delete
                            </DropdownItem>
                            
                          </DropdownList>
                        </Dropdown>
                      </>
                    )
                  }}
                >
                  {/* <img src={icons[product.icon]} alt={`${product.name} icon`} style={{ maxWidth: '60px' }} /> */}
                </CardHeader>
                <CardTitle>{product.name}</CardTitle>
                <CardBody>{product.description}</CardBody>
              </Card>
            ))}
          </Gallery>
        </PageSection>
        <PageSection
          isFilled={false}
          stickyOnBreakpoint={{ default: 'bottom' }}
          padding={{ default: 'noPadding' }}
          variant="light"
        >
          <Pagination
            itemCount={totalItemCount}
            page={page}
            perPage={perPage}
            onPerPageSelect={onPerPageSelect}
            onSetPage={onSetPage}
            variant="bottom"
          />
        </PageSection>
    </React.Fragment>
  );
}

export { Dashboard };