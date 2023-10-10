package com.chat.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class TranslateCriteria {

    @JsonProperty(value = "data")
    private String text;
    private String status;
    private String error;
    private String targetLng = "ES";

    private String detectedSourceLanguage;

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getTargetLng() {
        return targetLng;
    }

    public void setTargetLng(String targetLng) {
        this.targetLng = targetLng;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public String getDetectedSourceLanguage() {
        return detectedSourceLanguage;
    }

    public void setDetectedSourceLanguage(String detectedSourceLanguage) {
        this.detectedSourceLanguage = detectedSourceLanguage;
    }
}