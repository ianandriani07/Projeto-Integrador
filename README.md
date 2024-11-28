# FreeForm
FreeForm é uma plataforma feita para agilizar os processos de avaliação através de formulários utilizados pela fisioterapia no campus Araranguá da UFSC. Ele consiste em uma ferramenta que permite a criação de fórmularios customizados, similar ao Google Forms, que são armazenados, processados e avaliados dentro da ferramenta para diagnosticos diversos.
Essa plataforma foi feita durante a disciplina de Projeto Integrado e ainda está em WIP (_Work in Progress_).

## Índice
- [Arquitetura](#arquitetura)
- [Quickstart](#quickstart)

## Arquitetura

**Fluxo de Execução**
![Fluxo de Execução]("https://github.com/ianandriani07/Projeto-Integrador/blob/main/images/Fluxo%20do%20Projeto.png")


**Fluxo do Bundler**
![Fluxo do Bundler]("https://github.com/ianandriani07/Projeto-Integrador/blob/main/images/Diagrama%20de%20Build.png")

A stack usada e sua decisão estão a seguir:

**React**
O react foi escolhido pela facilidade de reutilização de código, principalmente na parte de renderização de fórmularios customizados. Ele facilitou a implementação, extensão e diminui o acoplamento do projeto nessa parte e foi por isso que foi escolhido para essa tarefa. Para mais informações em como usar react: [React: Quickstart](https://react.dev/learn "React: Quickstart")

**SWC**
O SWC foi utilizado em vez do babel para transpilação do código jsx já que ele tem suporte nativo para typescript e diminui uma dependência adicional do projeto. Além disso, ele tem um único arquivo de configuração em vez 300 deles. Para saber como usar o SWC com o Webpack e o Flask: [Usando o Webpack, Flask e SWC](https://python-webpack-boilerplate.readthedocs.io/en/latest/swc/ "Usando o Webpack, Flask e SWC")

**Webpack**
Devido a experiência da equipe com a ferramenta e a necessidade de integrar o front com o back-end em flask ele foi escolhido. Além disso, ele removeu completamente a necessidade de usar um outro server como o next.js para fazer o serviço que um bundler qualquer faria. Ele possuí algumas coisas muito interessantes como uma pipeline de execução muito customizavel, ainda que pouco amigavel, e tem infinitos plugins. Para mais informações em como usar o Flask com o Webpack: [Flask e Webpack: Tutorial, a Origem](https://python-webpack-boilerplate.readthedocs.io/en/latest/setup_with_flask/ "Flask e Webpack: Tutorial, a Origem")

**Flask**
Irineu.
**Azure SQL Database**
Pinto

## Quickstart
### Como iniciar o projeto na primeira vez
```bash
docker-compose up --build
```

### Após o projeto já ser iniciado pela primeira vez

* Após o projeto já ter sido iniciado, você pode executa-lo novamente utilizando
```bash
docker-compose up
```
* Para parar a execução do projeto basta utilizar
```bash
docker-compose down
```

### Quando utilizar 'docker-compose up --build' após o projeto já ter sido iniciado
* **Modificações no Dockerfile**: Sempre que você alterar o Dockerfile (como adicionar novos pacotes, mudar as etapas de construção ou fazer qualquer outra alteração), será necessário reconstruir os contêineres para que as mudanças tenham efeito
* **Alterações nas dependências**: Se você fizer mudanças nos arquivos que definem dependências, como o **requirements.txt** para o Flask ou o **package.json** para o Webpack, precisará reconstruir os contêineres para instalar as novas dependências.
* **Mudanças na configuração do docker-compose.yml**: Se você modificar o arquivo **docker-compose.yml**, como mudar as portas, volumes, ou variáveis de ambiente, você deve usar **--build** para garantir que os contêineres sejam atualizados com as novas configurações.

### Quando utilizar 'docker-compose up'
* **Alterações no código da aplicação**: Se você alterar apenas o código da aplicação (como arquivos **.py** para o Flask ou **.js/.scss** para o Webpack), e não fez mudanças no Dockerfile ou nas dependências, você pode rodar apenas **docker-compose up**. Como você configurou volumes no **docker-compose.yml**, essas mudanças no código serão refletidas automaticamente dentro do contêiner sem precisar reconstruí-lo.
