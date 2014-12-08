import numpy as np
import matplotlib.pyplot as plt

#will covert to class after test

N = 5
cubby_val   = (4, 4, 4, 4, 4)
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, cubby_val,   width, color='g')

plt.ylabel('Value')
plt.title('Value of Cubbies')
plt.xticks(ind+width/2., ('C1', 'C2', 'C3', 'C4', 'C5') )
plt.yticks(np.arange(0,21,1))

plt.show()



