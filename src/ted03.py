"""TED 03 - ML supervisionado em descrições da base PetFinder.my mini.

Execução: python src/ted03.py
Separa por grupos de descrições iguais antes da vetorização, evita vazamento.
Não prevê compatibilidade, disponibilidade ou aprovação de adoção.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import platform
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, classification_report,
                             confusion_matrix, f1_score, precision_recall_fscore_support)
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
COLS = ['Cat', 'Dog']
SEED = 42


def normalized_group(text: str) -> str:
    # Mesmas descrições normalizadas permanecem sempre no mesmo conjunto.
    text = unicodedata.normalize('NFKC', str(text)).casefold()
    text = ' '.join(text.split())
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def clean_text(s: pd.Series) -> pd.Series:
    return s.fillna('').astype(str).str.strip()


def metrics(y, pred):
    p, r, f, sup = precision_recall_fscore_support(y, pred, labels=COLS, zero_division=0)
    return {'n': int(len(y)), 'accuracy': float(accuracy_score(y, pred)),
            'f1_macro': float(f1_score(y, pred, average='macro', labels=COLS, zero_division=0)),
            'classes': {lab: {'precision': float(p[i]), 'recall': float(r[i]),
                              'f1': float(f[i]), 'suporte': int(sup[i])}
                        for i, lab in enumerate(COLS)}}


def logistic():
    return Pipeline([('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2,
                    max_features=25000, sublinear_tf=True, strip_accents='unicode')),
                    ('model', LogisticRegression(max_iter=1500, class_weight='balanced',
                                                random_state=SEED))])


def naive_bayes():
    return Pipeline([('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2,
                    max_features=25000, sublinear_tf=True, strip_accents='unicode')),
                    ('model', MultinomialNB(alpha=1.0))])


def plot_bar_labels(ax, bars):
    for b in bars:
        ax.annotate(f'{b.get_height():.0f}' if b.get_height()>=2 else f'{b.get_height():.3f}', (b.get_x()+b.get_width()/2,b.get_height()),
                    xytext=(0,4), textcoords='offset points', ha='center', va='bottom',fontsize=9)


def save_figures(report: dict, ytest, pred, out: Path):
    fig_dir = out / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    counts = report['distribuicao']
    fig, ax = plt.subplots(figsize=(8,4))
    bars=ax.bar(['Treino','Validação','Teste'], [counts[k]['total'] for k in ['treino','validacao','teste']])
    plot_bar_labels(ax,bars)
    ax.set_title('TED 03 - Quantidade de registros por conjunto')
    ax.set_ylabel('Registros')
    fig.tight_layout(); fig.savefig(fig_dir/'01_divisao_dados.png',dpi=160);plt.close(fig)

    metric=report['validacao']; mnames=list(metric)
    fig, ax=plt.subplots(figsize=(9,4.5))
    bars=ax.bar(mnames, [metric[n]['f1_macro'] for n in mnames]);plot_bar_labels(ax,bars)
    ax.set_ylim(0,1.12);ax.set_ylabel('F1 macro na validação')
    ax.set_title('Comparação dos algoritmos (validação independente)')
    fig.tight_layout();fig.savefig(fig_dir/'02_comparacao_validacao.png',dpi=160);plt.close(fig)

    cm=confusion_matrix(ytest,pred,labels=COLS)
    fig,ax=plt.subplots(figsize=(5.8,5.3))
    ConfusionMatrixDisplay(cm,display_labels=['Gato','Cão']).plot(ax=ax,cmap='Blues',colorbar=False,values_format='d')
    ax.set_title('Matriz de confusão - conjunto de teste')
    ax.set_xlabel('Espécie prevista');ax.set_ylabel('Espécie real')
    fig.tight_layout();fig.savefig(fig_dir/'03_matriz_confusao.png',dpi=160);plt.close(fig)

    results=report['teste']['modelo_selecionado']['classes']
    x=np.arange(len(COLS));w=0.25
    fig,ax=plt.subplots(figsize=(8,4.6))
    for j,(label,k) in enumerate([('Precisão','precision'),('Recall','recall'),('F1','f1')]):
        ax.bar(x+(j-1)*w,[results[c][k] for c in COLS],w,label=label)
    ax.set_xticks(x,['Gato','Cão']);ax.set_ylim(0,1.12)
    ax.set_ylabel('Pontuação (0 a 1)');ax.set_title('Métricas por espécie no teste')
    ax.legend();fig.tight_layout();fig.savefig(fig_dir/'04_metricas_por_classe.png',dpi=160);plt.close(fig)
    return cm


def run(input_path: Path, output_dir: Path):
    df = pd.read_csv(input_path, encoding='utf-8-sig')
    if not {'Type','Description','linha_origem'}.issubset(df.columns):
        raise ValueError('A base tratada da TED 02 deve possuir Type, Description e linha_origem.')
    if df['Type'].isna().any() or set(df['Type'].unique()) != set(COLS):
        raise ValueError('Type deve conter as duas classes Cat e Dog, sem valores ausentes.')
    if df['linha_origem'].isna().any() or df['linha_origem'].duplicated().any():
        raise ValueError('linha_origem deve possuir identificadores únicos e não ausentes.')
    orig_count=len(df)
    df=df.copy()
    df['texto']=clean_text(df['Description'])
    sem_texto=int(df['texto'].eq('').sum())
    df=df[df['texto'].ne('')].reset_index(drop=True)
    df['grupo']=df['texto'].map(normalized_group)
    y=df['Type'].to_numpy(); groups=df['grupo'].to_numpy()

    # Divisão estratificada por grupo: descrições idênticas não se repartem.
    outer=StratifiedGroupKFold(n_splits=5,shuffle=True,random_state=SEED)
    trainval_pos,test_pos=next(outer.split(df['texto'],y,groups))
    trainval=df.iloc[trainval_pos].copy().reset_index(drop=True)
    test=df.iloc[test_pos].copy().reset_index(drop=True)
    inner=StratifiedGroupKFold(n_splits=8,shuffle=True,random_state=SEED+1)
    train_pos,val_pos=next(inner.split(trainval['texto'], trainval['Type'],trainval['grupo']))
    train=trainval.iloc[train_pos].copy(); val=trainval.iloc[val_pos].copy()

    assert not set(train['grupo']) & set(val['grupo'])
    assert not set(train['grupo']) & set(test['grupo'])
    assert not set(val['grupo']) & set(test['grupo'])
    assert len(train)+len(val)+len(test)+sem_texto==orig_count

    candidates={'Maioria (baseline)': DummyClassifier(strategy='most_frequent'),
                'Naive Bayes + TF-IDF': naive_bayes(),
                'Regressão Logística + TF-IDF': logistic()}
    valid_results={}
    for name, est in candidates.items():
        if isinstance(est,DummyClassifier):
            est.fit(np.zeros((len(train),1)),train['Type'])
            pred=est.predict(np.zeros((len(val),1)))
        else:
            est.fit(train['texto'],train['Type'])
            pred=est.predict(val['texto'])
        valid_results[name]=metrics(val['Type'],pred)

    # O conjunto de teste não participa da escolha do modelo.
    selected=max((name for name in candidates if name!='Maioria (baseline)'),
                 key=lambda name: valid_results[name]['f1_macro'])
    final=naive_bayes() if selected.startswith('Naive') else logistic()
    final.fit(trainval['texto'],trainval['Type'])
    test_pred=final.predict(test['texto'])
    baseline=DummyClassifier(strategy='most_frequent').fit(np.zeros((len(trainval),1)),trainval['Type'])
    test_baseline=baseline.predict(np.zeros((len(test),1)))
    probs=final.predict_proba(test['texto']);labels=list(final.classes_)
    confidence=np.max(probs,axis=1)

    # Diagnóstico extra: sem reentreinar, oculta termos óbvios apenas no TESTE;
    # não deve ser comparado como novo teste independente (distribuição perturbada).
    mask_pattern=re.compile(r'\b(cat|cats|kitten|kittens|dog|dogs|puppy|puppies|feline|canine)\b',re.IGNORECASE)
    masked_test=test['texto'].map(lambda v:mask_pattern.sub(' ',v))
    mask_pred=final.predict(masked_test)

    def counts(a):
        return {'total':len(a),'Gato':int((a['Type']=='Cat').sum()),'Cão':int((a['Type']=='Dog').sum()),
                'descricoes_distintas':int(a['grupo'].nunique())}
    mixed_groups=int(df.groupby('grupo')['Type'].nunique().gt(1).sum())
    summary={
        'titulo':'TED 03 - Classificação da espécie a partir de descrições',
        'objetivo':'Conferência exploratória de cadastros; não determina compatibilidade nem disponibilidade.',
        'origem':str(input_path.relative_to(ROOT)) if input_path.is_relative_to(ROOT) else str(input_path),
        'seed':SEED,'registros_base_ted02':orig_count,'sem_descricao_excluidos':sem_texto,
        'registros_modelagem':len(df),'grupos_duplicados_com_classes_conflitantes':mixed_groups,
        'estrategia':'StratifiedGroupKFold 5 folds -> teste; StratifiedGroupKFold 8 folds -> validacao; grupos por descricao NFKC/espacos/casefold, SHA-256; escolha por F1 macro na validacao, retreino em treino+validacao.',
        'variavel_alvo':'Type (Cat, Dog)','variavel_entrada':['Description'],
        'atributos_excluidos':'Breed1, MaturitySize e demais colunas não usados; AdoptionSpeed não é alvo.',
        'distribuicao':{'treino':counts(train),'validacao':counts(val),'teste':counts(test), 'treino_final':counts(trainval)},
        'validacao':valid_results,
        'modelo_selecionado':selected,
        'teste':{'modelo_selecionado':metrics(test['Type'],test_pred),
                 'baseline_maioria':metrics(test['Type'],test_baseline),
                 'teste_com_termos_de_especie_ocultos':metrics(test['Type'],mask_pred)},
        'matriz_confusao':{'rotulos':COLS,'valores':confusion_matrix(test['Type'],test_pred,labels=COLS).tolist()},
        'alerta':'O teste com palavras ocultas altera artificialmente a distribuicao de entrada; e um diagnostico auxiliar, nao outra estimativa imparcial de generalizacao.',
        'bibliotecas':{'python':platform.python_version(), 'scikit-learn':sklearn.__version__,
                       'pandas':pd.__version__,'numpy':np.__version__,
                       'matplotlib':matplotlib.__version__},
    }
    output_dir.mkdir(parents=True,exist_ok=True)
    save_figures(summary,test['Type'],test_pred,output_dir)
    preds=pd.DataFrame({'linha_origem':test['linha_origem'].to_numpy(),
                       'classe_real':test['Type'].to_numpy(),
                       'classe_prevista':test_pred,
                       'confianca_modelo':np.round(confidence,4),
                       'correta':(test['Type'].to_numpy()==test_pred)})
    preds.to_csv(output_dir/'predicoes_teste.csv',index=False,encoding='utf-8-sig')
    details=[]
    for part,name in [(train,'treino'),(val,'validacao'),(test,'teste')]:
        details.append(part[['linha_origem','Type','grupo']].assign(conjunto=name))
    pd.concat(details).sort_values('linha_origem').to_csv(output_dir/'particoes.csv',index=False,encoding='utf-8-sig')
    (output_dir/'resultados.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    (output_dir/'classificacao_teste.txt').write_text(classification_report(test['Type'],test_pred,labels=COLS,zero_division=0),encoding='utf-8')
    print(json.dumps({'modelo_selecionado':selected,'validacao_f1_macro':valid_results[selected]['f1_macro'],
                      'teste_f1_macro':summary['teste']['modelo_selecionado']['f1_macro'],
                      'teste_acuracia':summary['teste']['modelo_selecionado']['accuracy'],
                      'baseline_f1_macro':summary['teste']['baseline_maioria']['f1_macro'],
                      'tamanhos':summary['distribuicao']},ensure_ascii=False,indent=2))
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=ROOT/'data/processed/petfinder_mini_tratado.csv')
    parser.add_argument('--out',type=Path,default=ROOT/'reports/TED03')
    args=parser.parse_args()
    run(args.input,args.out)
