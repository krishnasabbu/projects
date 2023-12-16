import { DynamicVariable, DynamicVariables, Template, Templates, Users } from "@app/utils/type";
import React from "react";

interface TemplateContextData {
    id: string;
    name: string;
    description: string;
    version: string;
    fileName: string;
    content: string;
    file: File | null;
    dynamicVariables: DynamicVariables;
    formDynamicVariables: DynamicVariables;
    templateList: Templates;
    users: Users;
    updateId: (newId: string) => void;
    updateName: (newName: string) => void;
    updateDescription: (newDescription: string) => void;
    updateVersion: (newVersion: string) => void;
    updateFileName: (newFileName: string) => void;
    updateContent: (newContent: string) => void;
    setFile: (newFile: File | null) => void;
    setDynamicVariables: (newDynamicVariables: DynamicVariables) => void;
    setFormDynamicVariables: (newDynamicVariables: DynamicVariables) => void;
    createTemplate: () => void;
    updateTemplates: (newTemplates: Templates) => void;
    updateTemplate: (newTemplate: Template) => void;
    setUsers: (newUsers: Users) => void;
}

const TemplateContext = React.createContext<TemplateContextData | undefined>(undefined);

export default function TemplateProvider ({ children}) {

    const [id, setId] = React.useState('');
    const [name, setName] = React.useState('');
    const [description, setDescription] = React.useState('');
    const [version, setVersion] = React.useState('');
    const [fileName, setFileName] = React.useState('');
    const [content, setContent] = React.useState('');
    const [file, setFile] = React.useState<File | null>(null);
    const [dynamicVariables, setDynamicVariables] = React.useState<DynamicVariables>([
        { id: '1', name: 'one', formatter: 'Drop Zone', formula: '' },
        { id: '2', name: 'two', formatter: 'Drop Zone', formula: '' },
        { id: '3', name: 'three', formatter: 'Drop Zone', formula: ''}
    ]);
    const [templateList, setTemplateList] = React.useState<Templates | []>([]);
    const [formDynamicVariables, setFormDynamicVariables] = React.useState<DynamicVariables>([]);
    const [users, setUsers] = React.useState<Users | []>([
        { id: '1', name: 'one', userName: 'Drop Zone', email: '' },
        { id: '2', name: 'two', userName: 'Drop Zone', email: '' },
        { id: '3', name: 'three', userName: 'Drop Zone', email: ''}
    ]);

    const updateId = (newId : string) => {
        console.log(newId);
        setId(newId);
    }

    const updateName = (newId : string) => {
        setName(newId);
    }

    const updateDescription = (newId : string) => {
        setDescription(newId);
    }

    const updateVersion = (newId : string) => {
        setVersion(newId);
    }

    const updateFileName = (newId : string) => {
        setFileName(newId);
    }

    const updateContent = (newId : string) => {
        setContent(newId);
    }

    const createTemplate = () => {

    }

    const updateTemplates = (templates: Templates) => {
        console.log(JSON.stringify(templates))
        setTemplateList(templates);
        console.log("templateList === "+templateList.length);
    }

    const updateTemplate = (template: Template) => {
        setId(template.id);
        setName(template.name);
        setDescription(template.description);
        setVersion(template.version);
        setFileName(template.filename);
        setDynamicVariables(template.dynamicVariables);
    }

    const contextValue: TemplateContextData = {
        id,
        name,
        description,
        version,
        fileName,
        content,
        file,
        dynamicVariables,
        formDynamicVariables,
        templateList,
        users,
        updateId,
        updateName,
        updateDescription,
        updateVersion,
        updateFileName,
        updateContent,
        setFile,
        setDynamicVariables,
        setFormDynamicVariables,
        createTemplate,
        updateTemplates,
        updateTemplate,
        setUsers,
    };

    return(
        <TemplateContext.Provider value={contextValue}>{children}</TemplateContext.Provider>
    );
};

export const useTemplateContext = () => React.useContext(TemplateContext);