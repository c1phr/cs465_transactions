import numpy as np
import matplotlib.pyplot as plt
import time

class barchart(object):

    def __init__(self, values):
        self.value = values
        self.change_val = 0

    def change_value(self, new_value):
        self.value = new_value
        self.change_val = 1

    def make_barchart(self):
        tru = True
        self.change_val = 0
        counter = 0
        if tru == True:
            while tru == True:
                if self.change_val == 1:
                    break
                else:
                    cubby_val = self.value
                    N = len(cubby_val)
                    label_list = []
                    for i in range(0, N):
                        label_list.append("C" + str(i+1))
                    index = np.arange(N)

                    p1 = plt.bar(index, cubby_val, .8, color='b', edgecolor="r", align="center")

                    plt.ylabel('Value')
                    plt.title('Value of Cubbies')
                    plt.xticks(index, label_list)
                    plt.yticks(np.arange(0,51,10))

                    def label_system(p1):
                        for rect in p1:
                            height = rect.get_height()
                            plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                                    ha='center', va='bottom')

                    label_system(p1)
                    if counter == 0:
                        plt.show()
                    counter = counter + 1
                
                tru = False



