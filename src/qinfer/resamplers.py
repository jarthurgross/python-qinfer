#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# resamplers.py: Implementations of various resampling algorithms.
##
# © 2012 Chris Ferrie (csferrie@gmail.com) and
#        Christopher E. Granade (cgranade@gmail.com)
#     
# This file is a part of the Qinfer project.
# Licensed under the AGPL version 3.
##
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

## FEATURES ####################################################################

from __future__ import division

## ALL #########################################################################

# We use __all__ to restrict what globals are visible to external modules.
__all__ = [
    'ClusteringResampler',
    'LiuWestResampler'
]

## IMPORTS #####################################################################

import numpy as np
import scipy.linalg as la
import warnings

from utils import outer_product, particle_meanfn, particle_covariance_mtx

try:
    import sklearn
    import sklearn.cluster
except ImportError:
    warnings.warn("Could not import scikit-learn. Some features may not work.")
    sklearn = None

## CLASSES #####################################################################

class ClusteringResampler(object):
    r"""
    Creates a resampler that breaks the particles into clusters, then applies
    a secondary resampling algorithm to each cluster independently.
    
    :param secondary_resampler: Resampling algorithm to be applied to each
        cluster. If ``None``, defaults to ``LiuWestResampler()``.
    """
    
    def __init__(self, secondary_resampler=None, quiet=True):
        self.secondary_resampler = (
            secondary_resampler
            if secondary_resampler is not None
            else LiuWestResampler()
        )
        self.quiet = quiet
        
    ## METHODS ##
    
    def __call__(self, model, particle_weights, particle_locations):
        ## TODO: docstring.
        
        # Allocate new arrays to hold the weights and locations.        
        new_weights = np.empty(particle_weights.shape)
        new_locs    = np.empty(particle_locations.shape)
        
        # Create and run a SciKit-Learn DBSCAN clusterer.
        clusterer = sklearn.cluster.DBSCAN()
        cluster_labels = clusterer.fit_predict(particle_locations)
        
        # Find out how many clusters were identified.
        # Cluster counting logic from:
        # [http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html].
        n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
        if not self.quiet:
            print "[Resampling] DBSCAN identified {} cluster{}.".format(n_clusters, "s" if n_clusters > 1 else "")
        
        # Loop over clusters, calling the secondary resampler for each.
        for idx_cluster in xrange(n_clusters):
            # Grab a boolean array identifying the particles in a  particular
            # cluster.
            this_cluster = cluster_labels == idx_cluster
            
            # Pass the particles in that cluster to the secondary resampler
            # and record the new weights and locations.
            cluster_ws, cluster_locs = self.secondary_resampler(model,
                particle_weights[this_cluster],
                particle_locations[this_cluster]
            )
            
            # Renormalize the weights of each resampled particle by the total
            # weight of the cluster to which it belongs.
            cluster_ws /= np.sum(particle_weights[this_cluster])
            
            # Store the updated cluster.
            new_weights[this_cluster] = cluster_ws
            new_locs[this_cluster]    = cluster_locs
            
        return new_weights, new_locs

class LiuWestResampler(object):
    r"""
    Creates a resampler instance that applies the algorithm of
    Liu and West (2000) to redistribute the particles.
    
    :param float a: Value of the Liu and West parameter :math:`a` to be used
        by the resampler.
    """
    def __init__(self, a=0.98, renormalize=False):
        self.a = a # Implicitly calls the property setter below to set _h.

    ## PROPERTIES ##

    @property
    def a(self):
        return self._a
        
    @a.setter
    def a(self, new_a):
        self._a = new_a
        self._h = np.sqrt(1 - new_a**2)

    ## METHODS ##
    
    def __call__(self, model, particle_weights, particle_locations):
        """
        Resample the particles according to algorithm given in 
        Liu and West (2000).
        """
        
        # Give shorter names to weights and locations.
        w, l = particle_weights, particle_locations
        
        # parameters in the Liu and West algorithm
        mean, cov = particle_meanfn(w, l, lambda x: x), particle_covariance_mtx(w, l)
        a, h = self._a, self._h
        S, S_err = la.sqrtm(cov, disp=False)
    	S = np.real(h * S)
        n_ms, n_mp = l.shape
        
        new_locs = np.empty(l.shape)        
        cumsum_weights = np.cumsum(w)[:, np.newaxis]
        
        idxs_to_resample = np.arange(n_ms)
        
        # Loop as long as there are any particles left to resample.
        while idxs_to_resample.size:
            # Draw j with probability self.particle_weights[j].
            js = np.argmax(np.random.random(size = (1, idxs_to_resample.size)) < cumsum_weights[idxs_to_resample], axis=0)
            
            # Set mu_i to a x_j + (1 - a) mu.
            mus = a * l[js,:] + (1 - a) * mean
            
            # Draw x_i from N(mu_i, S).
            new_locs[idxs_to_resample, :] = mus + np.dot(S, np.random.randn(n_mp, mus.shape[0])).T
            
            # Now we remove from the list any valid models.
            idxs_to_resample = idxs_to_resample[np.nonzero(np.logical_not(
                model.are_models_valid(new_locs[idxs_to_resample, :])
            ))[0]]


        # Now we reset the weights to be uniform, letting the density of
        # particles represent the information that used to be stored in the
        # weights.
        return np.ones((w.shape[0],)) / w.shape[0], new_locs
        
    
