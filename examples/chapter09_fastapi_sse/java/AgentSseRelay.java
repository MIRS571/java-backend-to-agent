package course.agent;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;

/**
 * A minimal non-blocking relay. Authentication and service credentials belong
 * in Spring Security and WebClient filters, not in request bodies or source code.
 */
@Service
public class AgentSseRelay {

    private final WebClient agentWebClient;

    public AgentSseRelay(WebClient agentWebClient) {
        this.agentWebClient = agentWebClient;
    }

    public Flux<ServerSentEvent<String>> stream(PythonChatRequest request) {
        return agentWebClient.post()
            .uri("/api/v1/agent/chat/stream")
            .contentType(MediaType.APPLICATION_JSON)
            .accept(MediaType.TEXT_EVENT_STREAM)
            .bodyValue(request)
            .retrieve()
            .bodyToFlux(
                new ParameterizedTypeReference<ServerSentEvent<String>>() {}
            );
    }

    public record PythonChatRequest(
        @JsonProperty("user_id") String userId,
        @JsonProperty("thread_id") String threadId,
        String message
    ) {}
}
