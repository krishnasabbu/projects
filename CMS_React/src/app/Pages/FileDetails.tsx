import React from "react";
import { FileUpload, FormHelperText, HelperText, HelperTextItem, PageSection, PageSectionVariants, Text, TextContent } from "@patternfly/react-core";
import FileViewer from 'react-file-viewer';
import mammoth from 'mammoth';
import { useTemplateContext } from "@app/context/TemplateProvider";

export const FileDetails: React.FunctionComponent = () => {

    const [value, setValue] = React.useState<File>();
    const [filename, setFilename] = React.useState('');
    const [isRejected, setIsRejected] = React.useState(false);
    const [htmlContent, setHtmlContent] = React.useState<string>('');

    const { fileName, updateFileName, file, setFile } = useTemplateContext();

    const handleFileInputChange = async (_, file: File) => {
      if (file && file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        setIsRejected(false);
        setValue(file);
        setFile(file);
        setFilename(file.name);
        updateFileName(file.name);
        readDocFile(file);
      } else {
        setFilename(file.name);
        setValue(undefined);
        setIsRejected(true);
      }
    };

    const readDocFile = (file) => {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const arrayBuffer = e.target?.result as ArrayBuffer;
        try {
          const result = await mammoth.convertToHtml({ arrayBuffer });
          console.log("value =============== "+result.value);
          setHtmlContent(result.value);
        } catch (error) {
          console.error('Error converting DOCX to HTML:', error);
        }
      };

      reader.readAsArrayBuffer(file);
    }

    const handleClear = (_event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
      setFilename('');
      setValue(undefined);
      setIsRejected(false);
    };

    return (
      <React.Fragment>
        <PageSection variant={PageSectionVariants.light}>
          <TextContent>
              <Text component="h3">Uplaod Functional Requirement Document (FRD)</Text>
              <Text component="p">This is a demo that showcases PatternFly cards.</Text>
          </TextContent>
        </PageSection>
        <PageSection variant={PageSectionVariants.light}>
          <FileUpload
            id="customized-preview-file"
            value={value}
            filename={filename}
            filenamePlaceholder="Drag and drop a file or upload one"
            onFileInputChange={handleFileInputChange}
            onClearClick={handleClear}
            browseButtonText="Upload"
            accept=".docx"
          >
            <FormHelperText>
              <HelperText>
                <HelperTextItem variant={isRejected ? "error" : "default"}>
                  {isRejected && "Must be a docx file"}
                </HelperTextItem>
              </HelperText>
            </FormHelperText>
          </FileUpload>
        </PageSection>
        <PageSection variant={PageSectionVariants.light}>
            {value && (
              <div className="pf-v5-u-m-md">
                <FileViewer fileType="docx" filePath={URL.createObjectURL(value)} />
              </div>
            )}
            {/* <div dangerouslySetInnerHTML={{ __html: htmlContent }} /> */}
        </PageSection>
      </React.Fragment>
    );
};