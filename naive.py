# returns model
def build_model(data, class_labels):
    class_count = [sum(1 if instance[-1] == c else 0 for instance in data) for c in class_labels]
    class_probs = [num / len(data) for num in class_count]
    cond_probs = {} # dictionary of form (attribute number, attribute value, class) : P(attribute value | class)
    
    for i in range(0, len(data[0]) - 1):
        attribute_values = sorted(list(set(instance[i] for instance in data)))
        for value in attribute_values:
            for j in range(0, len(class_labels)):
                c = class_labels[j]
                count = sum(1 if instance[-1] == c and instance[i] == value else 0 for instance in data)
                cond_probs[(i, value, c)] = count / class_count[j]
    return class_probs, cond_probs

# returns list of (instance, result) tuples
def test(model, data, class_labels):
    results = []
    for instance in data:
        results.append((instance, classify(model, instance, class_labels)))
    return results

def classify(model, instance, class_labels):
    class_probs, cond_probs = model
    probabilities = []
    for i in range(0, len(class_labels)):
        c = class_labels[i]
        p = class_probs[i]
        for k in range(0, len(instance) - 1):
            p *= cond_probs[(k, instance[k], c)]
        probabilities.append((p, c))
    probabilities.sort(key = lambda x : x[0], reverse = True)
    return probabilities[0][1]

        