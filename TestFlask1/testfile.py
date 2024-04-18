# Give me python code to ready a csv file in a memory efficient way
def read_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            yield [float(_) if _.replace('.', '', 1).isdigit() else _
                   for _ in row]


if __name__ == '__main__':

    # Read the data from CSV and put it into an array of arrays (rows are lists inside another list)
    rows = []

    for r in read_from_csv('data/iris-with-header.csv'):

        print("Row:", len(rows))

        rows += [[_.strip('" ')
                  .lower().translate({ord('.'): None})
                   for _ in r]]

    headers = ['sepal length','sepal width',
               'petal length', 'petal width']


    df = pd.DataFrame(rows[1:], columns=headers)



