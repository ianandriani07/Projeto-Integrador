# FreeForm
FreeForm é uma plataforma feita para agilizar os processos de avaliação através de formulários utilizados pela fisioterapia no campus Araranguá da UFSC. Ele consiste em uma ferramenta que permite a criação de fórmularios customizados, similar ao Google Forms, que são armazenados, processados e avaliados dentro da ferramenta para diagnosticos diversos.
Essa plataforma foi feita durante a disciplina de Projeto Integrado e ainda está em WIP (_Work in Progress_).

## Como iniciar o projeto na primeira vez
```
bash
docker-compose up --build
```

## Após o projeto já ser iniciado pela primeira vez

* Após o projeto já ter sido iniciado, você pode executa-lo novamente utilizando
```
bash
docker-compose up
```
* Para parar a execução do projeto basta utilizar
```
bash
docker-compose down
```

## Quando utilizar 'docker-compose up --build' após o projeto já ter sido iniciado
* **Modificações no Dockerfile**: Sempre que você alterar o Dockerfile (como adicionar novos pacotes, mudar as etapas de construção ou fazer qualquer outra alteração), será necessário reconstruir os contêineres para que as mudanças tenham efeito
* **Alterações nas dependências**: Se você fizer mudanças nos arquivos que definem dependências, como o **requirements.txt** para o Flask ou o **package.json** para o Webpack, precisará reconstruir os contêineres para instalar as novas dependências.
* **Mudanças na configuração do docker-compose.yml**: Se você modificar o arquivo **docker-compose.yml**, como mudar as portas, volumes, ou variáveis de ambiente, você deve usar **--build** para garantir que os contêineres sejam atualizados com as novas configurações.

## Quando utilizar 'docker-compose up'
* **Alterações no código da aplicação**: Se você alterar apenas o código da aplicação (como arquivos **.py** para o Flask ou **.js/.scss** para o Webpack), e não fez mudanças no Dockerfile ou nas dependências, você pode rodar apenas **docker-compose up**. Como você configurou volumes no **docker-compose.yml**, essas mudanças no código serão refletidas automaticamente dentro do contêiner sem precisar reconstruí-lo.

## Membros da Equipe
- Fábio
- Ian
- Felipe
