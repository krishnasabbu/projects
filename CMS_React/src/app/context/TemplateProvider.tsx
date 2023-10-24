import { DynamicVariables } from "@app/utils/type";
import React, { PropsWithChildren } from "react";

interface TemplateContextData {
    id: string;
    name: string;
    description: string;
    version: string;
    fileName: string;
    content: string;
    file: File | null;
    dynamicVariables: DynamicVariables;
    updateId: (newId: string) => void;
    updateName: (newName: string) => void;
    updateDescription: (newDescription: string) => void;
    updateVersion: (newVersion: string) => void;
    updateFileName: (newFileName: string) => void;
    updateContent: (newContent: string) => void;
    setFile: (newFile: File | null) => void;
    setDynamicVariables: (newDynamicVariables: DynamicVariables) => void;
    createTemplate: () => void;
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

    const contextValue: TemplateContextData = {
        id,
        name,
        description,
        version,
        fileName,
        content,
        file,
        dynamicVariables,
        updateId,
        updateName,
        updateDescription,
        updateVersion,
        updateFileName,
        updateContent,
        setFile,
        setDynamicVariables,
        createTemplate
    };

    return(
        <TemplateContext.Provider value={contextValue}>{children}</TemplateContext.Provider>
    );
};

export const useTemplateContext = () => React.useContext(TemplateContext);