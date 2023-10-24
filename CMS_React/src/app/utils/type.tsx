export interface Template {
    id: string;
    name: string;
    description: string;
    version: string;
    filename: string;
    content: string;
    status: string;
    dynamicVariables: DynamicVariables
}

export interface DynamicVariable {
    id:string;
    name:string;
    formatter:string;
    formula:string;
}

export type Templates = Template[];
export type DynamicVariables=DynamicVariable[];