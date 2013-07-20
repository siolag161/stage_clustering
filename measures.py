from clustering import *

####################################################### SPATIAL COHERENCE #######################################################
def cluster_label_change(cluster, max_size):
    l = len(cluster.objects)
    if l == 0: return 0
    cluster = list(cluster.objects) #list(cluster)

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
    if not expected: return 0.0

    return float(nbr_changes-expected)/(cardinality-expected), 1
