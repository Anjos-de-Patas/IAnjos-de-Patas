"""Gera a Versão Final (4.0) do Documento Técnico a partir da versão 3.0.

Preserva integralmente as seções 1 a 24 da versão 3.0, atualiza capa e folha de rosto,
acrescenta as seções 25 a 38 da TED 04 antes das referências e inclui as novas referências.
Uso: python src/gerar_documento_final.py   (depois converta para PDF no Word ou LibreOffice)
"""
import copy
from pathlib import Path
from docx import Document
from docx.shared import Cm

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs/TED03_Documento_Tecnico_v3.0.docx"
OUT = ROOT / "docs/TED04_Documento_Tecnico_Final_v4.0.docx"

d = Document(SRC)
ps = d.paragraphs
idx = {p.text.strip(): i for i, p in enumerate(ps)}
T_H1, T_H2 = ps[idx["24 CONCLUSÃO DA TED 03"]], ps[idx["21.6 LIMITAÇÕES, RISCOS E RELAÇÃO COM O MVP"]]
T_BODY = ps[idx["24 CONCLUSÃO DA TED 03"] + 1]
T_CAP = next(p for p in ps if p.text.startswith("Quadro 4 –"))
T_FONTE = ps[ps.index(T_CAP) + 1]
T_FIG = next(p for p in ps if p._p.xpath('.//w:drawing'))
T_REF = ps[idx["REFERÊNCIAS"] + 1]
TB2 = next(t for t in d.tables if t.rows[0].cells[0].text.strip().startswith("Questão"))
TB3 = next(t for t in d.tables if t.rows[0].cells[0].text.strip().startswith("Procedimento"))
ANCORA = ps[idx["REFERÊNCIAS"]]._p

def set_text(par_el, texto):
    from docx.text.paragraph import Paragraph
    p = Paragraph(par_el, T_BODY._parent)
    runs = p.runs
    if not runs:
        p.add_run(texto)
        return p
    runs[0].text = texto
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
    return p

def par(modelo, texto):
    el = copy.deepcopy(modelo._p)
    for dr in el.xpath('.//w:drawing'):
        dr.getparent().getparent().remove(dr.getparent())
    ANCORA.addprevious(el)
    return set_text(el, texto)

H1 = lambda t: par(T_H1, t)
H2 = lambda t: par(T_H2, t)
P = lambda t: par(T_BODY, t)
CAP = lambda t: par(T_CAP, t)
FONTE = lambda t="Fonte: elaborado pelos autores (2026).": par(T_FONTE, t)

def tabela(modelo, linhas):
    tb = copy.deepcopy(modelo._tbl)
    rows = tb.xpath('./w:tr')
    head, body = rows[0], rows[1]
    for r in rows[1:]:
        tb.remove(r)
    from docx.table import Table
    def fill(tr, valores):
        cells = tr.xpath('./w:tc')
        for c, v in zip(cells, valores):
            ps_c = c.xpath('./w:p')
            for extra in ps_c[1:]:
                c.remove(extra)
            set_text(ps_c[0], v)
    fill(head, linhas[0])
    for valores in linhas[1:]:
        tr = copy.deepcopy(body)
        tb.append(tr)
        fill(tr, valores)
    # mantém a tabela inteira junto da linha de fonte (keepNext em todas as linhas)
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    for pel in tb.xpath('.//w:p'):
        ppr = pel.get_or_add_pPr()
        if ppr.find(qn('w:keepNext')) is None:
            ppr.insert(0, OxmlElement('w:keepNext'))
    ANCORA.addprevious(tb)

def figura(caminho, legenda, largura_cm=16):
    CAP(legenda)
    el = copy.deepcopy(T_FIG._p)
    for r in el.xpath('./w:r'):
        el.remove(r)
    ANCORA.addprevious(el)
    from docx.text.paragraph import Paragraph
    Paragraph(el, T_BODY._parent).add_run().add_picture(str(caminho), width=Cm(largura_cm))
    FONTE("Fonte: elaborado pelos autores com base nos resultados das TEDs 03 e 04 (2026).")

# ---------- capa e folha de rosto ----------
for p in ps[:62]:
    for r in p.runs:
        if "Versão 3.0" in r.text:
            r.text = r.text.replace("Versão 3.0", "Versão Final (4.0)")
        if "TEDs 01, 02 e 03" in r.text:
            r.text = r.text.replace("TEDs 01, 02 e 03", "TEDs 01, 02, 03 e 04")
nat = next(p for p in ps[:62] if p.text.strip().startswith("Trabalho apresentado"))
set_text(nat._p, "Trabalho apresentado à disciplina de Big Data e Ciência de Dados do curso de Análise e "
         "Desenvolvimento de Sistemas do Centro Universitário de Balsas – UNIBALSAS. Versão final do Documento "
         "Técnico do Projeto, que reúne a seleção dos dados (TED 01), a limpeza e análise exploratória (TED 02), "
         "a modelagem com Machine Learning (TED 03) e a integração dos resultados, a análise ética e de proteção "
         "de dados e a comunicação por Data Storytelling (TED 04).")

# ---------- TED 04 ----------
H1("25 APRESENTAÇÃO DA VERSÃO FINAL E CONTEXTO DO PROBLEMA")
P("Esta é a versão final do Documento Técnico do IAnjos de Patas. As seções 1 a 24 reproduzem integralmente a "
  "versão 3.0 e registram, nessa ordem, a seleção dos dados (TED 01), a preparação e a análise exploratória "
  "(TED 02) e a modelagem com Machine Learning (TED 03). As seções 25 a 38 foram acrescentadas na TED 04 e "
  "integram esses resultados em uma única narrativa, analisam os aspectos éticos e de proteção de dados e "
  "apresentam as conclusões e as possibilidades de evolução da solução.")
P("O problema investigado permanece o mesmo definido no início do semestre: na Sociedade Protetora dos Animais "
  "Anjos de Patas, em Balsas (MA), as informações dos animais ficam dispersas e quem deseja adotar tem dificuldade "
  "de encontrar animais que correspondam às suas preferências e à sua rotina. A solução proposta no projeto de "
  "Inteligência Artificial é um catálogo web com busca em linguagem natural, em que a IA converte o pedido da "
  "pessoa em critérios estruturados e o sistema apresenta somente animais efetivamente cadastrados.")
P("Ao longo do semestre, essa proposta foi implementada pela equipe na aplicação web da ONG "
  "(https://anjos-de-patas.netlify.app). Nela, o assistente de adoção usa o Google Gemini para interpretar a "
  "conversa e consulta o banco de dados com filtros de espécie, idade, porte e convivência, sem inventar "
  "características. A pergunta que orienta esta versão final é, portanto: o que os dados públicos analisados "
  "ensinaram sobre a construção dessa busca, e quais cuidados eles exigem?")

H1("26 CONJUNTO DE DADOS UTILIZADO")
P("A base utilizada em todas as etapas foi a PetFinder.my mini, versão simplificada da competição PetFinder.my "
  "Adoption Prediction, distribuída no tutorial do TensorFlow sobre dados estruturados (seções 3 a 5). Ela contém "
  "11.537 anúncios históricos de cães e gatos da Malásia e 15 colunas: espécie, idade, raça, sexo, cores, porte, "
  "pelagem, vacinação, castração, saúde, taxa, descrição livre, quantidade de fotos e velocidade de adoção. A "
  "versão usada é identificada pelo SHA-256 registrado em data/manifesto_ted02.json.")
P("A relação com o problema é parcial e foi tratada assim desde a TED 01: a base permite estudar e testar filtros "
  "por características cadastradas, mas não representa os animais da Anjos de Patas, não contém temperamento nem "
  "convivência estruturados e não informa a disponibilidade atual. Como a licença de redistribuição não foi "
  "confirmada, os arquivos CSV não são publicados no repositório; o script src/obter_dados.py baixa a mesma versão "
  "a partir da fonte oficial, e o manifesto permite conferir a integridade.")

H1("27 PREPARAÇÃO E TRATAMENTO DOS DADOS")
P("A TED 02 verificou valores inválidos, espaços indevidos, descrições ausentes, repetições e valores extremos "
  "(seções 10 a 12). Não houve valores fora dos domínios esperados; foram encontradas 9 descrições ausentes, "
  "143 linhas integralmente repetidas excedentes, 78 idades iguais a zero e 235 perfis sem fotos. As respostas "
  "Not Sure de vacinação e castração foram mantidas como categoria própria, distinta de Sim e Não.")
P("A principal decisão de preparação foi revista durante o semestre e registrada na seção 19: a entrega inicial "
  "removia as repetições, mas, como a base não tem identificador original, linhas iguais podem ser animais "
  "diferentes. Na versão adotada, os 11.537 registros foram preservados e as repetições passaram a ser marcadas, "
  "o que permitiu agrupá-las na divisão dos dados da TED 03 e evitar vazamento entre treino e teste. Em 23/11/2026, "
  "a equipe executou novamente os scripts das TEDs 02 e 03 a partir da base baixada da fonte oficial, e os arquivos "
  "de resultados gerados foram idênticos aos versionados no repositório.")

H1("28 ANÁLISE EXPLORATÓRIA")
P("A análise exploratória (seções 12 a 16) mostrou uma base com predominância de cães (6.601 registros, cerca de "
  "57%) sobre gatos (4.936, cerca de 43%), porte médio como categoria mais frequente nas duas espécies (62,05% dos "
  "gatos e 75,03% dos cães) e idades concentradas nos primeiros meses de vida, com mediana de 4 meses e cauda "
  "longa de animais mais velhos. Também revelou incerteza relevante nos cuidados: 13,13% dos registros têm "
  "vacinação Not Sure e 11,64% têm castração Not Sure.")
P("Esses achados orientaram diretamente as etapas seguintes. O desbalanceamento entre espécies levou ao uso de "
  "linha de base majoritária e de F1-score macro na TED 03; as descrições repetidas levaram à divisão agrupada; e a "
  "incerteza nos cuidados levou à regra de que um pedido que exige vacinação confirmada não pode ser atendido por "
  "um registro Not Sure. A análise também deixou claro o que a base não permite afirmar: ela não mede "
  "convivência, não explica a velocidade de adoção e não pode ser generalizada para Balsas.")

H1("29 MODELAGEM DE MACHINE LEARNING")
P("A TED 03 conduziu dois experimentos complementares (seções 18 a 21). No Experimento A, um problema de "
  "classificação supervisionada binária, a descrição textual do anúncio foi usada para prever a espécie. Foram "
  "comparadas uma linha de base majoritária, Naive Bayes e Regressão Logística, ambos com TF-IDF, usando divisão "
  "estratificada e agrupada por descrição (8.074 registros de treino, 1.151 de validação e 2.303 de teste), escolha "
  "do modelo pelo F1-score macro na validação e avaliação única no teste.")
P("No Experimento B, sem variável-alvo, foi estudada a tarefa mais próxima do MVP: aplicar os filtros obrigatórios "
  "de um pedido e ordenar os candidatos pelas preferências opcionais. A ordenação por vizinhos mais próximos (k-NN "
  "com similaridade de cosseno sobre atributos codificados e texto) foi comparada com a ordem original do catálogo "
  "e com uma regra explícita que conta quantas preferências cada perfil atende, em 17 cenários escritos pela equipe.")

H1("30 RESULTADOS OBTIDOS")
P("A Tabela 16 reúne os principais resultados quantitativos, e a Figura 13 os apresenta de forma comparativa.")
CAP("Tabela 16 – Síntese dos resultados dos experimentos")
tabela(TB3, [["Experimento e medida", "Comparador", "Resultado principal"],
             ["A – F1-score macro no teste", "Linha de base: 36,42%", "Regressão Logística: 92,57% (acurácia 92,71%)"],
             ["A – F1-score macro sem termos de espécie", "Modelo no teste: 92,57%", "83,79% (análise de sensibilidade)"],
             ["A – Sobreajuste (treino final × teste)", "Teste: 92,57%", "Treino: 96,91% (diferença de 4,3 pontos)"],
             ["B – Preferências atendidas no top-5", "Ordem original: 41,04%", "Regra explícita e k-NN: 96,25% (empate em 16 de 16 cenários)"],
             ["B – Filtros obrigatórios respeitados", "—", "100% nos três procedimentos; 1 cenário sem candidatos"]])
FONTE("Fonte: elaborado pelos autores com base em reports/TED03 e reports/TED03_recomendacao (2026).")
figura(ROOT / "reports/TED04/figures/01_sintese_resultados.png", "Figura 13 – Síntese dos resultados: o modelo supera a linha de base em A, e em B a regra empata com o k-NN")

H1("31 INTERPRETAÇÃO INTEGRADA DOS RESULTADOS")
P("Lidos em conjunto, os resultados contam uma história coerente. O Experimento A mostra que o texto das "
  "descrições carrega informação útil: o classificador acerta a espécie em cerca de 93% dos casos, muito acima da "
  "linha de base. Mas a análise de sensibilidade e os termos de maior peso mostram que boa parte desse acerto vem "
  "de palavras explícitas como cat, kitten, dog e puppy, e que o modelo aprendeu também expressões em malaio "
  "típicas da base. O modelo é útil para conferir cadastros, não para entender pedidos em português.")
P("O Experimento B é o mais relevante para o problema. Para atributos estruturados e confirmados, uma regra simples "
  "e auditável produziu exatamente o mesmo resultado que o k-NN. A explicação é estrutural (seção 21.5): quando "
  "todos os perfis têm os mesmos campos codificados, a similaridade de cosseno passa a contar coincidências, que é "
  "o que a regra faz. Ou seja, o Machine Learning não trouxe ganho onde os dados já estão organizados.")
P("A conclusão integrada é que a IA deve ser usada onde há linguagem livre, para interpretar o pedido da pessoa, e "
  "que a decisão sobre quais animais mostrar deve ficar com filtros e regras sobre dados confirmados. Essa é "
  "justamente a arquitetura adotada no assistente da aplicação web: o modelo de linguagem interpreta a conversa, e "
  "a consulta ao banco aplica os filtros e apresenta no máximo três animais reais. A análise exploratória sustenta "
  "o mesmo cuidado ao mostrar que informações incertas, como Not Sure, não podem ser tratadas como confirmadas.")

H1("32 ANÁLISE ÉTICA")
P("A principal questão ética do projeto é o impacto de uma recomendação sobre a vida de um animal e de uma família. "
  "Um resultado incorreto pode levar uma pessoa a um animal incompatível com sua rotina e aumentar o risco de "
  "devolução. Por isso, a equipe definiu que nenhum modelo decide sobre adoções: as recomendações apenas orientam a "
  "busca, e a avaliação continua com a equipe da ONG, que conhece os animais e conduz a triagem.")
P("O Quadro 6 resume os riscos éticos identificados e as medidas adotadas ou recomendadas.")
CAP("Quadro 6 – Riscos éticos e medidas de mitigação")
tabela(TB2, [["Risco", "Medida adotada ou recomendada"],
             ["Inferir comportamento por raça, porte ou sexo", "Convivência e temperamento só são usados quando confirmados no cadastro; a ausência de informação nunca é tratada como compatibilidade"],
             ["Viés histórico e geográfico da base", "Resultados tratados como estudo; nenhuma métrica é apresentada como desempenho nos dados da ONG"],
             ["Viés de idioma (descrições em inglês e malaio)", "O classificador não é aplicado a textos em português; a busca do MVP usa campos estruturados"],
             ["Uso de AdoptionSpeed para priorizar animais", "Variável excluída dos modelos, para não favorecer perfis que historicamente foram adotados mais rápido"],
             ["Confiança excessiva na IA", "Comparação obrigatória com linha de base e com regra simples; o empate do Experimento B foi registrado"],
             ["Decisão automatizada sobre adoções", "O sistema não aprova, não reserva e não reprova pedidos; a decisão é humana"]])
FONTE()

H1("33 PRIVACIDADE E LGPD")
P("O conjunto PetFinder.my mini descreve animais e não contém colunas com dados de pessoas. A análise das "
  "descrições livres feita na TED 04, porém, mostrou que alguns anúncios incluem dados pessoais dos responsáveis: "
  "foram encontrados quatro textos com sequências de dígitos compatíveis com números de telefone, acompanhadas do "
  "primeiro nome de uma pessoa para contato. Trata-se de dados pessoais, ainda que publicados originalmente em "
  "anúncios públicos, e a Lei nº 13.709/2018 se aplica ao seu tratamento (BRASIL, 2018).")
P("As medidas já adotadas reduzem esse risco: os CSV com as descrições não são publicados no repositório, os "
  "arquivos de resultados (predições, top-5 e termos relevantes) não contêm o texto das descrições nem os números "
  "encontrados, e o uso dos dados é restrito ao estudo. Como cuidado adicional, recomenda-se limpar as saídas do "
  "notebook ted02_limpeza_eda.ipynb, que exibe trechos de descrições como exemplo, e mascarar números de telefone "
  "caso as descrições venham a ser usadas em novos experimentos.")
P("Na aplicação real da ONG, o tratamento de dados pessoais é central e exige mais cuidado do que a base de estudo. "
  "O Quadro 7 relaciona os princípios da LGPD às medidas existentes na solução.")
CAP("Quadro 7 – Princípios da LGPD e medidas na solução")
tabela(TB2, [["Princípio (art. 6º)", "Aplicação no projeto"],
             ["Finalidade", "Dados do interessado (nome, e-mail, telefone, cidade e relato da rotina) são usados apenas para a triagem da adoção, informada no formulário"],
             ["Necessidade", "O assistente não solicita dados pessoais; eles são pedidos só no formulário de interesse"],
             ["Transparência", "A pessoa acompanha a etapa do seu pedido na própria conta; a página de transparência mostra apenas totais"],
             ["Segurança", "Autenticação, segurança em nível de linha no banco e notas internas restritas à equipe"],
             ["Prevenção", "As conversas com o assistente não são gravadas no banco de dados"],
             ["Não discriminação", "Nenhum perfil de pessoa é pontuado por modelo; a avaliação é feita pela equipe"]])
FONTE()
P("A anonimização dos dados não elimina todos os riscos: descrições livres, combinadas com cidade e características "
  "raras de um animal, podem permitir identificar pessoas. Por isso, futuros experimentos com dados da ONG devem "
  "partir de uma base autorizada, com campos mínimos, descrições revisadas e acesso controlado.")

H1("34 LIMITAÇÕES DOS DADOS, DAS ANÁLISES E DOS MODELOS").paragraph_format.page_break_before = True
CAP("Quadro 8 – Principais limitações identificadas")
tabela(TB2, [["Dimensão", "Limitação"],
             ["Dados", "Base histórica e estrangeira; sem identificador original, sem disponibilidade atual e sem temperamento ou convivência estruturados"],
             ["Qualidade", "Descrições curtas, multilíngues ou ausentes; respostas Not Sure; 7 grupos de textos iguais com espécies diferentes"],
             ["Análise exploratória", "Frequências descritivas, sem inferência causal; não podem ser generalizadas para Balsas"],
             ["Experimento A", "Dependência de termos explícitos de espécie e de vocabulário em malaio; tarefa distante da recomendação"],
             ["Experimento B", "17 cenários escritos pela equipe; métrica calculada sobre os mesmos campos usados na ordenação; sem avaliação por adotantes"],
             ["Validação", "Nenhum teste com frases abertas em português nem com dados reais e autorizados da ONG"]])
FONTE()
P("Essas limitações não invalidam o trabalho, mas definem o alcance das conclusões: os resultados sustentam "
  "decisões de arquitetura e de cuidado com os dados, e não afirmações sobre o desempenho da solução com os "
  "animais e os adotantes da Anjos de Patas.")

H1("35 DATA STORYTELLING")
P("A comunicação final dos resultados foi organizada como uma narrativa em que cada etapa responde a uma pergunta "
  "e prepara a seguinte, seguindo a sequência problema, dados, análise, resultados, interpretação, "
  "responsabilidade, solução e próximos passos (KNAFLIC, 2019). O Quadro 9 resume essa narrativa, que estrutura a "
  "apresentação final disponível em presentation/apresentacao-final.pdf.")
CAP("Quadro 9 – Narrativa dos resultados")
tabela(TB2, [["Momento da narrativa", "Mensagem e evidência"],
             ["O problema", "Pessoas não encontram animais compatíveis porque as informações estão dispersas"],
             ["Os dados", "11.537 anúncios públicos permitem estudar filtros, mas não representam os animais da ONG"],
             ["A análise", "Dados desbalanceados, repetidos e com incerteza (Not Sure) exigem cuidados antes de modelar"],
             ["Os resultados", "O texto identifica a espécie com F1 de 92,57%, mas para atributos estruturados a regra empata com o k-NN"],
             ["A interpretação", "A IA deve interpretar a linguagem; filtros e regras devem decidir o que é mostrado"],
             ["A responsabilidade", "Dados pessoais em descrições, vieses de idioma e de origem e decisão sempre humana"],
             ["A solução", "O assistente da aplicação web aplica essa arquitetura e mostra só animais reais"],
             ["Os próximos passos", "Testar frases em português e avaliar relevância com dados autorizados da ONG"]])
FONTE()
P("A Figura 13 foi escolhida como gráfico central da narrativa porque sustenta, em uma única imagem, as duas "
  "conclusões principais: o ganho do modelo sobre a linha de base no Experimento A e o empate entre regra e k-NN "
  "no Experimento B. Os demais gráficos das TEDs 02 e 03 são usados apenas quando explicam um achado específico.")

H1("36 CONCLUSÕES")
P("O projeto mostrou que é possível transformar uma base pública em conhecimento útil para uma solução real, desde "
  "que se reconheça com clareza o que os dados permitem e o que não permitem afirmar. A preparação rastreável da "
  "TED 02 tornou possível uma avaliação honesta na TED 03, sem vazamento entre treino e teste e com resultados "
  "reproduzidos de forma idêntica nesta etapa.")
P("Em resposta ao problema inicial, os resultados indicam que a busca por animais compatíveis deve combinar duas "
  "partes: um modelo de linguagem para interpretar o pedido em português e filtros e regras transparentes sobre "
  "dados confirmados para escolher o que mostrar. O Machine Learning clássico teve bom desempenho na tarefa textual, "
  "mas não superou uma regra simples nos atributos estruturados, e esse resultado orientou a arquitetura adotada na "
  "aplicação da ONG. Permanecem em aberto a qualidade da interpretação de frases reais em português e a percepção de "
  "relevância pelos adotantes, que dependem de dados e testes que esta base não oferece.")

H1("37 POSSIBILIDADES DE EVOLUÇÃO DA SOLUÇÃO")
P("A evolução recomendada começa pela construção de um conjunto de avaliação próprio, com frases reais em português "
  "e os critérios esperados revisados pela equipe, para medir a interpretação do assistente com a meta de 80% de "
  "concordância definida no projeto de IA. Em seguida, com autorização da ONG, os cadastros locais podem substituir "
  "a base estrangeira, incluindo campos confirmados de temperamento e convivência.")
P("Com esses dados, será possível reavaliar a ordenação por similaridade textual, agora em português, e verificar "
  "se ela traz ganho sobre as regras em preferências subjetivas, como “calmo” ou “brincalhão”. Outras evoluções "
  "possíveis são o uso do classificador apenas como alerta de inconsistência entre descrição e espécie cadastrada, o "
  "mascaramento automático de dados pessoais em textos livres e a coleta de retorno dos adotantes sobre a "
  "relevância das sugestões, sempre com a decisão final mantida pela equipe da ONG.")

H1("38 HISTÓRICO DE VERSÕES").paragraph_format.page_break_before = True
CAP("Quadro 10 – Histórico de versões do Documento Técnico")
tabela(TB2, [["Versão", "Conteúdo"],
             ["1.0 – setembro/2026 (TED 01)", "Problema, necessidades de dados, comparação de alternativas, seleção e avaliação preliminar da PetFinder.my mini"],
             ["2.0 – setembro/2026 (TED 02)", "Limpeza, tratamentos justificados, estatísticas e análise exploratória"],
             ["3.0 – novembro/2026 (TED 03)", "Revisão da preparação, Experimentos A e B de Machine Learning, resultados e reprodutibilidade"],
             ["4.0 final – dezembro/2026 (TED 04)", "Integração dos resultados, ética, privacidade e LGPD, limitações, Data Storytelling, conclusões e evolução"]])
FONTE()

# ---------- referências ----------
refs = [p for p in d.paragraphs if p._p.getparent() is ANCORA.getparent()]
novas = {
    "BRASIL": ("BRASIL. ", "Lei nº 13.709, de 14 de agosto de 2018", ". Lei Geral de Proteção de Dados Pessoais (LGPD). Brasília, DF: Presidência da República, 2018. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm. Acesso em: 23 nov. 2026."),
    "KNAFLIC": ("KNAFLIC, Cole Nussbaumer. ", "Storytelling com dados", ": um guia sobre visualização de dados para profissionais de negócios. Rio de Janeiro: Alta Books, 2019."),
}
lista = d.paragraphs
i_ref = next(i for i, p in enumerate(lista) if p.text.strip() == "REFERÊNCIAS")
existentes = [p for p in lista[i_ref + 1:] if p.text.strip()]
for chave, partes in novas.items():
    texto = "".join(partes)
    depois = next((p for p in existentes if p.text.strip() > texto), None)
    el = copy.deepcopy(T_REF._p)
    (depois._p.addprevious if depois else existentes[-1]._p.addnext)(el)
    pr = set_text(el, partes[0])
    base = pr.runs[0]
    for k, trecho in enumerate(partes[1:]):
        r = copy.deepcopy(base._r); el.append(r)
        from docx.text.run import Run
        run = Run(r, pr); run.text = trecho; run.bold = (k == 0)
    base.bold = False

d.save(OUT)
print("Documento salvo em", OUT)
