from clustering import *
import numpy as np

######################################################################################

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


        
############################################### Entry point ##########################################################
import sys, getopt
from numpy import random
from numpy.random import rand

def usage():
     print '[USAGE]: km.py -i <inputfile> -o <outputfile> -d <size of dimension projection> -n <number of clusters> -p <number of parallel processes>'
     
def main(argv):
    inputfile = ''
    outputfile = ''
    dsize = 4
    nclust = 4
    proc = 1
        
    try:
        opts, args = getopt.getopt(argv,"hi:o:d:n:p:",["ifile=","ofile=","dsize","nclust","proc"])
    except getopt.GetoptError:    
        usage()    
        sys.exit(2)
                
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d", "--dize"):
            dsize = int(arg)
        elif opt in ("-n", "--nclust"):
            nclust = int(arg)
        elif opt in ("-p", "--proc"):
            proc = int(arg)
            
    data =  read_matrix_data(inputfile)
    print 'done reading...'
    import time
    from scipy.cluster.vq import whiten
    random.seed((1030,2000))

    #whiten datasomewhere
    print 'begin executing kmeans...'
    km = kmeans_execute(data, dimensions_size = dsize, number_of_clusters = nclust, processes = proc)
    print 'done executing kmeans...'
    write_clustering(km, basic_fields = FIELD_BASIC, measure_fields = FIELD_MEASURE,  
                     ofile = outputfile, with_clusters = True)
    
if __name__ == "__main__":
    main(sys.argv[1:])
