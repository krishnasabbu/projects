import * as React from 'react';
import { useTemplateContext } from '@app/context/TemplateProvider';
import { Badge, Bullseye, Button, Card, CardBody, CardFooter, CardHeader, CardTitle, Dropdown, DropdownItem, DropdownList, EmptyState, EmptyStateActions, EmptyStateFooter, EmptyStateHeader, EmptyStateIcon, EmptyStateVariant, Gallery, MenuToggle, MenuToggleElement, PageSection, PageSectionVariants, Pagination, Select, SelectList, SelectOption, Text, TextContent, Toolbar, ToolbarContent, ToolbarFilter, ToolbarItem } from '@patternfly/react-core';
import { ArrowRightIcon, EllipsisVIcon, EyeIcon, PlusCircleIcon, TrashIcon } from '@patternfly/react-icons';
import { NavLink, useHistory } from 'react-router-dom';
import { APIService } from '@app/utils/APIService';
import { Templates } from '@app/utils/type';

export const Dashboard: React.FunctionComponent = () => {

  const {templateList, updateTemplates, updateTemplate} = useTemplateContext();
  const [totalItemCount, setTotalItemCount] = React.useState(0);

  const [cardData, setCardData] = React.useState<Templates>([]);
  const [selectedItems, setSelectedItems] = React.useState<number[]>([]);
  const [isLowerToolbarDropdownOpen, setIsLowerToolbarDropdownOpen] = React.useState(false);
  const [page, setPage] = React.useState(1);
  const [perPage, setPerPage] = React.useState(10);
  const [filters, setFilters] = React.useState<Record<string, string[]>>({ products: [] });
  const [state, setState] = React.useState({});

  const history = useHistory();

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
    setFilters({
      ...filters,
      products: checked ? [...prevSelections, selection] : prevSelections.filter(
        (value) => value !== selection)
    });
  };

   React.useEffect(() => {
     const fetchTemplates = async () => {
       const data = await APIService.get<Templates>('http://localhost:8081/response');
       console.log(data);
       updateTemplates(data);
       setTotalItemCount(data.length);
       setCardData(data);
     };
     fetchTemplates();
   }, []);

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
        categoryName="Templates"
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

  const viewDetails = (id: string) => {
    const foundObject = templateList.find(obj => obj.id === id);
    console.log("foundObject ===== "+foundObject);
    updateTemplate(foundObject);
    history.push("/template");
  }

  const filtered =
    filters.products.length > 0
      ? templateList.filter((card: { status: string }) => filters.products.length === 0 || filters.products.includes(card.status))
      : cardData.slice((page - 1) * perPage, perPage === 1 ? page * perPage : page * perPage - 1);

  console.log("filtered : "+filtered);

  return (
    <React.Fragment>
        <PageSection variant={PageSectionVariants.light}>
          <TextContent>
            <Text component="h1">Tempaltes</Text>
            <Text component="p">Display list of templates</Text>
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
                    titleText="Add a new Template"
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
            {filtered.map((template, key) => (
              <Card isCompact isClickable isSelectable key={template.name} id={template.name.replace(/ /g, '-')}>
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
                              aria-label={`${template.name} actions`}
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
                                deleteItem(template);
                              }}
                            >
                              <EyeIcon />
                              Edit
                            </DropdownItem>
                            <DropdownItem
                              key="trash"
                              onClick={() => {
                                deleteItem(template);
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
                  {/* <img src={pfIcon} style={{ maxWidth: '60px' }} /> */}
                </CardHeader>
                <CardTitle>{template.name}</CardTitle>
                <CardBody>{template.description}</CardBody>
                <CardFooter>
                  <Button variant="link" onClick={() => viewDetails(template.id)}>
                    View Details
                  </Button>
                </CardFooter>
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