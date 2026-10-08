# Minimal secure JavaScript (Node.js) sandbox image
FROM node:20-alpine

# Security: Setup sandbox user (uid 1000) and isolated workspace
RUN if id -u node >/dev/null 2>&1; then \
        sed -i 's/^node:/sandbox:/' /etc/passwd && \
        sed -i 's/^node:/sandbox:/' /etc/group; \
    else \
        addgroup -g 1000 sandbox && \
        adduser -u 1000 -G sandbox -s /bin/sh -D sandbox; \
    fi && \
    mkdir -p /workspace && \
    chown -R 1000:1000 /workspace

WORKDIR /workspace

USER sandbox

CMD ["node", "--version"]
