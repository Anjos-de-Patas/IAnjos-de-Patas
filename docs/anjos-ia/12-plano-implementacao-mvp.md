# 12 - Plano de implementação do MVP

## Objetivo

Este documento organiza o estado atual da Anjos IA em três grupos: concluído, parcial e pendente. Ele serve como guia para os próximos commits e para a preparação da validação final do MVP.

## Concluído

### Perfil do adotante

- coleta progressiva;
- variáveis de perfil;
- persistência entre mensagens;
- uma pergunta por vez;
- reaproveitamento das informações já fornecidas.

### Interesse e recomendação

- identificação de animal específico;
- recuperação pela base de conhecimento;
- regras para evitar invenção de informações;
- tratamento de animal indisponível;
- alternativas limitadas.

### Solicitação de adoção

- identificação da intenção de iniciar adoção;
- coleta de nome;
- coleta de WhatsApp;
- coleta de e-mail;
- recusa de e-mail;
- autorização de contato;
- preservação das variáveis durante o cadastro.

### Persistência

- integração HTTP;
- Google Apps Script;
- Google Sheets;
- armazenamento dos dados;
- status inicial;
- geração automática de protocolo.

### Consulta de status

- consulta por e-mail;
- consulta por WhatsApp;
- filtro opcional pelo animal;
- retorno de status e protocolo;
- tratamento de solicitação não encontrada.

### Listagem

- intenção `listar_animais`;
- recuperação da base;
- apresentação de até 3 animais;
- fotos em Markdown;
- URLs diretas testadas com sucesso.

### Controle de estado

- preservação de `interesse_animal`;
- reset de `quer_iniciar_adocao`;
- preservação e reset de `consultar_status`;
- preservação de `aceita_contato`;
- preservação de `recusou_email`.

## Parcial

### Filtro de animais

A recuperação semântica ainda não garante correspondência exata entre:

- espécie;
- porte;
- idade.

Exemplo observado: Bento não foi priorizado em uma busca por cachorro pequeno e filhote.

Melhoria planejada:

```text
perfil estruturado
   ↓
filtro determinístico
   ↓
animais compatíveis
   ↓
LLM apenas para apresentação
```

### Seleção após listagem

A listagem funciona, mas a transição entre:

```text
lista
→ escolha do animal
→ interesse_animal
→ adoção
```

ainda precisa ser refinada e testada ponta a ponta.

### Bloqueio de adoção sem animal

O comportamento desejado está definido, mas deve ser garantido formalmente em todos os caminhos do workflow:

```text
quer_iniciar_adocao = sim
E
interesse_animal vazio
```

deve direcionar o usuário para seleção/listagem antes do cadastro.

## Pendente

- substituir todas as imagens de teste por links diretos confiáveis;
- revisar prompts sobre saúde e procedimentos da ONG;
- eliminar qualquer resposta não fundamentada sobre etapas internas;
- repetir todos os testes depois das últimas alterações;
- executar validação com usuários reais;
- registrar resultados da validação acadêmica;
- preparar integração com o site.

## Ordem recomendada dos próximos passos

1. implementar filtro determinístico;
2. concluir seleção pós-listagem;
3. adicionar guarda contra adoção sem animal;
4. revisar prompts de segurança e fidelidade ao contexto;
5. executar regressão completa;
6. corrigir problemas encontrados;
7. aplicar teste com público-alvo;
8. registrar evidências;
9. atualizar documentação final;
10. preparar integração futura com o site.

## Critério para considerar o MVP pronto para validação

O MVP poderá ser considerado pronto para a validação com usuários quando for possível executar sem interrupções o seguinte cenário:

```text
iniciar conversa
→ preencher perfil
→ pedir animais
→ visualizar fotos
→ selecionar animal
→ iniciar adoção
→ informar dados
→ receber protocolo
→ consultar status
→ retornar ao fluxo normal
```

## Fora do escopo atual

Nesta etapa não fazem parte do MVP:

- painel administrativo próprio;
- banco de dados dedicado;
- autenticação de usuários;
- integração oficial com WhatsApp;
- integração definitiva com o site;
- gestão completa dos animais pela ONG.

Essas funcionalidades podem ser tratadas em versões futuras.
