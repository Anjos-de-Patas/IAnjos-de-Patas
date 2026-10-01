# Anjos IA — Documentação do MVP

## Visão geral

A **Anjos IA** é o agente conversacional do projeto **IAnjos de Patas**, desenvolvido no Dify para apoiar o processo de adoção de animais.

Esta documentação registra a evolução do MVP de forma incremental, mantendo cada etapa separada em commits na branch:

```text
feature/anjos-ia
```

A branch foi criada a partir da `main`, mas todas as alterações específicas da Anjos IA estão sendo versionadas separadamente para não modificar diretamente o código principal do repositório.

## Estado atual do MVP

Atualmente, a Anjos IA contempla:

- coleta progressiva do perfil do adotante;
- identificação de interesse em um animal;
- recomendação baseada em dados da base de conhecimento;
- tratamento de animal indisponível;
- listagem de animais disponíveis;
- exibição de fotos em Markdown;
- seleção de animal;
- início do processo de adoção;
- coleta de nome, WhatsApp e e-mail;
- tratamento de recusa de e-mail;
- autorização de contato;
- registro da solicitação no Google Sheets;
- geração automática de protocolo;
- consulta de status;
- controle e preservação de variáveis de conversa;
- testes técnicos do workflow;
- documentação da arquitetura geral.

---

# Índice da documentação

## 01 — Visão geral

Arquivo:

```text
docs/anjos-ia/README.md
```

Documento principal que centraliza a navegação e o estado atual da Anjos IA.

## 02 — Base de conhecimento

Arquivo:

```text
docs/anjos-ia/02-base-conhecimento.md
```

Conteúdo:

- base fictícia de animais;
- estrutura dos dados;
- status de disponibilidade;
- fotos;
- integração com Knowledge do Dify;
- limitações da recuperação semântica.

Arquivo de dados:

```text
data/anjos-ia/base_teste_animais_com_fotos.csv
```

## 03 — Coleta de perfil

Arquivo:

```text
docs/anjos-ia/03-coleta-perfil.md
```

Conteúdo:

- coleta progressiva;
- variáveis do perfil;
- perguntas uma por vez;
- persistência das respostas;
- prevenção de repetição de perguntas.

Schema:

```text
data/anjos-ia/perfil_adotante_schema.json
```

## 04 — Interesse e recomendação

Arquivo:

```text
docs/anjos-ia/04-interesse-recomendacao.md
```

Conteúdo:

- `interesse_animal`;
- consulta à base;
- recomendação;
- animal indisponível;
- alternativas;
- uso do perfil na recomendação;
- regras para evitar invenção de informações.

Schema:

```text
data/anjos-ia/interesse_recomendacao_schema.json
```

## 05 — Solicitação de adoção

Arquivo:

```text
docs/anjos-ia/05-fluxo-solicitacao-adocao.md
```

Conteúdo:

- `quer_iniciar_adocao`;
- coleta de dados;
- autorização de contato;
- WhatsApp;
- e-mail;
- `recusou_email`;
- validação do cadastro;
- encerramento do fluxo.

Schema:

```text
data/anjos-ia/adocao_schema.json
```

## 06 — Integração com Google Planilhas

Arquivo:

```text
docs/anjos-ia/06-integracao-google-sheets.md
```

Conteúdo:

- HTTP POST;
- Google Apps Script;
- Google Sheets;
- estrutura da planilha;
- geração de protocolo;
- status inicial da solicitação.

Código:

```text
src/anjos-ia/google-apps-script/Code.gs
```

Exemplo de payload:

```text
data/anjos-ia/exemplo_solicitacao_post.json
```

## 07 — Consulta de status

Arquivo:

```text
docs/anjos-ia/07-consulta-status.md
```

Conteúdo:

- `consultar_status`;
- consulta por e-mail ou WhatsApp;
- filtro opcional pelo animal;
- retorno do status;
- retorno do protocolo;
- tratamento de solicitação não encontrada.

Código auxiliar do Dify:

```text
src/anjos-ia/dify/ler_status.py
```

Schema:

```text
data/anjos-ia/consulta_status_schema.json
```

## 08 — Listagem de animais com fotos

Arquivo:

```text
docs/anjos-ia/08-listagem-animais-com-fotos.md
```

Conteúdo:

- `listar_animais`;
- busca de animais disponíveis;
- integração com perfil;
- fotos;
- Markdown;
- URLs diretas;
- limitação atual da recuperação semântica.

Prompt:

```text
src/anjos-ia/dify/prompt_listar_animais.md
```

Schema:

```text
data/anjos-ia/listagem_animais_schema.json
```

## 09 — Estado e preservação de variáveis

Arquivo:

```text
docs/anjos-ia/09-estado-e-preservacao-variaveis.md
```

Conteúdo:

- preservação de `interesse_animal`;
- reset de `quer_iniciar_adocao`;
- preservação e reset de `consultar_status`;
- preservação de `aceita_contato`;
- preservação de `recusou_email`;
- tratamento de `listar_animais`.

Schema:

```text
data/anjos-ia/estado_conversa_schema.json
```

## 10 — Testes do workflow

Arquivo:

```text
docs/anjos-ia/10-testes-workflow.md
```

Conteúdo:

- 17 casos de teste;
- resultados técnicos;
- erros encontrados;
- correções;
- cenários parciais;
- pendências;
- roteiro de teste ponta a ponta.

Casos de teste estruturados:

```text
data/anjos-ia/casos_teste_workflow.json
```

## 11 — Arquitetura e fluxo geral

Arquivo:

```text
docs/anjos-ia/11-arquitetura-fluxo-geral.md
```

Conteúdo:

- arquitetura do MVP;
- módulos;
- Dify;
- Gemini;
- Knowledge;
- Google Apps Script;
- Google Sheets;
- fluxo de adoção;
- consulta de status;
- controle de estado;
- limitações e evolução futura.

Diagrama Mermaid:

```text
src/anjos-ia/architecture/fluxo-geral.mmd
```

Schema:

```text
data/anjos-ia/arquitetura_mvp.json
```

---

# Principais variáveis

## Perfil

```text
perfil_especie
perfil_moradia
perfil_criancas
perfil_outros_animais
perfil_porte
perfil_idade
perfil_tempo_sozinho
perfil_rotina
perfil_quintal
perfil_atividade
```

## Interesse, adoção e status

```text
interesse_animal
especie_animal
adotante_nome
adotante_whatsapp
adotante_email
aceita_contato
recusou_email
quer_iniciar_adocao
consultar_status
listar_animais
```

---

# Fluxo resumido

```text
Usuário
  ↓
Coleta de perfil
  ↓
Identificação de intenção
  ↓
Recomendação ou listagem
  ↓
Escolha do animal
  ↓
Solicitação de adoção
  ↓
Google Apps Script
  ↓
Google Sheets
  ↓
Protocolo
  ↓
Consulta de status
```

---

# Histórico dos commits da Anjos IA

Todos os commits abaixo pertencem à branch `feature/anjos-ia`.

| Etapa | Commit | Descrição |
|---|---|---|
| 01 | `42ebea7` | `docs: registra desenvolvimento inicial da Anjos IA` |
| 02 | `7c97b61` | `feat: adiciona base de conhecimento da Anjos IA` |
| 03 | `089b27a` | `feat: documenta coleta de perfil do adotante` |
| 04 | `920c0cc` | `feat: documenta interesse e recomendação de animais` |
| 05 | `ac0c6cb` | `feat: documenta fluxo de solicitação de adoção` |
| 06 | `97bbfd7` | `feat: integra solicitações com Google Planilhas` |
| 07 | `9fe4e21` | `feat: implementa consulta de status da adoção` |
| 08 | `7da8b47` | `feat: adiciona fluxo de listagem de animais com fotos` |
| 09 | `e1afe69` | `fix: organiza preservação e reset de estado do workflow` |
| 10 | `c07828b` | `test: documenta testes funcionais da Anjos IA` |
| 11 | `7fbe9b8` | `docs: adiciona arquitetura e fluxo geral da Anjos IA` |

---

# Pendências atuais

As principais evoluções ainda previstas são:

1. impedir formalmente o início da adoção quando nenhum animal estiver selecionado;
2. concluir o fluxo de seleção do animal após a listagem;
3. tornar os filtros de espécie, porte e idade mais determinísticos;
4. substituir URLs de teste restantes por imagens diretas ou fotos oficiais;
5. revisar respostas sobre saúde e procedimentos para evitar informações não documentadas;
6. executar novo teste completo de regressão;
7. realizar validação com usuários reais;
8. preparar a futura integração da Anjos IA com o site.

## Observação

Os dados de animais utilizados atualmente são fictícios e destinados ao desenvolvimento e validação do MVP.

Resultados de validação com usuários reais devem ser registrados somente após a aplicação efetiva dos testes com o público-alvo.
