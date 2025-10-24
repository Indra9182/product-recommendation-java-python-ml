package com.example.reco.controller;

import com.example.reco.service.RecoService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/recommendations")
public class RecommendationController {

    private final RecoService recoService;

    public RecommendationController(RecoService recoService) {
        this.recoService = recoService;
    }

    @GetMapping("/{userId}")
    public ResponseEntity<String> recommend(@PathVariable Integer userId,
                                            @RequestParam(defaultValue = "5") Integer k) {
        String body = recoService.getRecommendationsForUser(userId, k);
        return ResponseEntity.ok(body);
    }
}
