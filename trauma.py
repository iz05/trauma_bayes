import numpy as np
import scipy.stats as stats

# returns model
def build_model(data, class_labels):
    class_count = [sum(1 if instance[-1] == c else 0 for instance in data) for c in class_labels]
    class_probs = [num / len(data) for num in class_count]
    cond_probs = {} # dictionary of form (attribute number, attribute value, class) : P(attribute value | class)
    corr_coeffs = {} # dictionary of form (attribute 1 number, attribute 2 number, class) : p_{12}

    for i in range(0, len(data[0]) - 1):
        attribute_values = sorted(list(set(instance[i] for instance in data)))
        for value in attribute_values:
            for j in range(0, len(class_labels)):
                c = class_labels[j]
                count = sum(1 if instance[-1] == c and instance[i] == value else 0 for instance in data)
                cond_probs[(i, value, c)] = count / class_count[j]

    for c in class_labels:
        subdata = [instance for instance in data if instance[-1] == c]
        for i in range(0, len(subdata[0]) - 1):
            for j in range(i + 1, len(subdata[0]) - 1):
                corr_coeffs[(i, j, c)] = corr_coeff([instance[i] for instance in subdata], [instance[j] for instance in subdata])
    return class_probs, cond_probs, corr_coeffs

def corr_coeff(list1, list2): # cramerV, calculate chi-square first, then normalize
    val1 = set(list1)
    val2 = set(list2)
    
    table = {}
    for v1 in val1:
        for v2 in val2:
            table[(v1, v2)] = 0
    for i in range(0, len(list1)):
        table[(list1[i], list2[i])] += 1
    
    array = []
    for v1 in val1:
        row = []
        for v2 in val2:
            row.append(table[(v1, v2)])
        array.append(row)

    array = np.array(array)
    X2 = stats.chi2_contingency(array, correction = False)[0]
    N = np.sum(array)
    minimum_dimension = min(array.shape) - 1
    
    if minimum_dimension <= 0:
        return 1
    
    # Calculate Cramer's V
    result = np.sqrt((X2 / N) / minimum_dimension)

    return result

# returns list of (instance, result) tuples
def test(model, data, class_labels):
    results = []
    for instance in data:
        results.append((instance, classify(model, instance, class_labels)))
    return results

def classify(model, instance, class_labels):
    class_probs, cond_probs, corr_coeffs = model
    probabilities = []
    for i in range(0, len(class_labels)):
        c = class_labels[i]
        p = class_probs[i] ** (len(instance) - 2)
        for j in range(0, len(instance) - 1):
            for k in range(j + 1, len(instance) - 1):
                j_prob = cond_probs[(j, instance[j], c)]
                k_prob = cond_probs[(k, instance[k], c)]
                p *= j_prob * k_prob + corr_coeffs[(j, k, c)] * (j_prob * k_prob * (1 - j_prob) * (1 - k_prob)) ** 0.5
        probabilities.append((p, c))
    probabilities.sort(key = lambda x : x[0], reverse = True)
    return probabilities[0][1]