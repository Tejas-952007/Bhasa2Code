# Minimal secure C/C++ sandbox image
FROM alpine:latest

# Security: Install minimal compilers and create unprivileged non-root user
RUN apk add --no-cache gcc g++ musl-dev && \
    addgroup -g 1000 sandbox && \
    adduser -u 1000 -G sandbox -s /bin/sh -D sandbox && \
    mkdir -p /workspace && \
    chown -R sandbox:sandbox /workspace

WORKDIR /workspace

USER sandbox

CMD ["g++", "--version"]
