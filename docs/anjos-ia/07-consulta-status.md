# 07 - Consulta de status da solicitação

## Objetivo

Esta etapa registra a implementação da consulta de status da adoção pela própria Anjos IA.

O usuário pode informar o e-mail ou o WhatsApp utilizado no cadastro e, quando necessário, o animal de interesse. O fluxo consulta a mesma planilha usada para registrar as solicitações e retorna o status atual e o protocolo.

## Entrada no fluxo

A variável de controle é:

```text
consultar_status
```

Ela recebe `sim` quando o usuário demonstra intenção de consultar uma solicitação já cadastrada.

Exemplos:

```text
"Como está minha adoção?"        -> sim
"Quero consultar minha solicitação." -> sim
"Qual o status do meu pedido?"   -> sim
```

## Fluxo no Dify

Os principais blocos são:

1. **SE/SENÃO 4 - CONSULTAR STATUS** - verifica se `consultar_status = sim`;
2. **SE/SENÃO 6** - verifica se existe e-mail ou WhatsApp disponível;
3. **Requisição HTTP 2 - Consultar solicitação** - chama o Web App por GET;
4. **Código 2 - Ler status** - interpreta a resposta JSON;
5. **SE/SENÃO 5 - Solicitação encontrada** - separa resultado encontrado e não encontrado;
6. **Resposta 7 - Status da solicitação** - apresenta nome, animal, status e protocolo;
7. **Resposta 8 - Solicitação não encontrada** - orienta o usuário a revisar os dados;
8. **Resposta 9 - Pedir contato** - solicita e-mail ou WhatsApp quando nenhum identificador foi informado;
9. **Modelo 6** e **Finalizar consulta de status** - redefinem `consultar_status` para `não` ao concluir.

## Requisição GET

A consulta utiliza o mesmo endpoint do Google Apps Script.

Parâmetros:

```text
email
whatsapp
animal
```

O animal é opcional e pode ajudar a diferenciar solicitações quando o mesmo contato possui mais de um registro.

## Regras de busca

O Apps Script:

- normaliza o e-mail para letras minúsculas;
- remove caracteres não numéricos do WhatsApp;
- percorre a planilha da linha mais recente para a mais antiga;
- aceita correspondência por e-mail ou WhatsApp;
- quando `animal` é informado, também exige correspondência com o animal;
- retorna o primeiro registro compatível encontrado.

## Exemplo de resposta encontrada

```json
{
  "sucesso": true,
  "encontrado": true,
  "nome": "Maria",
  "animal": "Bento",
  "status": "Em avaliação",
  "protocolo": "ADP-0001"
}
```

## Exemplo de resposta não encontrada

```json
{
  "sucesso": true,
  "encontrado": false,
  "mensagem": "Solicitação não encontrada."
}
```

## Tratamento no Dify

O nó de código transforma o booleano retornado pela API em texto simples:

```text
sim
não
```

Também extrai os campos:

- nome;
- animal;
- status;
- protocolo;
- mensagem.

Isso facilita o uso desses dados nos nós condicionais do workflow.

## Resposta apresentada ao usuário

Quando a solicitação é encontrada, o formato utilizado é:

```text
Olá, [nome]!

A sua solicitação de adoção de [animal] está atualmente com o status:

[status]

Protocolo: [protocolo]
```

Quando não é encontrada:

```text
Não encontrei uma solicitação com os dados informados.
Confira se o e-mail, WhatsApp ou animal estão corretos e tente novamente.
```

Quando falta contato:

```text
Para localizar sua solicitação, preciso que você informe o e-mail ou o WhatsApp usado no cadastro.
```

## Preservação da intenção

Durante os testes foi identificado que, depois de o bot pedir e-mail ou WhatsApp, uma resposta contendo apenas o identificador podia fazer a intenção de consulta desaparecer.

O extrator foi ajustado para preservar:

```text
consultar_status = sim
```

enquanto o fluxo de consulta estiver ativo.

## Finalização

Depois de retornar o status, o sistema redefine:

```text
consultar_status = não
```

Isso impede que as próximas mensagens continuem presas no fluxo de consulta.

## Arquivos relacionados

```text
src/anjos-ia/google-apps-script/Code.gs
src/anjos-ia/dify/ler_status.py
```

## Estado atual

A consulta de status está integrada ao MVP e utiliza a mesma planilha do cadastro de adoção, permitindo que o usuário acompanhe a solicitação sem depender de uma nova entrada manual no sistema.
