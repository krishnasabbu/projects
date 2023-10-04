package com.chat.model;

import java.io.Serializable;

public class GitFile implements Serializable {
    private static final long serialVersionUID = 1L;
    private String filename;
    private String patch;

    private String raw_url;

    public String getFilename() {
        return filename;
    }

    public void setFilename(String filename) {
        this.filename = filename;
    }

    public String getPatch() {
        return patch;
    }

    public void setPatch(String patch) {
        this.patch = patch;
    }

    public String getRaw_url() {
        return raw_url;
    }

    public void setRaw_url(String raw_url) {
        this.raw_url = raw_url;
    }
}
