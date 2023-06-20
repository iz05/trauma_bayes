import file_processing, result_analysis, naive, trauma, hidden
import time

# header, data = file_processing.read_csv("datasets/credit-g-discrete.csv", True)
# file_processing.split_data_stratify(data)

header, data_train = file_processing.read_csv("train.csv", False)
header, data_test = file_processing.read_csv("test.csv", False)
class_labels = file_processing.get_class_labels(data_train)

start = time.time()
model = naive.build_model(data_train, class_labels)
results = naive.test(model, data_test, class_labels)
end = time.time()
print("---------- RESULTS FOR NAIVE BAYES ----------\n")
print("ACCURACY: %s%%\n" % (result_analysis.accuracy(data_test, results) * 100))
print("CONFUSION MATRIX: \n%s" % result_analysis.matrix(data_test, results, class_labels))
print("IT TOOK %s SECONDS TO BUILD THIS MODEL." % (end - start))
print("\n")

start = time.time()
model = trauma.build_model(data_train, class_labels)
results = trauma.test(model, data_test, class_labels)
end = time.time()
print("---------- RESULTS FOR TRAUMATIZED BAYES ----------\n")
print("ACCURACY: %s%%\n" % (result_analysis.accuracy(data_test, results) * 100))
print("CONFUSION MATRIX: \n%s" % result_analysis.matrix(data_test, results, class_labels))
print("IT TOOK %s SECONDS TO BUILD THIS MODEL." % (end - start))
print("\n")

start = time.time()
model = hidden.build_model(data_train, class_labels)
results = hidden.test(model, data_test, class_labels)
end = time.time()
print("---------- RESULTS FOR HIDDEN NAIVE BAYES ----------\n")
print("ACCURACY: %s%%\n" % (result_analysis.accuracy(data_test, results) * 100))
print("CONFUSION MATRIX: \n%s" % result_analysis.matrix(data_test, results, class_labels))
print("IT TOOK %s SECONDS TO BUILD THIS MODEL." % (end - start))
print("\n")
