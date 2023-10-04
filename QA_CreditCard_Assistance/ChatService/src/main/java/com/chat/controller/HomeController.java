package com.chat.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

    @GetMapping ("/chat")
    public String chat() {
        System.out.println("elements");
        return "chat";
    }

    @GetMapping ("/bot")
    public String bot() {
        System.out.println("bot");
        return "bot";
    }
}
