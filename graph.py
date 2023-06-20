import matplotlib.pyplot as plt

x_axis = ["IRIS", "CREDIT", "COVID"]
naive = [0.001, 0.015, 2.407]
trauma = [0.009, 0.369, 20.681]
hidden = [0.018, 1.683, 369.593]
gaussian = [0.031, 0.693, 142.876]

line1 = plt.plot(x_axis, naive, 'ko-', label = 'naive')
line2 = plt.plot(x_axis, trauma, 'ro-', label = 'trauma')
line3 = plt.plot(x_axis, hidden, 'mo-', label = 'hidden')
line4 = plt.plot(x_axis, gaussian, 'co-', label = 'gaussian')
plt.legend()

plt.xlabel("Dataset")
plt.ylabel("Runtime")

plt.show()