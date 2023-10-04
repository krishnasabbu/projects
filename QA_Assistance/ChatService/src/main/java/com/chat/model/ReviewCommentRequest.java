package com.chat.model;

public class ReviewCommentRequest {

    private String body;

    public ReviewCommentRequest(String body) {
        this.body = body;
    }

    public String getBody() {
        return body;
    }

    public void setBody(String body) {
        this.body = body;
    }
}
