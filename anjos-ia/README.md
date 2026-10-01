# Anjos IA

Agente conversacional do projeto **IAnjos de Patas**, desenvolvido para apoiar o processo de adoção de animais.

> Esta pasta reúne apenas os materiais específicos da Anjos IA. O desenvolvimento está sendo versionado na branch `feature/anjos-ia`, separadamente da `main`.

## Objetivo

A Anjos IA foi criada para:

- conversar com pessoas interessadas em adoção;
- coletar preferências do adotante;
- apresentar animais disponíveis;
- exibir fotos e informações básicas;
- registrar interesse em adoção;
- coletar dados de contato;
- gerar protocolo;
- permitir consulta do status da solicitação.

## Tecnologias

- Dify
- Gemini 3.5 Flash
- Knowledge do Dify
- Google Apps Script
- Google Sheets
- GitHub

## Fluxo principal

```text
Usuário
  ↓
Coleta de perfil
  ↓
Listagem / recomendação
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

## Funcionalidades já implementadas

- [x] coleta progressiva do perfil;
- [x] persistência das variáveis de conversa;
- [x] identificação de interesse por animal;
- [x] consulta à base de conhecimento;
- [x] recomendação de animais;
- [x] listagem de animais disponíveis;
- [x] exibição de fotos em Markdown;
- [x] coleta de nome, WhatsApp e e-mail;
- [x] tratamento de recusa de e-mail;
- [x] autorização de contato;
- [x] registro da solicitação no Google Sheets;
- [x] protocolo automático no padrão `ADP-XXXX`;
- [x] consulta de status;
- [x] reset das variáveis de controle;
- [x] documentação de testes técnicos;
- [x] documentação da arquitetura.

## Funcionalidades em melhoria

- [ ] bloquear formalmente adoção sem animal selecionado;
- [ ] concluir a seleção do animal após a listagem;
- [ ] melhorar filtros exatos por espécie, porte e idade;
- [ ] substituir URLs de teste restantes por imagens diretas;
- [ ] revisar respostas sobre saúde e procedimentos;
- [ ] executar novo teste de regressão ponta a ponta;
- [ ] validar a solução com usuários reais;
- [ ] integrar futuramente a Anjos IA ao site.

## Estrutura dos arquivos

```text
anjos-ia/
└── README.md

docs/anjos-ia/
├── README.md
├── 02-base-conhecimento.md
├── 03-coleta-perfil.md
├── 04-interesse-recomendacao.md
├── 05-fluxo-solicitacao-adocao.md
├── 06-integracao-google-sheets.md
├── 07-consulta-status.md
├── 08-listagem-animais-com-fotos.md
├── 09-estado-e-preservacao-variaveis.md
├── 10-testes-workflow.md
├── 11-arquitetura-fluxo-geral.md
└── 12-plano-implementacao-mvp.md

data/anjos-ia/
├── base_teste_animais_com_fotos.csv
├── perfil_adotante_schema.json
├── interesse_recomendacao_schema.json
├── adocao_schema.json
├── exemplo_solicitacao_post.json
├── consulta_status_schema.json
├── listagem_animais_schema.json
├── estado_conversa_schema.json
├── casos_teste_workflow.json
└── arquitetura_mvp.json

src/anjos-ia/
├── dify/
│   ├── ler_status.py
│   └── prompt_listar_animais.md
├── google-apps-script/
│   └── Code.gs
└── architecture/
    └── fluxo-geral.mmd
```

## Base de teste

Os animais utilizados atualmente são fictícios e servem somente para desenvolvimento e validação do MVP.

Antes de uso real, a base deve ser substituída pelos dados reais e autorizados pela ONG.

## Documentação detalhada

A documentação técnica completa está em:

```text
docs/anjos-ia/README.md
```

## Branch de desenvolvimento

```text
feature/anjos-ia
```

As alterações específicas da Anjos IA devem continuar sendo feitas nessa branch enquanto o MVP estiver em desenvolvimento.
