import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine

df = pd.read_csv('out-2.csv', usecols=['id', 'image_link', 'image_title', 'source_link'])
print(df)

engine = create_engine('mysql://root:@localhost/Clothes')
with engine.connect() as conn, conn.begin():
    df.to_sql('Clothes', conn, if_exists='replace')