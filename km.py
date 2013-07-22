from clustering import *
import numpy as np

######################################################################################
""" classes """

class KMClustering(SubspaceClustering, MeasureMixin):
    """ basically it is a subspace clustering but might contain some additonal information such as a list of measures/values"""
    def __init__(self, algorithm, parameters, run,
                 clustering_id = None, **measures):

        SubspaceClustering.__init__(self, algorithm, parameters, run, clustering_id,
                                    contains_noise = False, clustering_on_dimension = False)
        MeasureMixin.__init__(self, **measures)

######################################################################################
""" useful helper functions """
def my_combi(data, dimensions, projection_dimension_size, nbr_step = 50, number_of_clusters = 4, threshold = 1e-5):
    """ at each yield, return a k-combination project from a data of n-dimensions """
    from itertools import combinations
    for projection in combinations(dimensions, projection_dimension_size):
        yield data[:,projection], projection, nbr_step, number_of_clusters, threshold


######################################  K-MEANS ################################################

def clusters_from_code(code, nbr_of_cluster, dims):
    import numpy as np
    clusters = []

    
    dims = set(dims)
    for label in xrange(nbr_of_cluster):
        objs = set(np.where(code == label)[0])
        #print np.where(code == label)
        cluster = SubspaceCluster(clustering_id = None, objects = objs, dimensions = dims)
        clusters.append(cluster) 
    
    return clusters
        
def kmeans(features, projection, ite = 50, k = 4, threshold = 1e-5):    
    """ perform k_keamns clustering and return a the result as a subsapce clustering object """
    from scipy.cluster.vq import kmeans, vq
    import datetime

    from measures import spatial_coherence
    
    #features = dims_arg       
    
    centroids, distance = kmeans(features, k, iter=ite, thresh=threshold)
    code, _ = vq(features, centroids)


    run_ = datetime.datetime.now().strftime("%y_%m_%d_%H_%M")
    params = "projection_size=%d, k=%d" %(len(projection), k)
    km_clt = KMClustering(algorithm ="exhaustive_kmeans", parameters = params, run = run_, clustering_id = None)
    clusters = clusters_from_code(code, k, projection)
    for cluster in clusters:
        km_clt.add_cluster(cluster)

    measures = {'spatial_coherence': spatial_coherence(km_clt, len(features))[0], 'distortion': distance}
    km_clt.update_measures(measures)
    
    return  km_clt 

def kmeans_args(params):
    data, projection, ite, k, threshold = params
    return kmeans(data, projection, ite, k, threshold)

def kmeans_execute(data, dimensions_size, number_of_clusters = 4, processes = 7):    
    import multiprocessing
    """ the data here is an numpy multi-array"""
    
    pool = multiprocessing.Pool(processes)

    dimensions = np.shape(data)[1]    
    features = my_combi(data, xrange(dimensions), dimensions_size)      
    rs = pool.map(kmeans_args, features)    
    pool.close()
    pool.join()
    
    return rs
