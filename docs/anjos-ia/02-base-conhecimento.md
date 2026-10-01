# 02 - Base de conhecimento da Anjos IA

## Objetivo

Esta etapa registra a criação e organização da base de conhecimento usada pela Anjos IA para consultar, recomendar e listar animais disponíveis para adoção.

## O que foi implementado

- criação de uma base fictícia com 10 animais para testes do MVP;
- padronização dos principais atributos usados nas recomendações;
- inclusão de status de adoção para diferenciar animais disponíveis e já adotados;
- inclusão de informações de convivência com gatos, cães e crianças;
- inclusão de dados de moradia recomendada, nível de atividade e tempo sozinho;
- inclusão de informações básicas de saúde, vacinação e castração;
- inclusão dos campos `foto_url` e `foto_markdown` para permitir exibição de imagens no chat;
- preparação da base para uso no módulo Knowledge do Dify;
- testes de recuperação de registros pelo Dify.

## Estrutura dos dados

| Campo | Finalidade |
|---|---|
| `id` | identificador único do animal |
| `nome` | nome exibido ao usuário |
| `especie` | cachorro ou gato |
| `sexo` | sexo do animal |
| `porte` | pequeno, médio ou grande |
| `idade_categoria` | filhote, adulto ou idoso |
| `idade_anos` | idade aproximada |
| `raca` | raça ou SRD |
| `descricao` | resumo do comportamento |
| `temperamento` | característica comportamental principal |
| `convive_gatos` | compatibilidade registrada com gatos |
| `convive_caes` | compatibilidade registrada com cães |
| `convive_criancas` | convivência registrada com crianças |
| `moradia_recomendada` | tipo de ambiente indicado no conjunto de testes |
| `nivel_atividade` | nível de atividade do animal |
| `tempo_sozinho` | tempo de referência usado nos testes |
| `saude` | informação de saúde presente na ficha |
| `vacinado` | situação de vacinação |
| `castrado` | situação de castração |
| `status` | Disponível ou Adotado |
| `foto_url` | URL pública da imagem |
| `foto_markdown` | marcação Markdown para exibição da foto |

## Integração com o Dify

A base foi adicionada ao recurso de Conhecimento do Dify. Nos testes, a recuperação foi utilizada para responder a consultas como:

- "Quais animais estão disponíveis para adoção?"
- "Quero ver cachorros pequenos e filhotes."
- "Quais gatos estão disponíveis?"
- consultas sobre um animal específico.

A recuperação fornece ao LLM dados como nome, espécie, porte, idade, status e URL da foto.

## Fotos

Durante os testes foi identificado que URLs do `loremflickr.com` nem sempre eram renderizadas no chat do Dify. Por isso, foram testadas URLs diretas de arquivos no Wikimedia Commons.

Já foram substituídas na base de teste as URLs de:

- Bento;
- Mel;
- Thor.

As demais URLs ainda são de teste e podem ser substituídas por imagens diretas ou pelas fotos oficiais dos animais quando o projeto estiver com dados reais.

## Regra de negócio importante

A Anjos IA deve apresentar somente animais com:

```text
status: Disponível
```

Um animal com status `Adotado` pode permanecer na base para testar o fluxo de indisponibilidade, mas não deve ser oferecido como opção de adoção.

## Limitações atuais

Esta base é fictícia e foi criada apenas para desenvolvimento e validação do MVP. Antes de uso real, os registros devem ser substituídos pelos dados fornecidos e autorizados pela ONG.

Também foi observado que a recuperação semântica do Dify não equivale a um filtro SQL exato. Por isso, filtros e regras adicionais no workflow continuam sendo necessários para garantir que os animais exibidos correspondam às preferências informadas pelo usuário.

## Arquivo

A base utilizada nesta etapa está versionada em:

```text
data/anjos-ia/base_teste_animais_com_fotos.csv
```
