import pandas as pd
f='data/raw/TA_202512.ods'
for sh in ['TA1','TA2','TA7','TA9','TA4']:
    df=pd.read_excel(f,sheet_name=sh,engine='odf',header=None)
    print('=====',sh,df.shape)
    for i in range(0,8):
        print(i,[str(x)[:45] for x in df.iloc[i].tolist()[:12]])
    ldn=df[df[0].astype(str).str.startswith('E09')]
    print('boroughs:',len(ldn))
    print(ldn.head(3).to_string(max_colwidth=25))
