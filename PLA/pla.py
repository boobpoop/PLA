import numpy as np
import matplotlib.pyplot as plt

def load_data():
    records = [[1,1,-1], [1,2,-1], [1,3,-1], [2,1,-1], [2,2,-1], [2,3, +1], [3,1,-1], [3,2,+1], [3,3,+1]]  
    data = []
    label = []
    for record in records:
        #add one dimension-----x0
        data.append([1, float(record[0]), float(record[1])])
        label.append(int(record[2]))
    return data, label

def sign(weight, x):
    if weight.dot(x) < 0:
        return -1
    elif weight.T.dot(x) == 0:
        return 0
    else:
        return +1

def PLA(data, label):
    data = np.array(data); label = np.array(label)
    # m = 2 + 1
    m, n = data.shape
    #weight before revising
    weight_old = np.zeros((n))
    #weight after revising
    weight_new = np.zeros((n))
    all_changed = True
    j = 0
    while all_changed:
        all_changed = False
        for i in range(m):
            predict = sign(weight_old, data[i])
            if predict != label[i]:
                all_changed = True
                weight_new = weight_old + label[i] * data[i]
                visualize(data.tolist(), label.tolist(), weight_old.tolist(), weight_new.tolist(), j, i)
                weight_old = weight_new
        j += 1

def arrow_annotate(ax, text1, tx1, ty1, line_color):
    ax.text(tx1/2, ty1/2, text1, fontsize=6, verticalalignment="center", horizontalalignment="center")
    ax.annotate("",xy=(tx1, ty1),xytext=(0,0),arrowprops=dict(color=line_color,arrowstyle="->",connectionstyle="arc3"))

def visualize(data, label, weight_old, weight_new, j, k):
    xcord_1 = []
    ycord_1 = []
    xcord1 = [] 
    ycord1 = []
    for i in range(len(label)):
        if label[i] == -1:
            xcord_1.append(data[i][1])
            ycord_1.append(data[i][2])
        else:
            xcord1.append(data[i][1])
            ycord1.append(data[i][2])
    plt.switch_backend("agg")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #draw a straight line
    x0 = np.arange(-4, 6, 0.1)
    if weight_new[2] == 0:
        if weight_new[1] == 0:
            plt.hlines(0, -4, 6, color = "black")
            plt.fill_between(x0, 0, 6 , facecolor = "chartreuse")
            plt.fill_between(x0, -4, 0, facecolor = "lightcoral")
        else:
            x1 = np.arange(-4, -weight_new[0] / float(weight_new[1]), 0.01)
            x2 = np.arange(-weight_new[0] / float(weight_new[1]), 6,  0.01)
            plt.vlines(-weight_new[0] / weight_new[1], -4, 6, color = "black")
            plt.fill_between(x1, -4, 6, facecolor = "chartreuse")
            plt.fill_between(x2, -4, 6, facecolor = "lightcoral")
    else:
        y0 = (-weight_new[0] - weight_new[1] * x0) / weight_new[2]
        if weight_new[2] > 0:
            plt.fill_between(x0, y0, 6, facecolor = "lightcoral")
            plt.fill_between(x0, y0, -4, facecolor = "chartreuse")
        else:
           plt.fill_between(x0, y0, 6, facecolor = "chartreuse")
           plt.fill_between(x0, y0, -4, facecolor = "lightcoral") 
        plt.ylim(-4, 6)
        ax.plot(x0, y0, color = "black")
    
    #w_old
    plt.plot([0, weight_old[1]], [0, weight_old[2]], color = "blue")
    arrow_annotate(ax, "w_old", weight_old[1], weight_old[2], "blue")
    #w_new
    plt.plot([0, weight_new[1]], [0, weight_new[2]], color = "red")
    arrow_annotate(ax, "w_new", weight_new[1], weight_new[2], "red")
    #y * x
    plt.plot([0, label[k] * data[k][1]], [0, label[k] * data[k][2]], color = "yellow") 
    arrow_annotate(ax, "y*x", label[k] * data[k][1], label[k] * data[k][2], "yellow")
     
    ax.scatter(xcord_1, ycord_1, s = 30, c = "red", marker = "o", alpha = 1)
    ax.scatter(xcord1, ycord1, s = 30, c = "blue", marker = "+", alpha = 1)

    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    plt.title("%dth round, %dth point" %(j+1,k+1))
    plt.legend()


    # dpi = 300 means 1800 * 1200 size of a graph
    plt.rcParams['savefig.dpi'] = 300 
    #add 0 inside file name to make it left-justified
    if j<10:
        plt.savefig("./pla_graph/visualize0%d%d.jpg" %(j, k))
    else:
        plt.savefig("./pla_graph/visualize%d%d.jpg" %(j, k))

    plt.close()
   
if __name__ == "__main__":
    data, label = load_data()
    PLA(data, label)
