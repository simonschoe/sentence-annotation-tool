from pathlib import Path
from datetime import datetime
import pandas as pd


FNAME = 'xxxxx'
FILE_PATH = Path(f'output/{FNAME}.jsonl')

data = pd.read_json(FILE_PATH, lines=True)
data = pd.concat([pd.json_normalize(data['meta']), data.drop(['meta'], axis=1)], axis=1)
data['accept'] = data['accept'].apply(lambda x: ','.join(map(str, x)))
data['_timestamp'] = data['_timestamp'].apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
data.to_excel(f'output/{FNAME}.xlsx')