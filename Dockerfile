# Fase 1: Node.js e Webpack para build dos assets
FROM node:20 AS build

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar package.json e instalar dependências Node.js
COPY package.json package-lock.json ./
RUN npm install

# Copiar todos os arquivos do projeto e rodar o build do Webpack
COPY . .
RUN npm run build

# Fase 2: Flask e Python para rodar a aplicação
FROM ubuntu:20.04

ENV NODE_VERSION=20.17.0

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Instalar dependências necessárias
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

# Instalar NVM e Node.js
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

# Configurar NVM_DIR e garantir que o NVM esteja disponível
ENV NVM_DIR=/root/.nvm
ENV PATH="/root/.nvm/versions/node/v$NODE_VERSION/bin/:$PATH"

# Carregar NVM no ambiente do bash
RUN echo "source $NVM_DIR/nvm.sh" >> /root/.bashrc

# Instalar Node.js usando NVM
RUN bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION"
RUN bash -c "source $NVM_DIR/nvm.sh && nvm use $NODE_VERSION"
RUN bash -c "source $NVM_DIR/nvm.sh && nvm alias default $NODE_VERSION"

# Copiar apenas os arquivos gerados pelo Webpack da fase anterior
COPY --from=build /app /app

# Instalar as dependências Python do Flask
COPY requirements.txt . 
RUN pip3 install --no-cache-dir -r requirements.txt

# Configurar Flask para o modo de desenvolvimento e hot-reload de templates
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Expor a porta 8000 para o Flask
EXPOSE 8000

# Definir o comando padrão para rodar o Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]