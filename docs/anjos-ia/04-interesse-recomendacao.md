# 04 - Identificação de interesse e recomendação de animais

## Objetivo

Esta etapa registra a evolução do fluxo responsável por entender o interesse do usuário em um animal e utilizar a base de conhecimento da Anjos IA para responder sobre disponibilidade e recomendar opções compatíveis com o perfil informado.

## Blocos utilizados no workflow

O fluxo foi organizado com os seguintes elementos principais:

1. **Modelo / Modelo de Interesse** - prepara o contexto usado para interpretar a mensagem;
2. **Extrator de interesse** - identifica intenções e dados relacionados ao interesse em adoção;
3. **Atribuidor de Variáveis Interesse** - persiste as informações extraídas;
4. **SE/SENÃO 2 - FLUXO NORMAL** - direciona consultas comuns para o fluxo de recomendação;
5. **LLM 2** - produz a resposta de recomendação;
6. **Recuperação de conhecimento** - consulta a base de animais;
7. **Verificar animal disponível** - diferencia animais disponíveis de casos que exigem alternativa;
8. **LLM alternativas / Modelo de alternativas** - prepara opções quando o animal desejado não está disponível;
9. **Resposta 2 alternativas** e **Resposta 3 normal** - apresentam a resposta final ao usuário.

## Variável principal de interesse

A variável central desta etapa é:

```text
interesse_animal
```

Ela representa o nome do animal específico pelo qual o usuário demonstrou interesse.

Exemplos:

```text
"Quero conhecer o Bento."      -> interesse_animal = Bento
"Gostei da Amora."             -> interesse_animal = Amora
"Quero adotar o Thor."         -> interesse_animal = Thor
```

## Preservação do interesse

Durante os testes foi identificado que o nome do animal poderia ser perdido quando a conversa avançava para outras etapas.

O extrator foi ajustado para preservar `interesse_animal` enquanto existe um processo de adoção ou uma consulta de status relacionada àquele animal.

Ao mesmo tempo, o valor não deve permanecer indefinidamente em conversas sem relação com adoção. Quando o usuário inicia um novo assunto e não existe processo ativo, o fluxo pode limpar ou substituir o interesse anterior.

## Recuperação pela base de conhecimento

A recomendação usa a base de animais registrada no Knowledge do Dify.

As informações retornadas podem incluir:

- nome;
- espécie;
- porte;
- idade;
- descrição;
- temperamento;
- convivência com outros animais;
- convivência com crianças;
- moradia recomendada;
- nível de atividade;
- estado de vacinação e castração;
- status de disponibilidade;
- URL da foto.

A resposta deve ser construída apenas com informações presentes no contexto recuperado.

## Regras aplicadas ao LLM de recomendação

O modelo foi ajustado para:

- não inventar características que não estejam na base;
- não afirmar compatibilidade como certeza;
- usar expressões como "pode combinar com o seu perfil" quando apropriado;
- considerar as preferências coletadas anteriormente;
- evitar diagnóstico, prescrição ou orientação veterinária específica;
- usar somente informações de saúde presentes no contexto;
- orientar o usuário a procurar a ONG ou um veterinário quando uma dúvida exigir avaliação profissional;
- não recomendar como disponível um animal cujo status indique indisponibilidade.

## Animal indisponível

Quando o usuário pergunta por um animal que não está disponível, o fluxo deve:

1. informar claramente que aquele animal não está disponível;
2. mencionar o nome do animal solicitado;
3. buscar alternativas na base;
4. apresentar no máximo duas opções disponíveis;
5. evitar afirmar que as alternativas são uma combinação perfeita.

Exemplo de comportamento esperado:

```text
A Cacau não está disponível para adoção no momento.
Posso te mostrar outras opções disponíveis com características semelhantes.
```

## Uso do perfil do adotante

Quando existe perfil preenchido, a recomendação pode considerar dados como:

```text
perfil_especie
perfil_porte
perfil_idade
perfil_moradia
perfil_outros_animais
perfil_criancas
perfil_atividade
```

Essas informações ajudam a ordenar ou contextualizar as opções retornadas pela base.

## Ajustes realizados durante os testes

Durante o desenvolvimento foram observados e corrigidos comportamentos como:

- repetição de informações já conhecidas;
- perda de `interesse_animal` ao avançar para adoção;
- respostas que tratavam compatibilidade como certeza;
- alternativas apresentadas sem indicar que o animal original estava indisponível;
- tentativa de responder questões de saúde além das informações existentes na base;
- necessidade de restaurar o fluxo normal após alterações no nó de decisão.

## Limitação atual

A recuperação do Knowledge do Dify é semântica. Portanto, ela pode retornar registros relacionados mesmo quando não correspondem exatamente a todos os filtros estruturados.

Esse comportamento motivou posteriormente a criação de um fluxo específico para **listar animais disponíveis**, documentado em uma etapa separada.

## Estado desta etapa

O fluxo de interesse e recomendação está integrado ao MVP e serve de ligação entre:

```text
coleta de perfil
      ↓
identificação do interesse
      ↓
consulta à base
      ↓
recomendação / alternativa
      ↓
seleção de um animal
```

A seleção de um animal específico passa a ser usada posteriormente pelo fluxo formal de solicitação de adoção.
