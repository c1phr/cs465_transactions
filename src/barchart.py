import numpy as np
import matplotlib.pyplot as plt

class barchart(object):

    def __init__(self, values):
        self.value = values

    def change_value(self, new_value):
        self.value = new_value

    def make_barchart(self):
        while True:
            cubby_val   = self.value
            N = len(cubby_val)
            label_list = []
            for i in range(0, N):
                label_list.append("C" + str(i+1))
            index = np.arange(N)    # the x locations for the groups
            width = .8       # the width of the bars: can also be len(x) sequence

            p1 = plt.bar(index, cubby_val, width, color='b', edgecolor="r", align="center")

            plt.ylabel('Value')
            plt.title('Value of Cubbies')
            plt.xticks(index, label_list)
            plt.yticks(np.arange(0,22,1))

            def autolabel(p1):
                # attach some text labels
                for rect in p1:
                    height = rect.get_height()
                    plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                            ha='center', va='bottom')

            autolabel(p1)

            plt.show()



