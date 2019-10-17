from PIL import Image
import numpy as np
import random

class Cartoonizer:
    def __init__(self,path,n=6):
        # im_path = "E:/Documents/Python/image cartoonizer/Beautiful-Awesome-Wallpaper.jpg"
        self.number_of_clusters = n
        im = Image.open(path)    
        self.im = np.asarray(im)
        self.rows,self.cols = self.im.shape[0],self.im.shape[1]
        self.cluster_assignments = None
        self.init_means()
    def init_means(self):
        self.means = np.random.random((self.number_of_clusters,3))*256
    def dist(self,a): 
        return (a[0]**2+a[1]**2+a[2]**2)**.5
    def get_cluster_assignments(self):
        print("Calculating cluster assignments.")
        self.cluster_distances = np.zeros((self.number_of_clusters,self.rows,self.cols))
        for i in range(self.number_of_clusters):
            diff = self.means[i,...]-self.im
            square = diff**2
            sum = np.sum(square,axis=2)
            distance = sum**.5
            self.cluster_distances[i]=np.array(distance)
        self.cluster_assignments = np.argmin(self.cluster_distances,axis=0)
        print("Cluster assignments calculated.")
    def move_averages(self):
        print("Calculating cluster averages.")
        for i in range(self.number_of_clusters):
            values_within_cluster = self.im[self.cluster_assignments==i].reshape(-1,3)
            if values_within_cluster.any():
                self.means[i]=values_within_cluster.mean(0)
        # print("a.means:\n" + str(a.means))
        print("Cluster averages calculated.")
    def build_resulting_image(self):
        self.final_im = np.zeros((self.rows,self.cols,3))
        for i in range(self.number_of_clusters):
            self.final_im[self.cluster_assignments==i]=self.means[i]
        self.picture_out = Image.fromarray(self.final_im.astype(np.uint8))
        self.picture_out.save("out.png")
    def run(self):
        converged = False
        iteration = 1
        while not converged:
            print("\niteration: " + str(iteration))
            old_cluster_assignments = np.array(self.cluster_assignments)
            self.get_cluster_assignments()
            self.move_averages()
            if (self.cluster_assignments == old_cluster_assignments).all():
                converged = True
            else:
                # prin("self.cluster_assignments.shape: " + str(self.cluster_assignments.shape))
                if old_cluster_assignments.shape == self.cluster_assignments.shape:
                    avg_diff = np.mean(abs(old_cluster_assignments - self.cluster_assignments))
                    print("Average movement: " + str(avg_diff))
            iteration += 1
        print("Converged!")
        self.build_resulting_image()

path = os.getcwd().replace("\\","/")+"/w4vioms17a631.jpg"
a=Cartoonizer(path,n=11)
a.means=np.array([[255,246,128],
                 [202,196,101],
                 [92,156,254],
                 [55,126,232],
                 [144,179,125],
                 [24,238,135],
                 [27,231,141],
                 [8,240,156],
                 [239,240,205],
                 [0,160,184],
                 [144,180,112]])
a.run()


    














