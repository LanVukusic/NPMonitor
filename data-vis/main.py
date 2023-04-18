# visualize different npm repositories from vectorized data of redame files.
# compress with t-SNE from 300 dimensions to 2 dimensions

import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# load the data
data = np.load("embedded_readmes.npy")
names = np.load("names.npy")

# # put the data thorugh kmeans
# kmeans = KMeans(n_clusters=10, random_state=0).fit(data)
# labels = kmeans.labels_

# # compress the data with t-SNE
# tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
# tsne_results = tsne.fit_transform(data)

# # plot the data
# plt.scatter(tsne_results[:,0], tsne_results[:,1], c=labels)
# for i, txt in enumerate(names):
#     plt.annotate(txt, (tsne_results[i,0], tsne_results[i,1]))

# #  show it
# plt.show()

while True:
  # get the input
  ins = input("Enter a repo name: ")

  # find the index of the repo
  index = np.where(names == ins)

  # get the vector
  vector = data[index][0]
  print(vector.shape)

  # get the distance to all other vectors with shape (876,384) (0,384) 
  differences = data - vector
  distances = np.linalg.norm(differences, axis=1)


  # get the 10 closest vectors
  closest = np.argsort(distances)[:3]

  # print the closest vectors
  print(names[closest])




# # plot the data
# plt.scatter(tsne_results[:,0], tsne_results[:,1])
# for i, txt in enumerate(names):
#     plt.annotate(txt, (tsne_results[i,0], tsne_results[i,1]))

# # save high resolution image and show it
# plt.savefig("tsne.png", dpi=500)
# plt.show()

# # save the data
# np.save("tsne_results.npy", tsne_results)
