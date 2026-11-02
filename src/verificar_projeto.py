"""Confere integridade dos dados, partições e métricas dos relatórios salvos."""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    report = json.loads((ROOT/'reports/TED03/resultados.json').read_text(encoding='utf-8'))
    manifest = json.loads((ROOT/'data/manifesto_ted02.json').read_text(encoding='utf-8'))
    raw = ROOT/'data/raw/petfinder-mini.csv'
    assert hashlib.sha256(raw.read_bytes()).hexdigest() == manifest['sha256'], 'Hash da base divergente'
    base = read_csv(ROOT/'data/processed/petfinder_mini_tratado.csv')
    parts = read_csv(ROOT/'reports/TED03/particoes.csv')
    predictions = read_csv(ROOT/'reports/TED03/predicoes_teste.csv')
    expected = {x['linha_origem']: x for x in base if x['Description'].strip()}
    assert len(parts) == len(expected) == report['registros_modelagem']
    assert len({x['linha_origem'] for x in parts}) == len(parts)
    assert {x['linha_origem'] for x in parts} == set(expected)
    groups = defaultdict(set)
    for row in parts:
        groups[row['grupo']].add(row['conjunto'])
        assert row['Type'] == expected[row['linha_origem']]['Type']
    assert all(len(v) == 1 for v in groups.values()), 'Vazamento entre partições'
    counts = Counter(x['conjunto'] for x in parts)
    for name, n in counts.items():
        assert n == report['distribuicao'][name]['total']
    test_ids = {x['linha_origem'] for x in parts if x['conjunto'] == 'teste'}
    assert len(predictions) == len(test_ids)
    assert {x['linha_origem'] for x in predictions} == test_ids
    cm = [[0, 0], [0, 0]]
    labels = report['matriz_confusao']['rotulos']
    for row in predictions:
        assert row['classe_real'] == expected[row['linha_origem']]['Type']
        cm[labels.index(row['classe_real'])][labels.index(row['classe_prevista'])] += 1
    assert cm == report['matriz_confusao']['valores']
    accuracy = sum(cm[i][i] for i in range(2))/len(predictions)
    assert abs(accuracy-report['teste']['modelo_selecionado']['accuracy']) < 1e-12
    print(f'OK: base íntegra; {len(parts)} registros sem vazamento; acurácia {accuracy:.4%}.')


if __name__ == '__main__':
    main()
