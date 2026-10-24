"""Offline per-account public engagement analysis; Python standard library only."""
import argparse
import csv
import json
import math
import statistics
from pathlib import Path


def analyze(rows):
    unique = {}
    for row in rows:
        for key in ('author_id', 'id'):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError(f'{key} must be a nonempty string')
        for key in ('selected', 'pinned'):
            if key in row and not isinstance(row[key], bool):
                raise ValueError(f'{key} must be boolean')
        value = row.get('likes')
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))
                                  or not math.isfinite(value) or value < 0):
            raise ValueError('likes must be a nonnegative finite number or null')
        unique[(row['author_id'], row['id'])] = dict(row)
    groups = {}
    for row in unique.values():
        groups.setdefault(row['author_id'], []).append(row)
    summaries, works = [], []
    for author_id, items in groups.items():
        baseline = [r['likes'] for r in items if r.get('likes') is not None
                    and not r.get('selected', False) and not r.get('pinned', False)]
        median = statistics.median(baseline) if baseline else None
        summaries.append(dict(author_id=author_id, author=items[-1].get('author', ''),
                              collected=len(items), likes_missing=sum(r.get('likes') is None for r in items),
                              baseline_n=len(baseline), baseline_median_likes=median,
                              baseline_usable=len(baseline) >= 5 and median is not None and median > 0))
        for row in items:
            works.append(dict(author_id=author_id, id=row['id'], title=row.get('title', ''),
                              url=row.get('url', ''), likes=row.get('likes'),
                              pinned=row.get('pinned', False), selected=row.get('selected', False),
                              baseline_n=len(baseline), baseline_median_likes=median,
                              relative_likes=round(row['likes'] / median, 3)
                              if len(baseline) >= 5 and median and row.get('likes') is not None else None))
    return dict(input_rows=len(rows), unique_works=len(unique), duplicate_rows=len(rows)-len(unique),
                accounts=summaries, works=works)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    rows = json.loads(Path(args.input).read_text(encoding='utf-8-sig'))
    if not isinstance(rows, list):
        parser.error('input must be a JSON array')
    result = analyze(rows)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out/'分析汇总.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    for name, items, fields in [('账号汇总.csv', result['accounts'],
                                ['author_id','author','collected','likes_missing','baseline_n','baseline_median_likes','baseline_usable']),
                               ('作品相对表现.csv', result['works'],
                                ['author_id','id','title','url','likes','pinned','selected','baseline_n','baseline_median_likes','relative_likes'])]:
        with (out/name).open('w', encoding='utf-8-sig', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(items)
    print(json.dumps({k: result[k] for k in ('input_rows','unique_works','duplicate_rows')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
