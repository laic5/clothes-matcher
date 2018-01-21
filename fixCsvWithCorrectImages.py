import pandas as pd

df = pd.read_csv('out-3.csv', usecols=['id', 'image_link', 'image_title', 'source_link'])
df.index = range(1,len(df)+1)
newdf = pd.DataFrame()

#state_df = df.loc[df['CITY'].str.startswith('BH'), ['STATE']]

df['id'] += 1

print(df['id'])

newdf = df.loc[(df.loc['id'].str[0:1] =='2' and df.loc['id'].str[0:2] != '20'), ['image_link', 'image_title', 'source_link']]

# #df.ix[(df.index.hour == 3) | (df.index.hour == 15)]
#
# for row,index in df.iterrows():
#     stringIndex = str(index)
#     if (stringIndex[:1] == '2' and stringIndex[:2] != '20'):
#         print(stringIndex)
#         pass
#     else:
#         print(df[row:])
#         minidf = pd.DataFrame(row)
#         newdf.append(minidf)

print(newdf)

