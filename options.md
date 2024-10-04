## Tipos de Perguntas

- Categorico
 - Exemplo: Escolha uma opção abaixo: 'a', 'b', 'c'
- Numérico
 - Exemplo: Digite um número: ...
- Numérico com intervalo
 - Exemplo: Digite um número com intervalor de 2: 0, 2, 4, 6, 8, 10, ...
- Textual
 - Exemplo: Escreva seu nome: ...

## Pergunta Categorica: Requisitos
### Tipo: Escolha única
- Texto: O texto associado a uma pergunta
- Opções Categoricas: As categorias.
- Tabela de Conversão: É necessario uma tabela que associe valores categoricos a valores númericos. Exemplos:
'a': 0,
'b': 5,
'c': 8
- Variavel de Associação: Uma variavel para associar os valores de seleção

### Tipo: Multipla escolha
- Texto: O texto associado a uma pergunta
- Opções Categoricas: As categorias.
- Tabela de Conversão: É necessario uma tabela que associe valores categoricos a valores númericos. Exemplos:
'a': 0,
'b': 5,
'c': 8
- Tipo de Redução: É necessário definir como os multiplos valores selecionados devem ser agrupados para produzir um único resultado. Exemplo: 'média', 'maior valor', 'mediana', ...
- Variavel de Associação: Uma variavel para associar os valores de seleção

## Pergunta Numérica: Requisitos

- Texto: O texto associado a uma pergunta
- Caixa númerica: A caixa de entrada de números
- Variavel de Associação: Uma variavel para associar os valores
- Valor máximo (Opcional): Um valor máximo para uma pergunta númerica
- Valor minimo (Opcional): Um valor minimo para uma pergunta númerica

## Pergunta Numérica com Intervalo: Requisitos
- Texto: O texto associado a uma pergunta
- Caixa númerica: A caixa de entrada de números
- Intervalo: O intervalor associado ao valor númerico.
- Variavel de Associação: Uma variavel para associar os valores
- Valor máximo (Opcional): Um valor máximo para uma pergunta númerica
- Valor minimo (Opcional): Um valor minimo para uma pergunta númerica

## Pergunta Textual: Requisitos
- Texto: O texto associado a uma pergunta
- Caixa textual: A caixa de entradad de textos
- Variavel de Associação: Uma variavel para associar os valores