# Método e evidências da inspeção

Consulta e execução em 16/09/2026. Foi baixado o ZIP publicado em https://storage.googleapis.com/download.tensorflow.org/data/petfinder-mini.zip, extraído o CSV e lido o README interno. O arquivo foi analisado com `src/inspecionar_dados.py`; os resultados estão em `inspecao.json`. 

Foram consultados: documentação do TensorFlow (https://www.tensorflow.org/tutorials/structured_data/preprocessing_layers), catálogo técnico da PetFinder original (https://www.tensorflow.org/datasets/catalog/pet_finder), página da competição (https://www.kaggle.com/competitions/petfinder-adoption-prediction/data) e metadados de Austin (https://data.austintexas.gov/api/views/9t4d-g238.json). A página dinâmica do Kaggle não forneceu seu texto completo nesta consulta; o original foi comparado apenas pela documentação técnica acessível. Não foi executada inspeção integral das duas alternativas não selecionadas.

Austin: foi consultada a versão histórica 9t4d-g238. O esquema possui Animal ID, Date of Birth, Name, DateTime, MonthYear, Outcome Type, Outcome Subtype, Animal Type, Sex upon Outcome, Age upon Outcome, Breed e Color. Os metadados indicam Public Domain. Embora útil para estudar saídas do abrigo, não possui coluna de porte e tem menor cobertura dos filtros previstos.

A PetFinder mini foi escolhida por permitir testar espécie, sexo, porte e idade em um CSV acessível e inspecionado. A ausência de comportamento, convivência, ID original e situação atual limita a aplicação. O atributo Age representa a idade do animal em meses. Nenhuma conversão para faixas etárias foi realizada nesta etapa.

Vazio: texto de comprimento zero após remover espaços. Duplicata excedente: linha idêntica nas 15 colunas após a primeira ocorrência. Not Sure é contado separadamente, não como vazio ou Não. Não foram removidas linhas nem preenchidas lacunas. Os totais não provam unicidade de animais. Não se realizou leitura humana completa dos textos, teste da IA, avaliação clínica ou validação com adotantes.

A análise utilizou dados históricos e não recebeu cadastros atuais da ONG. A meta de 80% do MVP continua sendo hipótese a testar. Não foram criados resultados de validação fictícios.
