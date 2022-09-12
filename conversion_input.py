import json
import pandas as pd

fname = 'training_sample'

def create_input(raw_path):
    
    df = pd.read_excel(raw_path, index_col=0)
    
    dict_array = [{
        'text': str(df.iloc[i, 3]),
        'meta': {'call_id': str(df.iloc[i, 0]),
                 'remark_id': str(df.iloc[i, 1]),
                 'sent_id': str(df.iloc[i, 2])}} for i in range(len(df))]

    with open(f'input/{fname}.jsonl', 'w', encoding='utf-8') as f:
        for item in dict_array:
            f.write(json.dumps(item)+'\n')

create_input(f'input/{fname}.xlsx')
