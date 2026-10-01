# 10 - Testes do workflow da Anjos IA

## Objetivo

Esta etapa registra os testes técnicos realizados durante o desenvolvimento do MVP da Anjos IA, os comportamentos observados, os problemas encontrados e as correções aplicadas.

Os registros abaixo não substituem a validação com usuários reais. Eles representam testes funcionais feitos durante a construção do workflow no Dify.

## Critério de classificação

Os casos foram classificados como:

- **Validado tecnicamente**: o comportamento foi testado e funcionou no cenário observado;
- **Corrigido durante os testes**: o problema foi identificado e houve ajuste no workflow;
- **Parcial**: parte do comportamento funciona, mas ainda existe limitação conhecida;
- **Pendente de validação final**: precisa de novo teste completo ou validação com usuários.

## Casos de teste

| ID | Cenário | Resultado esperado | Situação |
|---|---|---|---|
| CT-01 | Saudação inicial | Responder normalmente sem entrar em adoção ou status | Validado tecnicamente |
| CT-02 | Coleta de espécie | Registrar cachorro ou gato no perfil | Validado tecnicamente |
| CT-03 | Coleta progressiva do perfil | Fazer uma pergunta por vez e preservar respostas anteriores | Corrigido durante os testes |
| CT-04 | Recomendação baseada na base | Usar apenas dados presentes no contexto recuperado | Corrigido durante os testes |
| CT-05 | Animal indisponível | Informar indisponibilidade e oferecer no máximo 2 alternativas | Pendente de validação final |
| CT-06 | Preservação de interesse_animal | Manter o animal escolhido durante adoção e consulta | Corrigido durante os testes |
| CT-07 | Início da adoção | Entrar no cadastro somente quando houver intenção clara | Validado tecnicamente |
| CT-08 | Autorização de contato | Preservar aceita_contato após resposta do usuário | Corrigido durante os testes |
| CT-09 | Recusa de e-mail | Não repetir a pergunta de e-mail depois de recusa explícita | Validado tecnicamente |
| CT-10 | WhatsApp com DDD | Capturar e preservar o número completo | Corrigido durante os testes |
| CT-11 | Registro no Google Sheets | Criar nova linha com dados da solicitação | Validado tecnicamente |
| CT-12 | Geração de protocolo | Gerar protocolo ADP e retornar ao fluxo | Validado tecnicamente |
| CT-13 | Consulta de status | Buscar solicitação por e-mail ou WhatsApp | Validado tecnicamente |
| CT-14 | Reset após adoção | Definir quer_iniciar_adocao = não após concluir | Corrigido durante os testes |
| CT-15 | Reset após consulta | Definir consultar_status = não após concluir | Corrigido durante os testes |
| CT-16 | Listagem com fotos | Exibir animais disponíveis com imagem, nome e dados | Validado tecnicamente |
| CT-17 | Filtragem exata na listagem | Priorizar corretamente espécie, porte e idade | Parcial |

## Evidências e observações

### CT-01 - Saudação inicial

Após a reconstrução do fluxo normal, a mensagem:

```text
ola
```

voltou a receber uma resposta normal, sem entrar indevidamente em outro ramo.

### CT-03 - Coleta progressiva

Foi executado um teste de conversa em que o usuário informou, ao longo de várias mensagens:

- cachorro;
- apartamento;
- presença de um gato;
- porte pequeno;
- filhote;
- cerca de uma hora sozinho;
- rotina tranquila;
- ausência de crianças.

O teste demonstrou a necessidade de preservar as variáveis já preenchidas e evitar perguntas repetidas.

### CT-04 - Recomendação

Durante testes iniciais, o modelo chegou a inventar etapas do processo da ONG e detalhes não existentes na base.

Como correção, os prompts passaram a exigir que as respostas sobre os animais utilizem somente dados presentes no contexto recuperado.

Também foi adicionada a orientação de não garantir compatibilidade absoluta entre animal e adotante.

### CT-06 - Interesse pelo animal

Foi identificado um caso em que o fluxo de adoção avançou sem manter corretamente o animal selecionado.

O efeito observado foi uma resposta final semelhante a:

```text
interesse na adoção de .
```

A preservação de `interesse_animal` passou a ser tratada como regra de estado.

Também ficou registrada a necessidade de impedir o início formal da adoção quando nenhum animal específico estiver selecionado.

### CT-09 - Recusa de e-mail

Em um teste, a usuária fictícia Maria:

1. informou o nome;
2. autorizou contato;
3. informou WhatsApp;
4. recusou fornecer e-mail.

Após a criação de `recusou_email` e do terceiro caso do nó **SE/SENÃO 4**, o fluxo passou a aceitar a conclusão usando WhatsApp quando a recusa de e-mail é explícita.

### CT-10 - WhatsApp

Foi observado um caso em que apenas o DDD `99` foi persistido.

A descrição do parâmetro foi ajustada para exigir o número completo com DDD e preservar o valor já coletado.

A coluna correspondente no Google Sheets também deve permanecer formatada como texto.

### CT-11 e CT-12 - Google Sheets e protocolo

O envio por HTTP POST foi testado com o Google Apps Script.

A solicitação passou a ser registrada com:

- data e hora;
- nome;
- WhatsApp;
- e-mail;
- animal;
- autorização;
- status inicial;
- protocolo;
- espécie.

O protocolo automático no formato `ADP-0001` passou a funcionar após a atualização da implantação do Web App para uma nova versão.

### CT-13 - Consulta de status

O fluxo foi preparado para consultar a planilha por:

- e-mail;
- ou WhatsApp;
- com animal opcional.

O retorno inclui nome, animal, status e protocolo.

Também foi necessário preservar `consultar_status = sim` quando o bot pede o contato e o usuário responde apenas com o identificador.

### CT-16 - Fotos

As URLs iniciais do `loremflickr.com` não renderizavam de forma consistente no preview do Dify.

Foram substituídas em alguns registros por links diretos do Wikimedia Commons.

As fotos de Thor e Mel foram exibidas corretamente no teste de listagem, confirmando que o Markdown com URL direta funciona.

### CT-17 - Filtragem exata

Consulta testada:

```text
Quero ver cachorros pequenos e filhotes disponíveis para adoção.
```

O perfil usado na busca continha:

```text
especie = cachorro
porte = pequeno
idade = filhote
```

Mesmo com `Top K = 10`, a recuperação retornou animais como Thor e Mel e não priorizou Bento como esperado.

Portanto, este caso permanece **parcial**.

A melhoria prevista é substituir ou complementar a recuperação semântica com:

- metadados estruturados;
- filtro determinístico;
- ou código de filtragem antes da resposta do LLM.

## Problemas relevantes ainda pendentes

1. impedir formalmente a adoção quando `interesse_animal` estiver vazio;
2. concluir o fluxo de seleção do animal depois da listagem;
3. tornar a filtragem por espécie, porte e idade determinística;
4. revisar respostas sobre cuidados veterinários para evitar orientações não fundamentadas;
5. impedir qualquer invenção sobre procedimentos internos da ONG;
6. executar uma conversa completa novamente depois de todas as correções;
7. validar o agente com usuários reais do público-alvo.

## Roteiro recomendado para teste completo

```text
1. iniciar conversa;
2. informar espécie de interesse;
3. responder ao perfil;
4. pedir animais disponíveis;
5. visualizar animal com foto e informações;
6. escolher um animal específico;
7. iniciar a adoção;
8. fornecer os dados solicitados;
9. verificar o protocolo;
10. consultar o status;
11. verificar se a conversa retorna ao fluxo normal.
```

## Observação sobre validação

Os testes deste documento são técnicos e funcionais.

A validação acadêmica com público-alvo deve ser registrada separadamente, com participantes reais, respostas reais e evidências reais. Nenhum resultado de usuário deve ser inventado para completar o relatório.
