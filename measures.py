from clustering import *

####################################################### SPATIAL COHERENCE #######################################################
def cluster_label_change(cluster, max_size):
    l = len(cluster.objects)
    if l == 0: return 0
    cluster = sorted(cluster.objects) #list(cluster)

    nbr = 0
    nxt = cluster[l-1]

    for i in range(l-1):
        cur = cluster[i]
        nxt = cluster[i+1]
        if (cur+1) != nxt: 
            nbr += 1
    if nxt != max_size-1:
        nbr += 1
    return nbr
    
def clustering_label_change(clustering, max_size):
    """ count the number of label changes for each clustering"""
    if not clustering.clusters:
        return 0
    total = sum([cluster_label_change(clt, max_size) for clt in clustering.clusters])    
    return total

def expected_number_of_changes(clustering, max_size):
    """ expected number """
    nbr_of_clusters = len(clustering.clusters)
    if (nbr_of_clusters == 0): 
        return 0
    sum_of_square = 0
    for cluster in clustering.clusters:
        sum_of_square += len(cluster.objects)**2
    return max_size-sum_of_square*1.0/max_size

def spatial_coherence(clustering, cardinality):    
    """ the tricky part about computing this measure lies in the fact that some clustering contains only non-noise clusters.
    meaning that sometime we have to know the cardinality of the whole dataset"""
    from collections import defaultdict

    if clustering.contains_noise:
        """ add the noisy part as an additional cluster """
        all_objects = set(range(cardinality)) # all objects possible from the data space
        other_objects = all_objects.difference(clustering.get_objects())
        other_cluster = SubspaceCluster(clustering_id = clustering.clustering_id, objects = other_objects, dimensions="")
        all_clusters  = clustering.clusters.append(other_cluster)
        
    
    nbr_changes = clustering_label_change(clustering, cardinality)
    expected  = expected_number_of_changes(clustering, cardinality)

    #print "nbr_changes=%s, expected=%s" %(nbr_changes, expected)
    if not expected: return 0.0, 1

    return float(nbr_changes-expected)/(cardinality-expected), 1

####################################################### Similarities #######################################################
# 2 helpers for computing the precision and the recall between 2 sets
def set_convert(ls):
    if ls.__class__.__name__ !='set':
        ls = set(ls)
    return ls

def precision_sets(set1, set2):
    """ computes the precision score of 2 sets"""

    set1, set2 = set_convert(set1), set_convert(set2)
    intersection = set1.intersection(set2)
    if set1:
        return float(len(intersection))/len(set1)
    return 0.0

def recall_sets(set1, set2):
    """ computes the recall of 2 sets """
    return precision_sets(set2, set1)

#f1
def f1_score(set1, set2, beta = 1):
    """ if b > 1 that means the completeness is more important (weighted more) than the homogeneity """
    precision = precision_sets(set1, set2)
    recall = recall_sets(set1, set2)

    if (precision+recall == 0): return 0.0

    return (1+beta)*(precision*recall)/(beta*precision+recall)

#cluster_similarity
def cluster_similarity(cluster1, cluster2):
    """ compute the similarity between cluster1 and cluster2. basically it is a pair of object 
    similarity and dimension similarity. and by similarity we mean precision """
    object_similarity = precision_sets(cluster1.objects, cluster2.objects)
    dimension_similarity = precision_sets(cluster1.dimensions, cluster2.dimensions)

    return (object_similarity, dimensions_similarity)


####################################################### F1-Score #####################################################
def best_hidden_cluster_matches(ref_clustering, target_clustering, beta = 1):
    mapped_hidden = {}
    hidden_clusters = ref_clustering.clusters

    for clust in clusters:            
        mapped_precision = -1
        for hclust in hidden_clusters:
            precision = precision_sets(hclust.objects, clust.objects)
            if precision > mapped_precision:
                mapped_precision = precision
        if mapped_precision > 0:
            for hclust in hidden_clusters:
                if mapped_precision == precision_sets(hclust.objects, clust.objects):
                    mapped_hidden.setdefault(hclust, set())
                    mapped_hidden[hclust].update(clust.objects)
    return mapped_hidden
                

def f1_score_clustering(ref_clustering, target_clustering, beta = 1):
    if not ref_clustering.clusters or not target_clustering.clusters:
        return 0.0

    nbr_of_hidden = len(ref_clustering.clusters) # number of hidden clusters
    best_matches = 

####################################################### Entropy #######################################################


#######################################################  #######################################################
