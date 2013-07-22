
########## CLASSES #################
def string_to_set(string, sep = ","):
    objects = set([int(elem) for elem in string.split(sep)])
    return objects

def list_to_string(set_of_elements, sep = ","):
    elements = list(set_of_elements)
    return sep.join([str(elem) for elem in elements])
    
class SubspaceCluster:
    """
    a class representing a subspace cluster
    i.e. pair of objects/dimensions
     """
    def __init__(self, clustering_id, objects, dimensions):
        self.clustering_id = clustering_id
        self._process_objects(objects)
        self._process_dimensions(dimensions)
        

    def __str__(self):
        """ TODO: """
        _str = "[objects = %s] - [dimensions = %s]" %(self.objects_str, self.dimensions_str)
        return _str

    def _process_objects(self, objects, sep = ","):        
        typename = objects.__class__.__name__
        if (typename == 'str'):
            self.objects = string_to_set(objects, sep)            
            self.objects_str = objects
        else:
            """ list or set """
            self.objects = set(objects)
            self.objects_str = list_to_string(self.objects)
            
    
    def _process_dimensions(self, dimensions, sep = ","):
        typename = dimensions.__class__.__name__
        if (typename == 'str'):
            self.dimensions = string_to_set(dimensions, sep)            
            self.dimensions_str = dimensions
        else:
            """ list or set """
            self.dimensions = set(dimensions)
            self.dimensions_str = list_to_string(self.dimensions)

    
class SubspaceClustering:
    """ a class representing a subspace clustering: list of clusters"""
    def __init__(self, algorithm, parameters, run,
                 clustering_id = None, clusters = [],  
                 contains_noise = False, clustering_on_dimension = False):
        self.algorithm = algorithm
        self.parameters = parameters
        self.run = run
        self.clusters = clusters
        
        self.contains_noise = contains_noise        
        self.clustering_on_dimension = clustering_on_dimension # to determine wherether we distingust clustering by their dimension projection or by run

        if not clustering_id:
            self.clustering_id = self._generate_id()
        else:
            self.clustering_id  = clustering_id

    def set_contains_noise(self, val):
        self.contains_noise = val
            
    def contains_noise(self):
        return self.contains_noise

    def set_clustering_on_dimension(self, val):
        self.clustering_on_dimension = val
        self.clustering_id = self._generate_id()

    def _generate_id(self):
        if self.clustering_on_dimension:
            print 'hello!!!'
            clustering_id = "%s_%s_%s_%s" %(self.algorithm, self.parameters, str(self.run), self.clusters[0].dimensions_str)
        else:
            clustering_id = "%s_%s_%s" %(self.algorithm,self. parameters, str(self.run))
                
        return clustering_id

    def get_objects(self):
        """ return the union of all objects from all clusters """
        objs = set()
        for cluster in self.clusters:
            objs.update(cluster.objects)

        return objs

    def add_cluster(self, cluster):
        if not cluster.clustering_id and self.clustering_id:
            cluster.clustering_id = self.clustering_id
        
        if self.clustering_id == cluster.clustering_id:
            self.clusters.append(cluster)

    def __key(self):
        return self.generate_id()

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())
        
    
class MeasureMixin:
    """ mixins (a particular pythnic syntatic sugar) for measures/values dictionary """
    from collections import defaultdict
    def __init__(self, **measures):
        if measures:
            self.measures = measures
        else:
            self.measures = {}

    def set_value(self, key, value):
        self.measures[key] = value

    def get_value(self, key):
        return self.measures.get(key)

    def update_measures(self, measures):
        self.measures.update(measures)

    def get_measure_names(self):
        return self.measures.keys()    
    

##################################### import/export from CSV  ####################################
FIELD_NAMES = ["algorithm", "parameters", "run", "dimensions", "objects"]  
    
def write_clustering(clusterings, basic_fields, measure_fields, ofile, with_clusters = True):
    """ write to file the clustering with optional additional measure fields. 
    the with_cluster indicates wherether we write at clustering or cluster level"""
    import csv
    with open(ofile, 'wb') as out_file:
        print("writing data to %s..." %(ofile))

        fields = list(basic_fields)
        fields.extend(measure_fields)
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
        writer.writerow(dict((fn,fn) for fn in fields))
        
        for clustering in clusterings:
            for cluster in clustering.clusters:
                row_basic = dict((fn, clustering.__dict__[fn]) for fn in basic_fields if  clustering.__dict__.has_key(fn))
                row_basic.update(dict((fn, cluster.__dict__[fn]) for fn in basic_fields if  cluster.__dict__.has_key(fn)))
                row_measure = dict((fn, clustering.get_value(fn)) for fn in measure_fields)
                
                row = dict(row_basic)
                row.update(row_measure)

                if with_clusters:
                    row.update({'objects': cluster.objects_str, 'dimensions': cluster.dimensions_str})

                    #print row                
                writer.writerow(row)

def read_clustering(ifile, field_names, is_cluster = True, contains_noise_ = False, clustering_on_dimension_ = False):
    """ import clustering from a csv-like text file. the field names are used to limit the fields we want to read
    return a list of clusterings. """
    import csv

    clusterings = {}
    with open(ofile, 'rb') as in_file:
        print("reading %s to get data..." %(ifile))
        file_dialect = csv.Sniffer().sniff(in_file.read(1024))
        in_file.seek(0)
        
        reader = csv.DictReader(csvfile = in_file, fieldnames = field_names, dialect = file_dialect)
        reader.next()

        line_count = 0
        for row in reader:
            clustering = SubspaceClustering(row['algorithm'], row['parameters'], row['run'],
                 row['clustering_id'], clusters = [], contains_noise = contains_noise_, clustering_on_dimension =  clustering_on_dimension_)

            clustering_id = clustering._generate_id()
            clusterings.setdefault(clustering_id, clustering)
            
            if (is_cluster):                
                cluster = SubspaceCluster(clustering_id, dimensions = str(row['dimensions']), objects = str(row['objects']))
                clusterings[clustering_id].add_cluster(cluster)
            else:
                pass
    return clusterings.values() 

###############################################################################################################
def read_matrix_data(ifile):
    """ read from an extended bedgraph-like file to a numpy array"""
    import csv
    import numpy as np
    with open(ifile, 'rb') as in_file:
        print("reading %s to get data..." %(ifile))
        file_dialect = csv.Sniffer().sniff(in_file.read(1024))
        in_file.seek(0)
        
        reader = csv.reader(in_file, dialect = file_dialect)
        reader.next()

        line_count = 0
        for row in reader:
            line_count += 1
            vals = row[3:]
            if (line_count == 1):
                data = np.array(vals, dtype=np.float64)
            else:
                data = np.vstack((data, np.array(vals, dtype=np.float64)))
                
        return data


        
