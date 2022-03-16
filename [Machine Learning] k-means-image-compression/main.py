import matplotlib.pyplot as plt;
from sklearn.cluster import KMeans;
import numpy;

# Read Image
img = plt.imread("/home/notta/Desktop/Coding/Personal-Projects/k-means-image-compression/image.jpg");
width = img.shape[0];
height = img.shape[1];

# Flatten Image
img = img.reshape(width*height, 3);

# K-Means Algorithm
kmeans = KMeans(n_clusters=50).fit(img);
labels = kmeans.predict(img);
clusters = kmeans.cluster_centers_;

img2 = numpy.zeros((width, height, 3), dtype=numpy.uint8);

# Create a new image with a smaller size
index = 0;
for i in range(width):
  for j in range(height):
    label_of_pixel = labels[index];
    img2[i][j] = clusters[label_of_pixel];
    index += 1;

plt.imshow(img2);
plt.show()