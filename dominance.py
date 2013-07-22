import * from measures

##################### SIMILARITY ########################
def cluster_structural_similarity(cluster1, cluster2):
    """ compute the similarity between cluster1 and cluster2. basically it is a pair of object 
    similarity and dimension similarity. and by similarity we mean precision """
    object_similarity = precision_sets(cluster1.objects, cluster2.objects)
    dimension_similarity = precision_sets(cluster1.dimensions, cluster2.dimensions)

    return (object_similarity, dimensions_similarity)

def is_structurally_similar_to(ref_cluster, target_cluster, object_threshold = 0.5, dimension_threshold = 0.5):
    """ checks whether the ref cluster is simlar to target cluster, w.r.t the two threshold. this relation is
    based on the calculation of precision, thus not being symetric nor transitive """
    object_similarity, dimensions_similarity = cluster_structural_similarity(ref_cluster, target_cluster)
    return object_similarity >= object_threshold and dimensions_similarity >= dimension_threshold

def is_inferior_to(ref_cluster, target_cluster, func):
    """ check whether a ref_cluser is inferior to another one w.r.t a evaluator f """
    return func(ref_cluster) < target_cluster

def is_dominated_by(ref_cluster, target_cluster, func, objs_threshold = 0.5, dims_threshold = 0.5):
    """ check whether a ref_cluser is inferior to another one w.r.t a evaluator f """
    return is_inferior_to(ref_cluster, target_cluster, func) and  is_structurally_similar_to(ref_cluster, target_cluster, object_threshold, dimension_threshold))

############################################## DOMINANCE #########################################
def non_dominated_clusters(clusters, func, dim_thres = 0.5, obj_thres = 0.5, filtered = False):
    """ filter out the non_dominated ones from a set of clusters. the processus of non_dominated finding
    is a bit complicated..

    it consists of:
    1. find a set of non_dominated (either dominant or isolated), called A
    2. among dominated: find the those who are not being by any of A, called B
    3. the result is the merge of A&B"""
    
    clusters = clustering.clusters
    sorted(clusters, key = func, reverse = True)
    sz = len(clusters) # nbr of clusters contained in this clustering
    idx = 0*np.ones([sz]) # a sz-size array of zeroes

    dominance = {}
    for i in xrange(sz):
        clA = clusters[i]
        for j in xrange(i+1, sz):
            clB = clusters[j]                 
            if is_dominated_by(clB, clA, func, dim_thres, obj_thres):
                dominance.setdefault(j, set())
                dominance[j].add(i)

    dominated_candidates = dominance.keys()
    non_dominated = [i for i in xrange(sz) if i not in dominated]
    for cand in dominated_candidates:
        selected = True
        for non_dom in non_dominated:
            if is_dominated_by(cand, non_dom, func, dim_thres, obj_thres):
                selected = False
                break
        if selected:
            non_dominated.append(cand)
                    
    return non_dominated

def non_dominated_clustering(clusterings, func, dim_thres = 0.5, obj_thres = 0.5, filtered = False):
    """ patch redundancy filtering for a list of clusterings """
    pass
