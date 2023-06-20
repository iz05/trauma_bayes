import csv
import random

# returns data read from csv
def read_csv(filename, header_yn = False):
    header = None
    data = []
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if header_yn:
                header = row
                header_yn = False
            else:
                data.append(row)
    return header, data

# split into training and testing (one time run)
def split_data(data):
    random.shuffle(data)
    n = int(2 * len(data) / 3)
    training = data[ : n]
    testing = data[n : ]

    file = open('train.csv', 'w', newline = '')
    writer = csv.writer(file)
    for row in training:
        writer.writerow(row)
    file.close()

    file = open('test.csv', 'w', newline = '')
    writer = csv.writer(file)
    for row in testing:
        writer.writerow(row)
    file.close()

# get the class labels of data
def get_class_labels(data):
    return list(set(instance[-1] for instance in data))

# split into training and testing (one time run)
def split_data_stratify(data):
    labels = get_class_labels(data)
    data_by_labels = []
    for label in labels:
        data_by_labels.append([instance for instance in data if instance[-1] == label])

    file_train = open('train.csv', 'w', newline = '')
    writer_train = csv.writer(file_train)
    file_test = open('test.csv', 'w', newline = '')
    writer_test = csv.writer(file_test)

    for d in data_by_labels:
        random.shuffle(d)
        n = int(2 * len(d) / 3)
        train_temp = d[:n]
        test_temp = d[n:]
        for row in train_temp:
            writer_train.writerow(row)
        for row in test_temp:
            writer_test.writerow(row)
    file_train.close()
    file_test.close()
        
