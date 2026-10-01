# 09 - Correções de estado e preservação de variáveis

## Objetivo

Esta etapa registra as correções feitas no workflow da Anjos IA para evitar perda de contexto, repetição de perguntas e permanência indevida do usuário em fluxos já concluídos.

Durante os testes conversacionais, foi observado que algumas variáveis de controle eram apagadas cedo demais ou permaneciam ativas depois da conclusão de uma etapa. Isso afetava principalmente os fluxos de interesse em um animal, adoção e consulta de status.

## Variáveis envolvidas

As principais variáveis ajustadas foram:

- `interesse_animal`
- `quer_iniciar_adocao`
- `consultar_status`
- `aceita_contato`
- `recusou_email`
- `listar_animais`

## Preservação de `interesse_animal`

O nome do animal escolhido precisa permanecer disponível enquanto o usuário estiver:

- iniciando uma adoção;
- fornecendo dados do adotante;
- consultando o status de uma solicitação;
- retomando uma conversa sobre o mesmo animal.

O problema identificado foi a possibilidade de o extrator devolver valor vazio em uma mensagem posterior e sobrescrever o nome já conhecido.

A regra adotada foi preservar o valor anterior quando o processo ativo ainda depende daquele animal.

Exemplo:

```text
Usuário: Quero adotar a Amora.
interesse_animal = Amora

Usuário: Meu nome é Maria.
interesse_animal deve continuar = Amora
```

Ao mesmo tempo, o interesse não deve permanecer para sempre. Quando não existe adoção ou consulta ativa e o usuário muda claramente de assunto, o sistema pode substituir ou limpar o valor anterior.

## Reset de `quer_iniciar_adocao`

A variável:

```text
quer_iniciar_adocao
```

é usada para manter o usuário dentro do fluxo formal de cadastro.

Após uma solicitação ser salva, ela precisa voltar para:

```text
não
```

Para isso foi utilizado:

```text
Modelo 5
      ↓
Finalizar processo de adoção
```

O Modelo 5 produz literalmente `não`, e o atribuidor sobrescreve a variável.

Isso impede que mensagens posteriores sejam interpretadas como continuação de uma adoção já concluída.

## Reset de `consultar_status`

O mesmo comportamento foi aplicado ao fluxo de consulta.

Depois de a solicitação ser encontrada e o status ser apresentado:

```text
consultar_status = não
```

O fluxo utiliza:

```text
Modelo 6
      ↓
Finalizar consulta de status
```

Sem esse reset, a próxima mensagem poderia continuar sendo enviada para o ramo de consulta.

## Preservação de `consultar_status` durante a coleta de contato

A intenção de consulta não deve ser apagada enquanto o sistema ainda está aguardando e-mail ou WhatsApp.

Exemplo:

```text
Usuário: Como está minha adoção?
consultar_status = sim

Bot: Informe o e-mail ou WhatsApp usado no cadastro.

Usuário: (99) 98856-8975
consultar_status deve continuar = sim
```

Somente após a consulta ser concluída a variável volta para `não`.

## Preservação de `aceita_contato`

Durante os testes foi necessário garantir que, depois de o usuário responder sobre autorização de contato, mensagens posteriores contendo nome, WhatsApp ou e-mail não apagassem essa decisão.

Exemplo:

```text
Usuário: Sim, autorizo o contato.
aceita_contato = sim

Usuário: Meu WhatsApp é ...
aceita_contato deve continuar = sim
```

A variável só deve mudar quando o usuário alterar explicitamente sua decisão.

## Preservação de `recusou_email`

A variável `recusou_email` foi criada para impedir que o bot repetisse a solicitação de e-mail depois de uma recusa explícita.

Regras aplicadas:

- se já estiver `sim`, manter `sim` durante a coleta;
- não interpretar um `não` genérico de outra pergunta como recusa de e-mail;
- não interpretar um `sim` genérico como autorização para apagar a recusa;
- alterar o valor apenas quando o usuário falar explicitamente sobre o e-mail;
- se o usuário fornecer um e-mail posteriormente, a informação pode ser atualizada.

## Variável `listar_animais`

A variável de listagem é tratada como intenção de curta duração.

Quando o usuário faz um novo pedido para ver animais:

```text
listar_animais = sim
```

Quando a mensagem seguinte trata de um animal específico ou de outro fluxo, o extrator deve retornar `não`.

Isso evita que o usuário fique preso continuamente no ramo de listagem.

## Uso do Atribuidor de Variáveis

O **Atribuidor de Variáveis Interesse** utiliza sobrescrita.

Esse comportamento é útil, mas exige que o extrator retorne valores coerentes. Caso contrário, uma variável já correta pode ser substituída por valor vazio ou por uma interpretação relacionada a outra pergunta.

Por isso, os prompts de extração passaram a considerar:

- valor atual da variável;
- fluxo ativo;
- intenção da mensagem atual;
- relação da resposta com a última pergunta feita pelo bot.

## Problemas que essas correções evitaram

As regras desta etapa foram criadas para reduzir situações como:

- animal escolhido desaparecendo no meio do cadastro;
- mensagem final exibindo "adoção de ." sem nome do animal;
- bot pedindo e-mail novamente após recusa;
- autorização de contato sendo apagada;
- consulta de status encerrando antes de receber o contato;
- usuário ficando preso na consulta após a resposta;
- usuário ficando preso no processo de adoção depois do cadastro;
- listagem de animais sendo repetida quando a conversa já avançou para outra intenção.

## Regra geral de estado

A lógica adotada pode ser resumida assim:

```text
1. preservar informações ainda necessárias ao fluxo ativo;
2. atualizar somente quando houver nova informação explícita;
3. não deixar respostas genéricas alterarem variáveis sem relação com a pergunta;
4. resetar variáveis de controle quando o fluxo terminar;
5. permitir que o usuário inicie uma nova intenção após a conclusão.
```

## Estado atual

As correções de estado estão incorporadas ao desenho atual do workflow e são essenciais para manter continuidade de contexto entre mensagens.

Novos testes de conversa completa continuam recomendados sempre que forem adicionados novos ramos ou novas variáveis ao agente.
