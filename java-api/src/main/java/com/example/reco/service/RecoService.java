package com.example.reco.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class RecoService {

    private final RestTemplate restTemplate;

    @Value("${ML_SERVICE_URL:http://ml-service:5001}")
    private String mlServiceUrl;

    public RecoService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public String getRecommendationsForUser(Integer userId, Integer k) {
        String url = String.format("%s/recommend?user_id=%d&k=%d", mlServiceUrl, userId, k);
        ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
        return response.getBody();
    }
}
