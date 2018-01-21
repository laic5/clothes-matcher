import pickle
import pandas as pd


PICKLED_FILE = 'google1937.p'

with open(PICKLED_FILE, 'rb') as pickle_file:
    content = pickle.load(pickle_file)

df = pd.DataFrame(content)
print(df)