# 06 - Integração com Google Planilhas e Apps Script

## Objetivo

Esta etapa registra a persistência das solicitações de adoção da Anjos IA em uma planilha do Google Sheets utilizando um Web App do Google Apps Script.

## Arquitetura da integração

```text
Usuário
  ↓
Anjos IA / Dify
  ↓
HTTP POST
  ↓
Google Apps Script
  ↓
Google Planilhas
```

O Dify envia os dados coletados no fluxo de adoção para o Web App. O Apps Script recebe o JSON, gera o protocolo e adiciona uma nova linha à planilha.

## Estrutura da planilha

A planilha utiliza as seguintes colunas:

| Coluna | Campo |
|---|---|
| A | Data/Hora |
| B | nome |
| C | whatsapp |
| D | email |
| E | animal de interesse |
| F | autorizo contato |
| G | status |
| H | Protocolo |
| I | Espécie |

A coluna de WhatsApp deve preferencialmente estar formatada como texto para evitar perda de zeros, sinais ou formatação.

## Status utilizados

A coluna de status foi preparada para os seguintes valores:

- Novo interesse
- Em contato
- Em avaliação
- Aprovado
- Não aprovado
- Concluído

Ao criar uma nova solicitação, o valor inicial é:

```text
Novo interesse
```

## Dados enviados pelo Dify

Exemplo do corpo JSON utilizado no POST:

```json
{
  "nome": "Maria",
  "whatsapp": "(99) 98856-8975",
  "email": "",
  "animal": "Bento",
  "aceita_contato": "sim",
  "especie": "Cachorro"
}
```

No workflow, esses valores são preenchidos a partir das variáveis de conversa:

- `adotante_nome`
- `adotante_whatsapp`
- `adotante_email`
- `interesse_animal`
- `aceita_contato`
- `especie_animal`

## Geração de protocolo

O Apps Script gera automaticamente um identificador no padrão:

```text
ADP-0001
ADP-0002
ADP-0003
...
```

O número é baseado na quantidade de registros já existentes na planilha.

O protocolo é devolvido ao Dify junto com a resposta da API.

## Resposta esperada

Exemplo:

```json
{
  "sucesso": true,
  "mensagem": "Solicitação registrada com sucesso",
  "protocolo": "ADP-0001"
}
```

## Tratamento de erro

Caso ocorra erro durante o processamento, o Apps Script retorna:

```json
{
  "sucesso": false,
  "mensagem": "descrição do erro"
}
```

## Publicação do Apps Script

Após qualquer alteração no código do Apps Script é necessário atualizar a implantação do Web App para uma nova versão.

Durante os testes, foi identificado um caso em que o código já estava atualizado no editor, mas o endpoint ainda executava uma versão anterior. A atualização da implantação corrigiu o problema e permitiu que o protocolo fosse retornado corretamente.

## Arquivo versionado

O código de referência do Apps Script utilizado no MVP foi adicionado ao repositório em:

```text
src/anjos-ia/google-apps-script/Code.gs
```

## Observação

O endereço real do Web App não foi incluído no repositório. O endpoint deve ser configurado diretamente no nó HTTP do Dify ou por variável de ambiente/configuração adequada quando a aplicação for integrada ao site.
