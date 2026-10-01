# 05 - Fluxo de solicitação de adoção

## Objetivo

Esta etapa registra a implementação do fluxo que permite ao usuário iniciar formalmente uma solicitação de adoção depois de demonstrar interesse em um animal.

O fluxo foi separado da etapa de recomendação para evitar que a coleta de dados pessoais comece antes da escolha do animal.

## Entrada no fluxo

A principal variável de controle é:

```text
quer_iniciar_adocao
```

Ela deve receber `sim` somente quando o usuário demonstra claramente que deseja iniciar a adoção.

Exemplos:

```text
"Quero adotar o Bento."          -> sim
"Quero iniciar a adoção."        -> sim
"Pode começar o processo."       -> sim
"Quero saber mais sobre ele."    -> não
```

## Regra de segurança do fluxo

Antes de avançar para a coleta de dados do adotante, o sistema deve possuir um animal definido em:

```text
interesse_animal
```

O objetivo é impedir solicitações sem identificação do animal.

Fluxo esperado:

```text
animal escolhido
      ↓
quer_iniciar_adocao = sim
      ↓
coleta dos dados do adotante
      ↓
validação das informações
      ↓
registro da solicitação
```

## Blocos utilizados no Dify

Os principais nós associados à adoção são:

1. **SE/SENÃO 3** - verifica se o usuário deseja iniciar a adoção;
2. **SE/SENÃO 4** - valida quais dados obrigatórios já foram coletados;
3. **LLM 4 - COLETA DE DADOS DA ADOÇÃO** - solicita o próximo dado necessário;
4. **Resposta 4 - Coleta de Dados** - apresenta a pergunta ao usuário;
5. **Salvar solicitação na planilha** - envia os dados para persistência;
6. **Modelo 5** - retorna literalmente `não`;
7. **Finalizar processo de adoção** - redefine `quer_iniciar_adocao`;
8. **Resposta 5 - Dados completos** - confirma que a solicitação foi registrada;
9. **Resposta 6 - Contato não autorizado** - encerra corretamente o fluxo quando o usuário não autoriza contato.

## Variáveis do adotante

| Variável | Finalidade |
|---|---|
| `adotante_nome` | nome informado pelo interessado |
| `adotante_whatsapp` | telefone/WhatsApp com DDD |
| `adotante_email` | e-mail do interessado, quando fornecido |
| `aceita_contato` | autorização para contato pela ONG |
| `recusou_email` | registra quando o usuário optou por não informar e-mail |
| `quer_iniciar_adocao` | controla se o fluxo de adoção está ativo |
| `interesse_animal` | animal escolhido |
| `especie_animal` | espécie do animal selecionado |

## Coleta gradual

O LLM de adoção foi configurado para pedir apenas os dados ainda ausentes.

Exemplo:

```text
Usuário: Quero adotar a Amora.
Bot: Qual é o seu nome?

Usuário: Maria.
Bot: Você autoriza que a ONG entre em contato com você?

Usuário: Sim.
Bot: Qual é o seu WhatsApp com DDD?
```

A conversa não deve repetir um dado já coletado.

## Autorização de contato

A variável:

```text
aceita_contato
```

é obrigatória para continuar com a solicitação.

Quando o usuário informa `não`, o fluxo direciona para **Resposta 6 - Contato não autorizado**.

Isso evita registrar uma solicitação sem que exista autorização para retorno da ONG.

## Recusa de e-mail

Durante os testes, foi observado que o bot continuava pedindo e-mail mesmo depois de o usuário informar que não queria fornecê-lo.

Para corrigir esse comportamento foi criada a variável:

```text
recusou_email
```

Regras:

- se o usuário disser explicitamente que não deseja informar e-mail, definir `recusou_email = sim`;
- enquanto `recusou_email = sim`, não pedir e-mail novamente;
- respostas genéricas como `sim`, `não` ou `ok` referentes a outras perguntas não devem alterar essa variável;
- se o usuário posteriormente fornecer um e-mail por vontade própria, a informação pode ser atualizada.

Com isso, o WhatsApp pode ser suficiente para concluir o cadastro quando o usuário autorizou contato.

## Regras do nó SE/SENÃO 4

O fluxo foi organizado com três condições principais:

### Caso 1 - contato não autorizado

```text
adotante_nome preenchido
E aceita_contato = nao
```

Destino:

```text
Resposta 6 - Contato não autorizado
```

### Caso 2 - dados completos com e-mail

```text
adotante_nome preenchido
E aceita_contato = sim
E adotante_email preenchido
E adotante_whatsapp preenchido
```

Destino:

```text
Salvar solicitação na planilha
```

### Caso 3 - e-mail recusado

```text
adotante_nome preenchido
E aceita_contato = sim
E adotante_whatsapp preenchido
E recusou_email = sim
```

Destino:

```text
Salvar solicitação na planilha
```

Caso nenhuma condição seja atendida, o fluxo retorna ao LLM de coleta para pedir o próximo dado necessário.

## Validação do WhatsApp

Foi identificado em teste um caso em que apenas o DDD foi salvo.

Por isso, a regra de extração do WhatsApp passou a exigir:

- número completo;
- DDD;
- preservação do valor já informado;
- não substituir o número completo por uma parte menor da mensagem.

Exemplo esperado:

```text
(99) 98856-8975
```

## Espécie do animal

A variável:

```text
especie_animal
```

aceita apenas:

```text
Cachorro
Gato
```

A espécie não deve ser inventada a partir do nome do animal. Ela deve vir da base de conhecimento ou de contexto confiável.

## Finalização do fluxo

Depois que a solicitação é registrada, o sistema precisa encerrar corretamente o estado de adoção.

Para isso:

1. **Modelo 5** produz o valor literal `não`;
2. **Finalizar processo de adoção** sobrescreve `quer_iniciar_adocao`;
3. a próxima mensagem do usuário não permanece presa no fluxo de cadastro.

Resultado esperado:

```text
quer_iniciar_adocao = não
```

## Problemas corrigidos nesta etapa

Durante os testes foram identificados e tratados:

- repetição da pergunta de e-mail;
- perda da autorização de contato;
- captura incompleta do WhatsApp;
- necessidade de permitir cadastro sem e-mail quando houve recusa explícita;
- necessidade de preservar o animal de interesse durante a coleta;
- necessidade de resetar o estado da adoção depois do cadastro;
- necessidade de impedir que respostas genéricas alterem variáveis sem relação com a pergunta atual.

## Estado atual

O fluxo de coleta e validação dos dados da adoção está integrado ao MVP.

A persistência dos dados, geração de protocolo e integração com Google Planilhas são tratadas na próxima etapa da documentação.
