import create_hashtag_mention_matrix
import json
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs


# access hashtag_clustering file, data from file to use in this script
normalized_matrix = create_hashtag_mention_matrix.normalized_matrix


centers = [[1, 1], [-1, -1], [1, -1]]
normalized_matrix, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.5, random_state=0)


af = AffinityPropagation(preference=-50).fit(normalized_matrix)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))

import matplotlib.pyplot as plt
from itertools import cycle

plt.close('all')
plt.figure(1, figsize=(18, 16))
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = normalized_matrix[cluster_centers_indices[k]]
    plt.plot(normalized_matrix[class_members, 0], normalized_matrix[class_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
    for x in normalized_matrix[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
plt.savefig('./data/jan_sample_affinity.png')