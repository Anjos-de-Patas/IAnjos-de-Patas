# 13 - Exportação e versionamento do workflow do Dify

## Objetivo

Preparar o repositório para armazenar uma exportação real do workflow da Anjos IA diretamente do Dify.

Até esta etapa, o repositório já contém documentação, schemas, prompts, código auxiliar e integrações. O que ainda falta para tornar o projeto mais reproduzível é guardar também a definição completa do workflow exportado pela própria plataforma.

## Arquivo esperado

Quando o workflow for exportado do Dify, o arquivo deve ser salvo em:

```text
src/anjos-ia/dify/workflow/anjos-ia-workflow.yml
```

Se a versão do Dify exportar como `.yaml`, pode ser usado:

```text
src/anjos-ia/dify/workflow/anjos-ia-workflow.yaml
```

## Como exportar no Dify

No Dify:

1. abra a aplicação **Anjos IA**;
2. abra o workflow atual;
3. procure a opção de exportação da aplicação/workflow;
4. exporte o arquivo DSL/YAML;
5. salve o arquivo sem alterar manualmente o conteúdo;
6. adicione o arquivo na pasta indicada acima.

## O que o arquivo deve representar

A exportação deve refletir a versão atual contendo, quando presentes no workflow:

- nó inicial;
- coleta de perfil;
- extratores de parâmetros;
- atribuidores de variáveis;
- identificação de interesse;
- fluxo normal;
- recomendação;
- consulta à base de conhecimento;
- listagem de animais;
- exibição das fotos;
- fluxo de adoção;
- coleta dos dados do adotante;
- integração HTTP;
- consulta de status;
- nós de reset de estado;
- respostas finais.

## Cuidados antes do commit

Antes de versionar o arquivo exportado, revisar se ele contém:

- tokens;
- chaves de API;
- segredos;
- credenciais;
- URLs privadas com dados sensíveis.

Se algum segredo estiver embutido no arquivo, ele deve ser removido do versionamento e configurado pela plataforma ou por variável segura.

## Estratégia de versionamento

Sempre que houver mudança importante no workflow:

```text
alterar no Dify
→ testar
→ exportar novamente
→ substituir o YAML no repositório
→ criar commit descrevendo a mudança
```

Exemplos de commits:

```text
feat: adiciona guarda de adoção sem animal selecionado
fix: corrige seleção do animal após listagem
fix: melhora filtro de espécie porte e idade
refactor: reorganiza fluxo de intenções no Dify
```

## Situação atual

A estrutura do repositório está preparada para receber o arquivo real.

O YAML não foi criado manualmente porque isso não representaria fielmente o workflow existente no Dify. O próximo passo é exportar o DSL diretamente da plataforma e versionar o arquivo original.
