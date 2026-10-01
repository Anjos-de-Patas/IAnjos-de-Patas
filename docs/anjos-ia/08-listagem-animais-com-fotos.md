# 08 - Listagem de animais disponíveis com fotos

## Objetivo

Esta etapa registra o fluxo específico criado para permitir que o usuário peça para ver os animais disponíveis para adoção, com nome, foto e informações básicas.

Esse fluxo foi criado depois de testes em que o usuário pediu uma lista de animais e a Anjos IA respondeu que não possuía uma listagem disponível.

## Nova intenção

Foi criada a variável:

```text
listar_animais
```

Ela recebe `sim` quando o usuário pede para ver ou listar animais disponíveis.

Exemplos:

```text
"Quais animais estão disponíveis?"       -> sim
"Me mostra os cachorros disponíveis."    -> sim
"Quero ver gatos para adoção."           -> sim
"Tem algum filhote disponível?"          -> sim
```

Ela recebe `não` quando o usuário fala sobre um animal específico ou sobre outro assunto.

## Fluxo criado

O fluxo específico ficou organizado assim:

```text
Extrator de interesse
        ↓
Atribuidor de Variáveis Interesse
        ↓
SE/SENÃO - LISTAR ANIMAIS
        ├── listar_animais = sim
        │      ↓
        │  Modelo - CONSULTA LISTA DE ANIMAIS
        │      ↓
        │  Recuperação - LISTA DE ANIMAIS
        │      ↓
        │  LLM - LISTAR ANIMAIS
        │      ↓
        │  Resposta - LISTA DE ANIMAIS
        │
        └── caso contrário
               ↓
           fluxo normal
```

## Consulta baseada no perfil

O nó **Modelo - CONSULTA LISTA DE ANIMAIS** recebe informações já coletadas do perfil:

- espécie;
- porte;
- idade;
- moradia;
- outros animais;
- crianças;
- nível de atividade.

Exemplo de consulta:

```text
BUSCA DE ANIMAIS PARA ADOÇÃO

Filtros obrigatórios:
status: Disponível
especie: cachorro
porte: pequeno
idade_categoria: filhote

Preferências adicionais:
moradia_recomendada:
convivência com outros animais:
convivência com crianças:
nivel_atividade:
```

## Recuperação de conhecimento

O nó **Recuperação - LISTA DE ANIMAIS** consulta a base:

```text
Base_Teste_Anjos_de_Patas_com_Fotos
```

Configurações testadas:

- consulta gerada pelo modelo de busca;
- recuperação por similaridade;
- Top K inicialmente em 5;
- posteriormente alterado para 10 durante os testes;
- filtro de metadados desativado.

O retorno da recuperação inclui o conteúdo do animal e seus campos, entre eles `foto_url`.

## LLM responsável pela listagem

O nó **LLM - LISTAR ANIMAIS** utiliza o resultado da recuperação como contexto.

Regras principais:

- usar somente informações presentes no contexto;
- exibir somente animais com status `Disponível`;
- mostrar no máximo 3 animais por resposta;
- priorizar opções compatíveis com o perfil;
- mostrar nome, foto, espécie, porte, idade e descrição curta;
- utilizar exatamente o valor de `foto_url`;
- não inventar nem modificar URLs;
- não mostrar animal sem foto;
- perguntar ao final qual animal o usuário deseja conhecer melhor.

## Formato da foto

A resposta utiliza Markdown:

```markdown
![Nome do animal](URL_EXATA_DA_FOTO)
```

Exemplo:

```markdown
![Thor](https://upload.wikimedia.org/wikipedia/commons/d/d5/Old_English_Sheep_Dog.JPG)
```

## Problema encontrado com as imagens

Inicialmente, a base utilizava URLs do domínio:

```text
loremflickr.com
```

Nos testes do Dify essas imagens não eram renderizadas corretamente, pois o endereço podia redirecionar antes de entregar o arquivo da imagem.

Foram realizados testes com URLs diretas do Wikimedia Commons.

As imagens diretas passaram a renderizar corretamente no preview do Dify.

Foram atualizadas nos testes as fotos de:

- Bento;
- Mel;
- Thor.

## Exemplo de resposta esperada

```markdown
### Thor

![Thor](https://upload.wikimedia.org/wikipedia/commons/d/d5/Old_English_Sheep_Dog.JPG)

- Espécie: Cachorro
- Porte: Médio
- Idade: Adulto
- Descrição: Ativo e companheiro. Gosta de brincadeiras e passeios.

### Mel

![Mel](https://upload.wikimedia.org/wikipedia/commons/4/4e/Picture_of_Chihuahua_dog.jpg)

- Espécie: Cachorro
- Porte: Pequeno
- Idade: Adulta
- Descrição: Muito carinhosa e sociável. Prefere rotinas tranquilas e companhia.
```

## Limitação observada na recuperação

Foi identificado um problema importante durante os testes.

Para a consulta:

```text
Quero ver cachorros pequenos e filhotes disponíveis para adoção.
```

o perfil estava corretamente preenchido com:

```text
especie = cachorro
porte = pequeno
idade = filhote
```

Mesmo assim, a recuperação semântica retornou Thor e Mel em vez de priorizar Bento, que corresponde melhor aos filtros estruturados.

O aumento do Top K de 5 para 10 não resolveu completamente esse comportamento.

Por isso, foi registrada como melhoria futura a possibilidade de aplicar filtragem determinística ou metadados estruturados antes da etapa de geração da resposta.

## Relação com a seleção do animal

O fluxo de listagem deve servir como etapa anterior ao início da adoção.

Fluxo desejado:

```text
usuário pede animais
        ↓
lista com fotos
        ↓
usuário escolhe um animal
        ↓
interesse_animal é preenchido
        ↓
usuário decide se quer iniciar adoção
        ↓
fluxo formal de adoção
```

## Estado atual

A listagem com fotos foi testada com sucesso no preview do Dify.

A renderização de imagens diretas está funcionando.

A principal melhoria pendente desta etapa é tornar o filtro por espécie, porte e idade mais determinístico, reduzindo a dependência exclusiva da recuperação semântica.
