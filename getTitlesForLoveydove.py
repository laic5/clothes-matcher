from csv import reader

with open('image_links.csv', 'w') as out:
    with open('out-2.csv', 'r') as inF:
        for row in reader(inF):
            print(row[1], file=out)
