package com.chat.services;

import com.chat.model.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.sourceforge.tess4j.ITesseract;
import net.sourceforge.tess4j.Tesseract;
import net.sourceforge.tess4j.TesseractException;
import net.sourceforge.tess4j.util.LoadLibs;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.parser.Parser;
import org.jsoup.select.Elements;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestTemplate;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.image.RescaleOp;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.io.*;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
public class ChatService {

    @Autowired
    RestTemplate restTemplate;

    @Value("${open.translate.api.url}")
    private String openApiURL;

    @Value("${open.api.key}")
    private String openApiKey;

    private String search = "&q=%s";

    private String AUTHORIZATION = "Bearer %s";

    private String TRANSLATION_TEXT = "Translate this into 1. %s:\\n\\n%s";

    private String CHAT_URL = "http://localhost:5000/chat?q=%s";

    private String VELOCITY_KEY = "value%s";
    private String VELOCITY_FINAL_KEY = "$%s";

    private String BERT_URL = "http://127.0.0.1:5000/api?query=%s";

    private String ANSWER_TEXT = "%s <br/><br/> <b>Please refer the below URL for more info :</b> <br/><br/> <a href='%s' target='_blank'>%s</a>";

    /*private String prompt = "Can you tell me the problems with the following pull request and describe your suggestions? \n"+
            "title: %s \n"+
            "body: %s \n"+
            "The following diff is the changes made in this PR. \n"+
            "%s";*/

    //private String prompt = "show me errors in the below code and highlight the error code with underline? \n" +
    //private String prompt = "compile below javascript code and show me errors and highlight the error code with underline? \n" +
    private String prompt = "compile below javascript code and show me errors and provide suggestions? \n" +
            "%s";

    private String DL_PROMPT = "Parse the below text and reply the details in JSON format, don't create any sub objects \n %s";

    private String ANSWER_PROMPT = "Provide a one-word answer to the following question \n %s";


    public String reviewChange(String content) {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Authorization", String.format(AUTHORIZATION, openApiKey));
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));

        OpenApiRequest openApiRequest = new OpenApiRequest();
        openApiRequest.setPrompt(String.format(prompt, content));

        HttpEntity<OpenApiRequest> request =
                new HttpEntity<OpenApiRequest>(openApiRequest, headers);
        System.out.println("URL ======= "+openApiURL);
        OpenApiResponse response = restTemplate.postForObject(openApiURL, request, OpenApiResponse.class);
        if(Objects.nonNull(response) && !CollectionUtils.isEmpty(response.getChoices())) {
            for(Choices choice: response.getChoices()) {
                System.out.println("Response === "+ response);
                return choice.getText();
            }
        }
        return "";
    }

    public TranslateCriteria getAnswerByBert(TranslateCriteria translateCriteria) {
        HttpHeaders headers = new HttpHeaders();
        OpenApiRequest openApiRequest = new OpenApiRequest();
        openApiRequest.setPrompt(translateCriteria.getText());
        HttpEntity<OpenApiRequest> request =
                new HttpEntity<OpenApiRequest>(openApiRequest, headers);
        System.out.println("URL ======= "+CHAT_URL);
        Map<String, String> response = restTemplate.getForObject(String.format(CHAT_URL, translateCriteria.getText()),
                Map.class);
        if(Objects.nonNull(response)) {
            String title = response.get("title");
            String answer = String.format(ANSWER_TEXT, response.get("answer"), title, title);
            translateCriteria.setText(answer.replaceAll("TITLE_URL", title));
        }
        return translateCriteria;
    }

    public TranslateCriteria getAnswer(TranslateCriteria translateCriteria) {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Authorization", String.format(AUTHORIZATION, openApiKey));
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
        OpenApiRequest openApiRequest = new OpenApiRequest();
        String prompt = String.format(ANSWER_PROMPT, translateCriteria.getText());
        System.out.println(prompt);
        openApiRequest.setPrompt(prompt);
        HttpEntity<OpenApiRequest> request =
                new HttpEntity<OpenApiRequest>(openApiRequest, headers);
        System.out.println("URL ======= "+openApiURL);
        OpenApiResponse response = restTemplate.postForObject(openApiURL, request, OpenApiResponse.class);
        if(Objects.nonNull(response) && !CollectionUtils.isEmpty(response.getChoices())) {
            for(Choices choice: response.getChoices()) {
                System.out.println(choice.getText());
                String answer = choice.getText().trim();
                translateCriteria.setText(answer);
            }
        }
        return translateCriteria;
    }


    public TranslateCriteria getDLDetails(TranslateCriteria translateCriteria) throws IOException {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Authorization", String.format(AUTHORIZATION, openApiKey));
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
        OpenApiRequest openApiRequest = new OpenApiRequest();
        String prompt = String.format(DL_PROMPT, translateCriteria.getText());
        System.out.println(prompt);
        openApiRequest.setPrompt(String.format(DL_PROMPT, translateCriteria.getText()));
        HttpEntity<OpenApiRequest> request =
                new HttpEntity<OpenApiRequest>(openApiRequest, headers);
        System.out.println("URL ======= "+openApiURL);
        OpenApiResponse response = restTemplate.postForObject(openApiURL, request, OpenApiResponse.class);
        if(Objects.nonNull(response) && !CollectionUtils.isEmpty(response.getChoices())) {
            for(Choices choice: response.getChoices()) {
                System.out.println(choice.getText());
                String answer = choice.getText().trim();
                ObjectMapper mapper = new ObjectMapper();
                Map<String, Object> map = mapper.readValue(getJsonFromString(answer), Map.class);
                Map<String, String> finalMap = new HashMap<>();
                this.jsonReplace(finalMap, map);
                translateCriteria.setText(this.createHtml(finalMap));
            }
        }
        return translateCriteria;
    }

    public TranslateCriteria getDLDetails_backup(TranslateCriteria translateCriteria) throws IOException {
        String answer = "{\n" +
                "    \"DriverLicense\": {\n" +
                "        \"Number\": \"ml1234568\",\n" +
                "        \"Class\": \"55 c\",\n" +
                "        \"Expiration\": \"08/31/2014\",\n" +
                "        \"Endorsement\": \"NONE\"\n" +
                "    },\n" +
                "    \"Cardholder\": {\n" +
                "        \"Name\": \"FNIMA\",\n" +
                "        \"Address\": \"2510 24m STREET, ANVTOWN, GA 95818\",\n" +
                "        \"DOB\": \"05/31/1977\",\n" +
                "        \"SSN\": \"NONE\",\n" +
                "        \"Veteran\": \"YES\",\n" +
                "        \"Sex\": \"F\",\n" +
                "        \"Eyes\": \"BRN\",\n" +
                "        \"Hair\": \"CWW\",\n" +
                "        \"Height\": \"5205\",\n" +
                "        \"Weight\": \"125m\",\n" +
                "        \"IssueDate\": \"08/31/2003\"\n" +
                "    }\n" +
                "}";
        ObjectMapper mapper = new ObjectMapper();
        Map<String, Object> map = mapper.readValue(getJsonFromString(answer), Map.class);
        Map<String, String> finalMap = new HashMap<>();
        this.jsonReplace(finalMap, map);
        translateCriteria.setText(this.createHtml(finalMap));
        return translateCriteria;
    }

    private String createHtml(Map<String, String> map) {
        StringBuilder sb = new StringBuilder();
        sb.append("<div>");

        sb.append("<table width='92%' style='margin: 20px;'>");
        for (Map.Entry<String, String> entry : map.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();
            sb.append("<tr><td>").append(key).append("</td><td>").append(value).append("</td></tr>");
        }
        sb.append("</table>");
        sb.append("<div class='quick-links'><div class='quick-link' id='submitCC'><div class='link'>Apply</div></div></div>");
        return sb.toString();
    }

    private TranslateCriteria translateTextByOpenAPI(TranslateCriteria translateCriteria) {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Authorization", String.format(AUTHORIZATION, openApiKey));
        headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
        OpenApiRequest openApiRequest = new OpenApiRequest();
        openApiRequest.setPrompt(translateCriteria.getText());
        HttpEntity<OpenApiRequest> request =
                new HttpEntity<OpenApiRequest>(openApiRequest, headers);
        System.out.println("URL ======= "+openApiURL);
        OpenApiResponse response = restTemplate.postForObject(openApiURL, request, OpenApiResponse.class);
        if(Objects.nonNull(response) && !CollectionUtils.isEmpty(response.getChoices())) {
            for(Choices choice: response.getChoices()) {
                System.out.println(choice.getText());
                translateCriteria.setText(choice.getText().trim().replace("\n", "<br/>"));
            }
        }
        return translateCriteria;
    }

    private Content getFakeContent() {
        Content content = new Content();
        Data data = new Data();
        Text text = new Text();
        text.setTranslatedText("Hi Good Morning!");
        text.setDetectedSourceLanguage("EN");
        data.setTranslations(Arrays.asList(text));
        content.setData(data);
        return content;
    }

    private LinkedList<String> searchStringList(String html) {
        LinkedList<String> searchList = new LinkedList<>();
        Document doc = Jsoup.parse(html, "", Parser.xmlParser());
        for (Element e : doc.select("")) {
            searchList.add(e.html());
        }
        if(CollectionUtils.isEmpty(searchList)) {
            searchList.add(html);
        }
        return searchList;
    }

    private String replaceContent(LinkedList<String> contents, String html) {
        if(contents.size() == 1) {
            return contents.get(0);
        }
        Document doc = Jsoup.parse(html, "", Parser.xmlParser());
        int i = 0;
        for (Element e : doc.select("value")) {
            e.html(contents.get(i));
            i++;
        }
        return doc.html();
    }

    public TranslateCriteria codeReviewWithGPT(String content) {
        String responseContent = this.reviewChange(content);
        TranslateCriteria translateCriteria = new TranslateCriteria();
        translateCriteria.setText(responseContent);
        return translateCriteria;
    }

    public TranslateCriteria chatWithGPT(String content, boolean isLanguage) {
        TranslateCriteria translateCriteria = new TranslateCriteria();
        if(isLanguage) {
            try {
                translateCriteria = this.translateEntirePage(content);
                System.out.println(translateCriteria.getText());
                return translateCriteria;
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            //translateCriteria.setText(String.format(TRANSLATION_TEXT, translateCriteria.getTargetLng(), content));
        }else {
            translateCriteria.setText(content);
        }
        return this.translateTextByOpenAPI(translateCriteria);
    }

    public static void processImg(BufferedImage inputImage, float scaleFactor, float offset )
            throws IOException, TesseractException
    {
        // We will create an image buffer
        // for storing the image later on
        // and inputImage is an image buffer
        // of input image
        BufferedImage outputImage = new BufferedImage( 1050, 1024, inputImage.getType( ) ) ;
        // Now, for drawing the new image
        // we will create a 2D platform
        // on the buffer image
        Graphics2D grp = outputImage.createGraphics( ) ;
        // drawing a new zoomed image starting
        // from 0 0 of size 1050 x 1024
        // and null is the ImageObserver class object
        grp.drawImage( inputImage, 0, 0, 1050, 1024, null ) ;
        grp.dispose( ) ;
        // for the gray scaling of images
        // we'll use RescaleOp object
        RescaleOp rescaleOutput = new RescaleOp( scaleFactor, offset, null ) ;
        // Here, we are going to perform
        // scaling of the image and then
        // writing on a .jpg file
        BufferedImage finalOutputimage = rescaleOutput.filter( outputImage, null ) ;
        ImageIO.write( finalOutputimage, " jpg ",
                new File( "pico.jpg " ) ) ;
        // Creating an instance of Tesseract class
        // that will be used to perform OCR
        Tesseract tesseractInstance = new Tesseract( ) ;
        tesseractInstance.setDatapath("." ) ;
        // finally performing OCR on the image
        // and then storing the result in 'str' string
        String str = tesseractInstance.doOCR( finalOutputimage ) ;
        System.out.println( str ) ;
    }


    public static void main(String[] args) throws IOException, TesseractException, URISyntaxException, ParseException {

        String json = "Sure, here's an example HTML table that displays the information you requested:\n" +
                "<table>\n" +
                "  <tr>\n" +
                "    <th>License Number</th>\n" +
                "    <td>1 23456739</td>\n" +
                "  </tr>\n" +
                "  <tr>\n" +
                "    <th>Name</th>\n" +
                "    <td>DOE JOHN</td>\n" +
                "  </tr>\n" +
                "  <tr>\n" +
                "    <th>Date of Birth</th>\n" +
                "    <td>09/05/1993</td>\n" +
                "  </tr>\n" +
                "  <tr>\n" +
                "    <th>Address</th>\n" +
                "    <td>ommm mwuus</td>\n" +
                "  </tr>\n" +
                "  <tr>\n" +
                "    <th>Sex</th>\n" +
                "    <td>m</td>\n" +
                "  </tr>\n" +
                "</table>\n" +
                "Note that this is just an example and the actual HTML styling may vary based on your requirements.\n";

        String text = "{\n" +
                "\"Driver License\": {\n" +
                "\"Number\": \"123456739\",\n" +
                "\"Class\": \"c\",\n" +
                "\"Expiry Date\": \"11/01/2025\",\n" +
                "\"First Name\": \"JOHN\",\n" +
                "\"Last Name\": \"DOE\",\n" +
                "\"Middle Name\": \"M\",\n" +
                "\"Suffix\": \"\",\n" +
                "\"Date of Birth\": \"09/05/1993\",\n" +
                "\"Sex\": \"m\",\n" +
                "\"Endorsements\": \"\",\n" +
                "\"Height\": \"ommm\",\n" +
                "\"Weight\": \"mwuus\",\n" +
                "\"Eye Color\": \"m.\",\n" +
                "\"Issue Date\": \"(Maﬁa ﬁzJ‘L’JSHnEFW‘ 55am;\"\n" +
                "}\n" +
                "}";




    }

    public String getJsonFromString(String input) {

        List<Character> stack = new ArrayList<Character>();
        List<String> jsons = new ArrayList<String>();
        String temp = "";
        for(char eachChar: input.toCharArray()) {
            if(stack.isEmpty() && eachChar == '{') {
                stack.add(eachChar);
                temp += eachChar;
            } else if(!stack.isEmpty()) {
                temp += eachChar;
                if(stack.get(stack.size()-1).equals('{') && eachChar == '}') {
                    stack.remove(stack.size()-1);
                    if(stack.isEmpty()) {
                        jsons.add(temp);
                        temp = "";
                    }
                }
                else if(eachChar == '{' || eachChar == '}')
                    stack.add(eachChar);
            } else if(temp.length()>0 && stack.isEmpty()) {
                jsons.add(temp);
                temp = "";
            }
        }
        return jsons.get(0);
    }

    private static void jsonReplace(Map<String, String> finalMap, Map<String, Object> map) {
        for(Map.Entry<String, Object> entry: map.entrySet()) {
            if(entry.getValue() instanceof Map) {
                jsonReplace(finalMap, (Map<String, Object>) entry.getValue());
            }else if(entry.getValue() instanceof String) {
                finalMap.put(entry.getKey(), (String) entry.getValue());
            }else if(entry.getValue() instanceof List) {
                List<Map<String, Object>> list = (List<Map<String, Object>>) entry.getValue();
                for(Map<String, Object> entryMap: list) {
                    jsonReplace(finalMap, entryMap);
                }
            }
        }
    }


    private String getMap(Map<String, String> replaceMap) throws IOException {
        String text = new String(Files.readAllBytes(Paths.get("D:\\Workspace\\ChatService\\src\\main\\resources\\templates\\body.html")), StandardCharsets.UTF_8);
        Document document = Jsoup.parse(text);
        Elements allElements =
                document.getAllElements();
        int i = 1;
        for (Element element : allElements) {
            if(StringUtils.hasText(element.ownText()) && element.ownText().length() > 5) {
                replaceMap.put("$content"+i, element.ownText());
                element.html("$content"+i);
                i++;
            }
        }
        return document.html();
    }

    public TranslateCriteria chatWithTrainedModel(String content) {
        try (CloseableHttpClient httpclient = HttpClients.createDefault()) {
            //HTTP GET method
            String url = String.format(CHAT_URL, content.replaceAll(" ", "%20"));
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
            //ObjectMapper mapper = new ObjectMapper();
            /*Map<String, String> map = mapper.readValue(responseBody, Map.class);
            TranslateCriteria translateCriteria = new TranslateCriteria();
            if(Objects.nonNull(map)) {
                String answer = String.format(ANSWER_TEXT, map.get("answer"), map.get("title"), map.get("title"));
                translateCriteria.setText(answer);
            }*/
            //String map = mapper.readValue(responseBody, String.class);
            TranslateCriteria translateCriteria = new TranslateCriteria();
            if(Objects.nonNull(responseBody)) {
                ObjectMapper mapper = new ObjectMapper();
                Map<String, String> map = mapper.readValue(responseBody, Map.class);
                translateCriteria.setText(map.get("answer"));
            }
            return translateCriteria;
        } catch (ClientProtocolException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private TranslateCriteria translateEntirePage(String language) throws IOException {
        /*ObjectMapper mapper = new ObjectMapper();
        Map<String, String> replacedMap = mapper.readValue(new File("D:\\Workspace\\ChatService\\src\\main\\resources\\templates\\spanish.json"), Map.class);
        Map<String, String> map = new LinkedHashMap<>();
        String replacedText = this.getMap(map);
        this.replaceContent(replacedMap, replacedText);*/
        TranslateCriteria translateCriteria = new TranslateCriteria();
        if("EN".equalsIgnoreCase(language)) {
            translateCriteria.setText(new String(Files.readAllBytes
                    (Paths.get("D:\\Workspace\\ChatService\\src\\main\\resources\\templates\\body.html")),
                    StandardCharsets.UTF_8));
        }else {
            translateCriteria.setText(new String(Files.readAllBytes
                    (Paths.get("D:\\Workspace\\ChatService\\src\\main\\resources\\templates\\replaceBody.html")),
                    StandardCharsets.UTF_8));
        }
        /*this.translateEntirePage(translateCriteria);*/
        return translateCriteria;
    }

    private TranslateCriteria translateEntirePage(TranslateCriteria translateCriteria) throws IOException {
        Map<String, String> map = new LinkedHashMap<>();
        String replacedText = this.getMap(map);
        Map<String, String> convertedMap = new LinkedHashMap<>();
        if(map.size() > 0) {
            int i = 0;
            System.out.println("Total Map count ====  = " + map.size());
            for(Map.Entry<String, String> valuesMap: map.entrySet()) {
                try {
                    HttpHeaders headers = new HttpHeaders();
                    headers.add("Authorization", String.format(AUTHORIZATION, openApiKey));
                    headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));

                    OpenApiRequest openApiRequest = new OpenApiRequest();
                    openApiRequest.setPrompt(String.format(TRANSLATION_TEXT, "ES", valuesMap.getValue()));

                    HttpEntity<OpenApiRequest> request =
                            new HttpEntity<OpenApiRequest>(openApiRequest, headers);
                    System.out.println("URL ======= "+openApiURL + " count ===== "+ i);

                    OpenApiResponse response = restTemplate.postForObject(openApiURL, request, OpenApiResponse.class);
                    if(Objects.nonNull(response) && !CollectionUtils.isEmpty(response.getChoices())) {
                        for(Choices choice: response.getChoices()) {
                            System.out.println(valuesMap.getValue() + " ==== "+choice.getText());
                            convertedMap.put(valuesMap.getKey(), choice.getText());
                        }
                    }
                    i++;
                    try {
                        Thread.sleep(1000l);
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                }catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
        ObjectMapper mapper = new ObjectMapper();
        String json = mapper.writeValueAsString(convertedMap);
        byte[] arr = json.getBytes();

        // Try block to check for exceptions
        try {
            // Now calling Files.write() method using path
            // and byte array
            Files.write(Paths.get("D:\\Workspace\\ChatService\\src\\main\\resources\\templates\\spanish.json"), arr);
        }

        // Catch block to handle the exceptions
        catch (IOException ex) {
            // Print message as exception occurred when
            // invalid path of local machine is passed
            System.out.print("Invalid Path");
        }
        String content = this.replaceContent(convertedMap, replacedText);
        translateCriteria.setText(content);
        return translateCriteria;
    }

    private String replaceContent(Map<String, String> replacedMap, String text1) throws IOException {

        String text = new String(Files.readAllBytes(Paths.get("D:\\Workspace\\ChatService\\src\\main\\resources\\templates\\body.html")), StandardCharsets.UTF_8);
        Document document = Jsoup.parse(text);
        Elements allElements =
                document.getAllElements();
        int i = 1;
        for (Element element : allElements) {
            if(StringUtils.hasText(element.ownText()) && element.ownText().length() > 5) {
                element.html(replacedMap.get("$content"+i));
                i++;
            }
        }
        /*return document.html();

        for(Map.Entry<String, String> valuesMap: replacedMap.entrySet()) {
            text = text.replace(valuesMap.getKey(), valuesMap.getValue());
        }*/
        byte[] arr = document.html().getBytes();

        // Try block to check for exceptions
        try {
            // Now calling Files.write() method using path
            // and byte array
            Files.write(Paths.get("D:\\Workspace\\ChatService\\src\\main\\resources\\templates\\replaceBody.html"), arr);
        }

        // Catch block to handle the exceptions
        catch (IOException ex) {
            // Print message as exception occurred when
            // invalid path of local machine is passed
            System.out.print("Invalid Path");
        }
        return text;
    }


}
