# Anjos IA — Registro de Desenvolvimento

## Visão geral

A **Anjos IA** é o agente conversacional do projeto **IAnjos de Patas**, construído no Dify para apoiar o processo de adoção de animais.

O fluxo foi desenvolvido de forma iterativa e atualmente contempla:

- coleta progressiva do perfil do adotante;
- recomendação de animais com base no perfil;
- consulta de animal específico;
- tratamento de animais indisponíveis e sugestão de alternativas;
- início do processo de adoção;
- coleta de nome, WhatsApp e e-mail;
- autorização ou recusa de contato;
- suporte à recusa de e-mail;
- registro da solicitação em Google Planilhas;
- geração automática de protocolo;
- consulta do status da solicitação;
- encerramento correto dos estados de adoção e consulta;
- listagem de animais disponíveis;
- exibição de nome, características e foto dos animais.

## Principais variáveis de perfil

- `perfil_especie`
- `perfil_moradia`
- `perfil_criancas`
- `perfil_outros_animais`
- `perfil_porte`
- `perfil_idade`
- `perfil_tempo_sozinho`
- `perfil_rotina`
- `perfil_quintal`
- `perfil_atividade`

## Variáveis de interesse e adoção

- `interesse_animal`
- `especie_animal`
- `adotante_nome`
- `adotante_whatsapp`
- `adotante_email`
- `aceita_contato`
- `recusou_email`
- `quer_iniciar_adocao`
- `consultar_status`
- `listar_animais`

## Fluxo de adoção

1. O usuário demonstra interesse em um animal.
2. A Anjos IA confirma o animal de interesse.
3. O fluxo identifica `quer_iniciar_adocao = sim`.
4. O agente coleta nome, autorização de contato e WhatsApp.
5. O e-mail é coletado quando informado.
6. Se o usuário recusar o e-mail, `recusou_email = sim` permite continuar somente com WhatsApp.
7. A solicitação é enviada ao Google Apps Script.
8. O Apps Script grava a solicitação na planilha.
9. Um protocolo no formato `ADP-XXXX` é gerado.
10. `quer_iniciar_adocao` é redefinido para `não` ao final do fluxo.

## Consulta de status

A intenção `consultar_status` direciona o usuário para o fluxo de acompanhamento.

A consulta utiliza:

- e-mail; ou
- WhatsApp;
- animal de interesse, quando disponível.

O Apps Script retorna:

- nome;
- animal;
- status;
- protocolo.

Depois da consulta concluída, `consultar_status` é redefinido para `não`.

## Listagem de animais disponíveis

Foi criado um fluxo exclusivo para a intenção `listar_animais`.

Fluxo atual:

```text
SE/SENÃO - LISTAR ANIMAIS
        ↓
Modelo - CONSULTA LISTA DE ANIMAIS
        ↓
Recuperação - LISTA DE ANIMAIS
        ↓
LLM - LISTAR ANIMAIS
        ↓
Resposta - LISTA DE ANIMAIS
```

A resposta pode apresentar:

- nome;
- foto;
- espécie;
- porte;
- idade;
- descrição.

As imagens são exibidas via Markdown usando URLs públicas diretas.

## Integração com Google Planilhas

A planilha de solicitações utiliza, atualmente, os campos:

| Coluna | Campo |
|---|---|
| A | Data/Hora |
| B | Nome |
| C | WhatsApp |
| D | E-mail |
| E | Animal de interesse |
| F | Autoriza contato |
| G | Status |
| H | Protocolo |
| I | Espécie |

Status previstos:

- Novo interesse
- Em contato
- Em avaliação
- Aprovado
- Não aprovado
- Concluído

## Regras importantes implementadas

- fazer apenas uma pergunta por vez;
- não repetir dados já informados;
- preservar variáveis relevantes durante o fluxo ativo;
- não inventar informações de animais;
- evitar garantias de compatibilidade;
- usar somente informações presentes na base/contexto;
- não pedir e-mail novamente quando houver recusa explícita;
- não manter o usuário preso no fluxo de adoção após a conclusão;
- não manter o usuário preso no fluxo de consulta de status;
- exibir somente animais com status disponível na listagem.

## Correções realizadas

Entre os principais problemas corrigidos durante os testes:

- repetição de perguntas;
- perda do animal de interesse;
- autorização de contato sendo sobrescrita;
- consulta de status sendo interrompida após informar e-mail/WhatsApp;
- geração de protocolo ausente em versão antiga do Apps Script;
- fluxo normal interrompido após remoção acidental de um SE/SENÃO;
- e-mail solicitado novamente após recusa;
- WhatsApp extraído apenas como DDD;
- listagem de animais sem fotos;
- URLs de imagem incompatíveis com a renderização do Dify.

## Situação atual

O MVP da Anjos IA já possui os principais fluxos funcionais. O desenvolvimento atual está concentrado em:

- aumentar a precisão da recuperação dos animais por perfil;
- validar todos os animais da base com URLs de imagem diretas;
- concluir os testes de regressão;
- validar a solução com o público-alvo;
- preparar a futura integração com o site Anjos de Patas.

## Próximos passos de versionamento

Os próximos commits desta branch devem separar as mudanças por responsabilidade, incluindo:

1. documentação da Anjos IA;
2. base de conhecimento de teste;
3. fluxo de perfil e recomendação;
4. fluxo de adoção;
5. integração com Google Planilhas;
6. protocolo e consulta de status;
7. recusa de e-mail e preservação de variáveis;
8. listagem de animais com fotos;
9. documentação de validação e testes.
