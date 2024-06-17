FROM ubuntu:latest

# Installer les outils de base et les langages
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    nodejs \
    npm \
    php \
    default-jdk \
    && apt-get clean

WORKDIR /app

COPY . .

# Commande par défaut (ne fait rien, le code est spécifié au runtime)
CMD ["tail", "-f", "/dev/null"]
