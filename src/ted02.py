"""TED 02 PetFinder mini: preparação conservadora e EDA reproduzível."""
from pathlib import Path
import json, hashlib, io, urllib.request, zipfile
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
URL='https://storage.googleapis.com/download.tensorflow.org/data/petfinder-mini.zip'
def main():
    rawfile=ROOT/'data/raw/petfinder-mini.csv'
    reports=ROOT/'reports/TED02'; figs=reports/'figures'; processed=ROOT/'data/processed'
    for p in [rawfile.parent,reports,figs,processed]: p.mkdir(parents=True,exist_ok=True)
    if not rawfile.exists():
        with urllib.request.urlopen(URL,timeout=90) as r: payload=r.read()
        with zipfile.ZipFile(io.BytesIO(payload)) as z: rawfile.write_bytes(z.read('petfinder-mini/petfinder-mini.csv'))
    raw=pd.read_csv(rawfile,keep_default_na=False)
    df=raw.copy()
    df['linha_origem']=range(2,len(df)+2)
    df['duplicata_excedente']=raw.duplicated()
    changed={}
    for c in raw.select_dtypes('object'):
        old=df[c].copy();df[c]=df[c].str.strip();changed[c]=int((old!=df[c]).sum())
    df['descricao_ausente']=df.Description.eq('')
    df.loc[df.descricao_ausente,'Description']=pd.NA
    invalid={}
    for c in ['Age','Fee','PhotoAmt','AdoptionSpeed']:
        numeric=pd.to_numeric(df[c],errors='coerce')
        bad=numeric.isna() | (numeric<0)
        if c!='Fee': bad=bad | (numeric%1!=0)
        if c=='AdoptionSpeed':bad=bad | ~numeric.isin(range(5))
        invalid[c]=int(bad.sum());df[c]=numeric.mask(bad)
    cats={'Type':['Cat','Dog'],'Gender':['Male','Female'],'MaturitySize':['Small','Medium','Large'], 'FurLength':['Short','Medium','Long'],'Vaccinated':['Yes','No','Not Sure'],'Sterilized':['Yes','No','Not Sure'],'Health':['Healthy','Minor Injury','Serious Injury']}
    for c,allowed in cats.items():
        invalid[c]=int((~df[c].isin(allowed)).sum())
    if any(invalid[c] for c in cats):
        raise ValueError('Categorias inesperadas na base: '+str({c:invalid[c] for c in cats if invalid[c]}))
    out=[]
    for c in ['Age','Fee','PhotoAmt']:
        q1,q3=df[c].quantile([.25,.75]);low=q1-1.5*(q3-q1);high=q3+1.5*(q3-q1)
        flag=(df[c]<low)|(df[c]>high)
        out.append({'variavel':c,'q1':q1,'q3':q3,'limite_inferior':low,'limite_superior':high,'sinalizados':int(flag.sum())})
        df['atipico_'+c]=flag
    frequencies=[]
    for c in cats:
        for k,n in df[c].value_counts(dropna=False).items(): frequencies.append({'variavel':c,'categoria':k,'quantidade':int(n),'percentual':round(n/len(df)*100,2)})
    pd.DataFrame(frequencies).to_csv(reports/'frequencias.csv',index=False,encoding='utf-8-sig')
    df[['Age','Fee','PhotoAmt']].describe().T.to_csv(reports/'estatisticas_numericas.csv',encoding='utf-8-sig')
    pd.DataFrame(out).to_csv(reports/'possiveis_outliers.csv',index=False,encoding='utf-8-sig')
    # Comparação de sensibilidade sem excluir os registros da base principal.
    reduced=df.loc[~df.duplicata_excedente]
    sensitivity=[]
    for c in ['Type','MaturitySize','Vaccinated']:
        a=df[c].value_counts(normalize=True)*100;b=reduced[c].value_counts(normalize=True)*100
        for k in a.index:sensitivity.append({'variavel':c,'categoria':k,'com_repeticoes_pct':a[k],'sem_excedentes_pct':b.get(k,0),'diferenca_pp':b.get(k,0)-a[k]})
    pd.DataFrame(sensitivity).to_csv(reports/'sensibilidade_duplicatas.csv',index=False,encoding='utf-8-sig')
    cross=pd.crosstab(df.Type,df.MaturitySize,normalize='index')*100
    cross.to_csv(reports/'especie_porte_percentual.csv',encoding='utf-8-sig')
    df.groupby('Type').Age.describe().to_csv(reports/'idade_por_especie.csv',encoding='utf-8-sig')
    def save(name):
        plt.tight_layout();plt.savefig(figs/name,dpi=160);plt.close()
    plt.rcParams.update({'font.size':10})
    df.Type.value_counts().rename(index={'Dog':'Cães','Cat':'Gatos'}).plot.bar(color='#336b87',rot=0,figsize=(7,3.4));plt.ylabel('Registros');plt.title('Espécies na base');save('01_especies.png')
    df.MaturitySize.value_counts().reindex(['Small','Medium','Large']).rename(index={'Small':'Pequeno','Medium':'Médio','Large':'Grande'}).plot.bar(color='#336b87',rot=0,figsize=(7,3.4));plt.ylabel('Registros');plt.title('Porte registrado');save('02_porte.png')
    df.Age.plot.hist(bins=list(range(0,261,10)),figsize=(7,3.4),color='#336b87');plt.xlabel('Idade em meses');plt.ylabel('Registros');plt.title('Distribuição de idade — intervalos de 10 meses');save('03_idade.png')
    care=pd.DataFrame({c:df[c].value_counts(normalize=True)*100 for c in ['Vaccinated','Sterilized']}).T.reindex(columns=['Yes','No','Not Sure'])
    care.index=['Vacinação','Castração'];care.columns=['Sim','Não','Não confirmado'];care.plot.barh(stacked=True,figsize=(7,3.4),color=['#498467','#b36b54','#a6a6a6']);plt.xlabel('Percentual');plt.legend(loc='lower center',bbox_to_anchor=(.5,-.55),ncol=3);save('04_cuidados.png')
    cross.reindex(columns=['Small','Medium','Large']).rename(index={'Dog':'Cães','Cat':'Gatos'},columns={'Small':'Pequeno','Medium':'Médio','Large':'Grande'}).plot.bar(stacked=True,rot=0,figsize=(7,3.4));plt.ylabel('Percentual dentro da espécie');plt.xlabel('');plt.legend(loc='upper right');save('05_especie_porte.png')
    df.boxplot(column='Age',by='Type',figsize=(7,3.4));plt.suptitle('');plt.title('Idade por espécie e valores extremos');plt.ylabel('Meses');plt.xlabel('Espécie');save('06_idade_especie.png')
    target=processed/'petfinder_mini_tratado.csv'
    with target.open('w',encoding='utf-8-sig',newline='') as f:df.to_csv(f,index=False)
    check=pd.read_csv(target)
    assert check.shape==df.shape and check.linha_origem.tolist()==df.linha_origem.tolist()
    summary={'linhas_brutas':len(raw),'colunas_brutas':raw.shape[1],'linhas_tratadas':len(df),'colunas_tratadas':df.shape[1],'duplicatas_excedentes':int(raw.duplicated().sum()),'descricoes_ausentes':int(df.descricao_ausente.sum()),'idade_zero':int(df.Age.eq(0).sum()),'sem_fotos':int(df.PhotoAmt.eq(0).sum()),'invalidos':invalid,'espacos_corrigidos':changed,'outliers':out,'maior_variacao_duplicatas_pp':max(abs(x['diferenca_pp']) for x in sensitivity),'sha256':hashlib.sha256(rawfile.read_bytes()).hexdigest()}
    (reports/'resumo.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'data/manifesto_ted02.json').write_text(json.dumps({'fonte':URL,'arquivo':'raw/petfinder-mini.csv','sha256':summary['sha256'],'observacao':'Mesma base da TED 01. IDs de linha são técnicos e não identificam animais.'},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2));return raw,df,summary
if __name__=='__main__':main()
