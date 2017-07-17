import create_hashtag_mention_matrix
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import pylab as plt
import json
from sklearn.manifold import TSNE
from collections import Counter

# define input data file
input_data_file = './data/toy_data.json'

# access hashtag_clustering file, data from file to use in this script
normalized_matrix = create_hashtag_mention_matrix.create_initial_data_structure(input_data_file)

with open(input_data_file, 'rb') as raw_tweet_data:

    # generate python dict from raw json data
    all_users_terms_dict = json.load(raw_tweet_data)
#print(len(all_users_terms_dict))

complete_terms_list = []
complete_users_list = []

for key, value in all_users_terms_dict.items():
    complete_terms_list.extend(value)
    if key not in complete_users_list:
        complete_users_list.append(key)
#print(len(complete_users_list))

term_set = set(complete_terms_list)
#print(len(term_set))

unique_terms = []

for term in term_set:
    unique_terms.append(term)
    
print(len(unique_terms))

pca = PCA(n_components=20)
pca_result = pca.fit_transform(normalized_matrix.data)

print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
print(sum(pca.explained_variance_ratio_))

kmeans = KMeans(n_clusters=3)
kmeans.fit(pca_result)

tsne = TSNE(n_components=3, verbose=1, perplexity=40, n_iter=300)
tsne_results = tsne.fit_transform(pca_result).T 


print(tsne_results.shape)
print((kmeans.labels_).shape)

Counter(kmeans.labels_)

#figure size for jupyter notebook
pl.figure(figsize=(1, (18, 16)))

plt.scatter(tsne_results[0], tsne_results[1], c=kmeans.labels_, cmap=plt.cm.rainbow)
#plt.show()
plt.savefig('./data/kmeans_toy.png')

cluster_1 = normalized_matrix[np.where(kmeans.labels_ == 1)]
x_1 = np.sum(cluster_1, axis=0)

print(cluster_1.shape)
print(x_1.shape)

cluster_2 = normalized_matrix[np.where(kmeans.labels_ == 2)]
x_2 = np.sum(cluster_2, axis=0)

print(cluster_2.shape)
print(x_2.shape)

cluster_3 = normalized_matrix[np.where(kmeans.labels_ == 3)]

x_3 = np.sum(cluster_3, axis=0)

print(cluster_3.shape)
print(x_3.shape)


def top_hashtags_per_cluster(cluster, unique_terms):

    top_tags = cluster.argsort()[-20:][::-1]

    for i in top_tags:
        print(unique_terms[i])

print(top_hashtags_per_cluster(x_1, unique_terms))
print(top_hashtags_per_cluster(x_2, unique_terms))
print(top_hashtags_per_cluster(x_3, unique_terms))
