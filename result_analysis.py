def accuracy(data, results):
    return sum(1 if data[i][-1] == results[i][1] else 0 for i in range(0, len(data))) / len(data)

def matrix(data, results, class_labels):
    m = {} # (predicted, actual)
    for c1 in class_labels:
        for c2 in class_labels:
            m[(c1, c2)] = 0 
    for i in range(0, len(data)):
        m[(results[i][1], data[i][-1])] += 1

    m_string = "\t"
    for c in class_labels:
        m_string = m_string + c + "\t"
    m_string += "\n"
    for c1 in class_labels:
        m_string += "\t"
        for c2 in class_labels:
            m_string = m_string + str(m[(c1, c2)]) + "\t"
        m_string += "\n"
    return m_string