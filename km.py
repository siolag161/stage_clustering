from clustering import *

######################################################################################
""" classes """

class KMClustering(SubspaceClustering, MeasureMixin):
    """ basically it is a subspace clustering but might contain some additonal information such as a list of measures/values"""
    def __init__(self, algorithm, parameters, run,
                 clustering_id = None, **measures):

        SubspaceClustering.__init__(self, algorithm, parameters, run, clustering_id)
        MeasureMixin.__init__(self, **measures)

######################################################################################
""" useful helper functions """
def my_combi(data, dimensions, projection_dimension_size):
    """ at each yield, return a k-combination project from a data of n-dimensions """
    from itertools import combinations
    for projection in combinations(dimensions, projection_dimension_size):
        yield data[:,projection], projection


######################################  K-MEANS ################################################

def kmeans(dims_arg, ite = 50, k = 4, threshold = 1e-5):
    """ perform k_keamns clustering and return a the result as a subsapce clustering object """
    from scipy.cluster.vq import kmeans, vq
 
    features, dims = dims_arg       
    
    centroids, distance = kmeans(features, k, iter=ite, thresh=threshold)
    code, _ = vq(features, centroids)    
    
    spatial_coherence = spatial_coherence_compute(code, k)
    
    km_clt = km_clustering(dims, code)
    km_clt.distortion = distance
    km_clt.spatial_coherence = spatial_coherence
    
    return  km_clt 

def kmeans_args(params):
    dims_arg, ite, k, threshold = params
    return kmeans(dims_arg, ite, k, threshold)

def kmeans_execute(data, dimensions, dimensions_size, number_of_clusters = 4, processes = 7):
    pool = multiprocessing.Pool(processes)
    dims_iter = my_combi(data, dimensions, dimensions_size)    
    rs = pool.map(kmeans_args, [dims_iter, 30, number_of_clusters, 1e-5])
    pool.close()
    pool.join()
    
    return rs
