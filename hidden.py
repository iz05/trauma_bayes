import math

# returns model
def build_model(data, class_labels):
    class_count = [sum(1 if instance[-1] == c else 0 for instance in data) for c in class_labels]

    # compute class probabilities
    class_probs = [(num + 1) / (len(data) + len(class_labels)) for num in class_count]

    # values of each attribute
    attribute_vals = []
    for i in range(0, len(data[0]) - 1):
        attribute_vals.append(set(data[j][i] for j in range(0, len(data))))

    # conditional probabilities - same as naive bayes
    cond_probs = {} # dictionary of form (attribute number, attribute value, class) : P(attribute value | class)
    
    for i in range(0, len(data[0]) - 1):
        attribute_values = sorted(list(set(instance[i] for instance in data)))
        for value in attribute_values:
            for j in range(0, len(class_labels)):
                c = class_labels[j]
                count = sum(1 if instance[-1] == c and instance[i] == value else 0 for instance in data)
                cond_probs[(i, value, c)] = (count + 1) / (class_count[j] + len(attribute_values))

    # probabilities
    probs = {} # key: (i, j, ai, aj, c)
    for i in range(0, len(attribute_vals)):
        for j in range(i + 1, len(attribute_vals)):
            for ai in attribute_vals[i]:
                for aj in attribute_vals[j]:
                    for c in class_labels:
                        subdata = [data[k] for k in range(0, len(data)) if data[k][-1] == c]
                        probs[(i, j, ai, aj, c)] = (len([subdata[k] for k in range(0, len(subdata)) if subdata[k][i] == ai and subdata[k][j] == aj ]) + 1) / (len(subdata) + len(attribute_vals[i]) * len(attribute_vals[j]))
                        probs[(j, i, aj, ai, c)] = probs[(i, j, ai, aj, c)]
                        
    # computing Ip        
    ip = {} # key: (i, j)
    for i in range(0, len(attribute_vals)):
        for j in range(i + 1, len(attribute_vals)):
            val = 0
            for ai in attribute_vals[i]:
                for aj in attribute_vals[j]:
                    for c in class_labels:
                        p = len([data[k] for k in range(0, len(data)) if data[k][i] == ai and data[k][j] == aj and data[k][-1] == c]) / len(data)
                        val += p * math.log2(probs[(i, j, ai, aj, c)] / cond_probs[(i, ai, c)] / cond_probs[(j, aj, c)])
            ip[(i, j)] = val
            ip[(j, i)] = val
    
    weights = []
    for i in range(0, len(attribute_vals)):
        weights.append(sum(ip[(i, j)] for j in range(0, len(attribute_vals)) if i != j))

    w = {} # key: (i, j)
    for i in range(0, len(attribute_vals)):
        for j in range(0, len(attribute_vals)):
            if i != j:
                if weights[i] == 0:
                    w[(i, j)] = 0.5
                else:
                    w[(i, j)] = ip[(i, j)] / weights[i]
    
    # finish implementing the probabilities
    parent_probs = {} # key: (i, ai, j, aj, c)
    for i in range(0, len(attribute_vals)):
        for ai in attribute_vals[i]:
            for j in range(0, len(attribute_vals)):
                if j != i:
                    for aj in attribute_vals[j]:
                        for c in class_labels:
                            instances = [data[k] for k in range(0, len(data)) if data[k][j] == aj and data[k][-1] == c]
                            sub_instances = [instances[k] for k in range(0, len(instances)) if instances[k][i] == ai]
                            parent_probs[(i, ai, j, aj, c)] = (len(sub_instances) + 1) / (len(instances) + len(attribute_vals[i]))

    return w, parent_probs, class_probs

# returns list of (instance, result) tuples
def test(model, data, class_labels):
    results = []
    for instance in data:
        results.append((instance, classify(model, instance, class_labels)))
    return results

def classify(model, instance, class_labels):
    weights, parent_probs, class_probs = model
    final_probs = []
    for k in range(0, len(class_labels)):
        c = class_labels[k]
        probs = []
        for i in range(0, len(instance) - 1):
            probs.append(sum(weights[(i, j)] * parent_probs[(i, instance[i], j, instance[j], c)] for j in range(0, len(instance) - 1) if j != i))
        p = class_probs[k]
        for thing in probs:
            p *= thing
        final_probs.append((p, c))
    final_probs.sort(key = lambda x : x[0], reverse = True)
    return final_probs[0][1]