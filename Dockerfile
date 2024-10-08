# Use a imagem oficial do Python no Ubuntu
FROM ubuntu:20.04

ENV NODE_VERSION=20.17.0

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Instala as dependências necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip \
    curl \
    apt-transport-https \
    gnupg2 \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list -o /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Instalar o Python e dependências do projeto
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Instalar NVM e Node.js
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default ${NODE_VERSION}

# Copiar arquivos do projeto para dentro do contêiner
COPY . .

# Instalar dependências do Node.js
RUN . "$NVM_DIR/nvm.sh" && npm install

# Configurar Flask para o modo de desenvolvimento e hot-reload de templates
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Configurar Flask para recarregar templates automaticamente
ENV FLASK_RUN_RELOAD=true

# Expor a porta 8000 para o Flask e 3000 para o Webpack Dev Server
EXPOSE 8000 3000

# Definir o comando padrão para rodar o npm run dev para desenvolvimento
CMD bash -c ". \"$NVM_DIR/nvm.sh\" && npm run dev"