import numpy as np

def pareto_frontier(clusterings, measures, reverse = []):
    """ get a list of clusterings based on the measure indexes passed in the arguments """
    clusterings.sort(key = lambda(x): x.get_value(measures[0]), reverse = False)
    
    pareto_frontier = [clusterings[0]]
    for clustering in clusterings[1:]:        
        if sum(clustering.get_value(measure) >= pareto_frontier[-1].get_value(measure) for measure in measures) != len(measures):
            pareto_frontier.append(clustering)

    print "########################################"
    for c in pareto_frontier:
        print c.get_value('spatial_coherence'), c.get_value('distortion')

    return pareto_frontier
