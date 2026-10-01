# 03 - Coleta do perfil do adotante

## Objetivo

Esta etapa registra a implementação da coleta progressiva de informações do usuário na Anjos IA. O perfil é usado para tornar a conversa mais organizada e fornecer contexto para a recomendação de animais.

## Fluxo implementado no Dify

A coleta foi organizada com os seguintes blocos principais:

1. **INICIAR** - recebe a mensagem do usuário;
2. **Extrator de Parâmetros** - identifica informações de perfil presentes na mensagem;
3. **Atribuidor de Variáveis** - persiste os valores extraídos em variáveis de conversa;
4. **LLM de perfil** - verifica quais informações ainda estão faltando e faz a próxima pergunta;
5. o processo se repete até existir informação suficiente para avançar para recomendação ou outra intenção.

A estratégia adotada evita pedir todos os dados de uma única vez e mantém a conversa mais próxima de um diálogo natural.

## Variáveis de conversa

| Variável | Finalidade |
|---|---|
| `perfil_especie` | espécie desejada pelo usuário |
| `perfil_moradia` | tipo de moradia |
| `perfil_criancas` | presença de crianças no ambiente |
| `perfil_outros_animais` | presença de outros animais |
| `perfil_porte` | preferência de porte |
| `perfil_idade` | preferência de idade |
| `perfil_tempo_sozinho` | tempo aproximado que o animal ficará sozinho |
| `perfil_rotina` | descrição da rotina do usuário |
| `perfil_quintal` | informação sobre disponibilidade de quintal |
| `perfil_atividade` | nível de atividade esperado |

As variáveis são do tipo texto e ficam salvas na conversa para que as informações não sejam perdidas a cada nova mensagem.

## Regras aplicadas à conversa

O modelo responsável pela coleta do perfil foi ajustado para:

- conversar em português brasileiro;
- usar linguagem simples e amigável;
- fazer **uma pergunta por resposta**;
- evitar repetir perguntas já respondidas;
- priorizar os campos ainda vazios;
- manter as respostas curtas;
- separar informações de rotina e nível de atividade;
- não recomendar um animal antes de concluir informações mínimas de perfil;
- aproveitar dados informados espontaneamente pelo usuário.

## Exemplo

Entrada:

```text
Quero um cachorro pequeno e filhote.
```

O extrator pode identificar:

```text
perfil_especie = cachorro
perfil_porte = pequeno
perfil_idade = filhote
```

Essas informações são armazenadas e o modelo pergunta somente o próximo dado necessário, por exemplo:

```text
Você mora em casa ou apartamento?
```

## Persistência

O bloco **Atribuidor de Variáveis** utiliza a operação de sobrescrita para atualizar o valor de cada variável quando uma informação válida é identificada.

Esse comportamento permite corrigir preferências durante a própria conversa. Por exemplo, se inicialmente o usuário disser que deseja um cachorro pequeno e depois mudar para porte médio, o perfil pode ser atualizado.

## Cuidados adotados

Durante os testes foi necessário garantir que uma resposta referente a uma pergunta específica não apagasse informações já coletadas em etapas anteriores.

Por isso, os prompts de extração passaram a considerar o contexto atual antes de atualizar os valores.

Também foi evitado interpretar respostas genéricas como `sim`, `não` ou `ok` como uma nova preferência quando elas se referem a outra pergunta do fluxo.

## Relação com a recomendação

Os dados do perfil são utilizados posteriormente pelo fluxo de recomendação e de listagem de animais.

Exemplo de critérios:

```text
Espécie: cachorro
Porte: pequeno
Idade: filhote
Moradia: apartamento
Outros animais: gato
Nível de atividade: moderado
```

Essas informações são transformadas em contexto de busca para consultar a base de conhecimento da Anjos IA.

## Estado atual

A coleta do perfil está implementada no workflow do Dify e foi utilizada nos testes conversacionais do MVP.

Ainda podem ser realizados ajustes de linguagem e de quantidade mínima de perguntas após a validação com usuários reais.
