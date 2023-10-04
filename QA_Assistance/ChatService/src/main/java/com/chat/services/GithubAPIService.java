package com.chat.services;

import com.chat.model.GitFile;
import com.chat.model.ReviewCommentRequest;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
public class GithubAPIService {

    @Autowired
    RestTemplate restTemplate;

    @Autowired
    ChatService chatService;

    private static final String X_GitHub_Api_Version_KEY = "X-GitHub-Api-Version";
    private static final String X_GitHub_Api_Version_VALUE = "2022-11-28";
    private static final String AUTHORIZATION_KEY = "Authorization";
    //private static final String AUTHORIZATION_VALUE = "Bearer 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";
    private static final String AUTHORIZATION_VALUE = "Bearer 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";

    private static final String URL = "%s/files";

    private static final String COMMENT_CONTENT = "%s " +
            "%s";

    public void getPRDiff(String content) {

    }

    public void reviewChangesAndPostComment(String payload) {
        JSONObject payloadJson=new JSONObject(payload);

        JSONObject pullRequest = payloadJson
                .getJSONObject("pull_request");

        String commentsUrl = pullRequest
                .getJSONObject("_links")
                .getJSONObject("comments")
                .getString("href");

        //String title = pullRequest.getString("title");
        //String body = pullRequest.getString("body");

        String url = pullRequest.getString("url");

        List<GitFile> files = getFiles(String.format(URL, url));

        StringBuilder sb = new StringBuilder();

        if(files.size() == 1) {
            GitFile gitFile = files.get(0);
            String reviewComments = chatService.reviewChange(this.getContent(gitFile.getRaw_url()));
            sb.append(reviewComments);
        }else if(files.size() > 1) {
            for(GitFile gitFile: files) {
                String reviewComments = chatService.reviewChange(this.getContent(gitFile.getRaw_url()));
                sb.append(String.format(COMMENT_CONTENT, gitFile.getFilename(), reviewComments));
                sb.append("\n");
            }
        }
        this.addPRReviewComment(commentsUrl, sb.toString());
    }

    public List<GitFile> getFiles(String url) {
        List<GitFile> fileList = new ArrayList<>();
        try {
            URI uri = new URI(url);
            ResponseEntity<GitFile[]> response = restTemplate.getForEntity(uri, GitFile[].class);
            fileList = Arrays.asList(response.getBody());
        }catch(Exception e) {
            e.printStackTrace();
        }
        return fileList;
    }

    public String getContent(String url) {

       /* try {
            URI uri = new URI(url);
            ResponseEntity<String> response = restTemplate.getForEntity(uri, String.class);
            return response.getBody();
        }catch(Exception e) {
            e.printStackTrace();
        }*/

        try (CloseableHttpClient httpclient = HttpClients.createDefault()) {

            //HTTP GET method
            HttpGet httpget = new HttpGet(url);
            System.out.println("Executing request " + httpget.getRequestLine());

            // Create a custom response handler
            ResponseHandler< String > responseHandler = response -> {
                int status = response.getStatusLine().getStatusCode();
                if (status >= 200 && status < 300) {
                    org.apache.http.HttpEntity entity = response.getEntity();
                    return entity != null ? EntityUtils.toString(entity) : null;
                } else {
                    throw new ClientProtocolException("Unexpected response status: " + status);
                }
            };
            String responseBody = httpclient.execute(httpget, responseHandler);
            System.out.println("----------------------------------------");
            System.out.println(responseBody);
            return responseBody;
        } catch (ClientProtocolException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public String addPRReviewComment(String commentsUrl, String comment) {
        try {
            System.out.println("comment === "+comment);
            URI uri = new URI(commentsUrl);
            HttpHeaders headers = new HttpHeaders();
            headers.set(X_GitHub_Api_Version_KEY, X_GitHub_Api_Version_VALUE);
            headers.set(AUTHORIZATION_KEY, AUTHORIZATION_VALUE);
            HttpEntity<ReviewCommentRequest> requestEntity = new HttpEntity<>(new ReviewCommentRequest(comment), headers);
            ResponseEntity<String> response = restTemplate.exchange(uri, HttpMethod.POST, requestEntity, String.class);
            return response.getBody();
        } catch (URISyntaxException e) {
            try {
                URI uri = new URI(commentsUrl);
                HttpHeaders headers = new HttpHeaders();
                headers.set(X_GitHub_Api_Version_KEY, X_GitHub_Api_Version_VALUE);
                headers.set(AUTHORIZATION_KEY, AUTHORIZATION_VALUE);
                HttpEntity<ReviewCommentRequest> requestEntity = new HttpEntity<>(new ReviewCommentRequest(comment), headers);
                ResponseEntity<String> response = restTemplate.exchange(uri, HttpMethod.POST, requestEntity, String.class);
                return response.getBody();
            }catch (URISyntaxException e1) {
                e1.printStackTrace();
            }
        }
        return null;
    }
}
