# Workflow do Dify

Esta pasta é destinada à exportação oficial do workflow da **Anjos IA**.

## Arquivo principal esperado

```text
anjos-ia-workflow.yml
```

ou, dependendo da versão do Dify:

```text
anjos-ia-workflow.yaml
```

## Importante

Não criar manualmente um YAML fingindo ser uma exportação do Dify.

O arquivo desta pasta deve ser gerado pela própria plataforma para representar corretamente:

- nós;
- conexões;
- variáveis;
- condições;
- modelos;
- prompts;
- recuperação de conhecimento;
- chamadas HTTP;
- respostas;
- configurações do workflow.

## Segurança

Antes do commit, verificar se a exportação contém qualquer credencial ou segredo.

Segredos não devem ser versionados.

## Documentação

Veja:

```text
docs/anjos-ia/13-export-workflow-dify.md
```
