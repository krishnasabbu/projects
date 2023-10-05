package com.chat.model;

import java.io.Serializable;
import java.util.List;

public class GitFiles implements Serializable {
    private static final long serialVersionUID = 1L;
    private List<GitFile> files;

    public List<GitFile> getFiles() {
        return files;
    }

    public void setFiles(List<GitFile> files) {
        this.files = files;
    }
}
