# Minimal secure Java sandbox image
FROM eclipse-temurin:21-alpine

# Security: Create unprivileged non-root user
RUN addgroup -g 1000 sandbox && \
    adduser -u 1000 -G sandbox -s /bin/sh -D sandbox && \
    mkdir -p /workspace && \
    chown -R sandbox:sandbox /workspace

WORKDIR /workspace

USER sandbox

CMD ["java", "--version"]
