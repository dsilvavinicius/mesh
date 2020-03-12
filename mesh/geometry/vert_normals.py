#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2013 Max Planck Society. All rights reserved.
# Created by Matthew Loper on 2013-03-12.


import scipy.sparse as sp
import numpy as np
from .tri_normals import NormalizedNx3, TriNormalsScaled
from ..utils import col


def normalize_v3(arr):
    ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
    lens = np.sqrt( arr[:,0]**2 + arr[:,1]**2 + arr[:,2]**2 )
    arr[:, 0] /= lens
    arr[:, 1] /= lens
    arr[:, 2] /= lens
    return arr


def vert_normals(v, f):
    """Source: https://sites.google.com/site/dlampetest/python/calculating-normals-of-a-triangle-mesh-using-numpy"""
    # Create a zeroed array with the same type and shape as our vertices i.e., per vertex normal
    norm = np.zeros(v.shape, dtype=v.dtype)
    # Create an indexed view into the vertex array using the array of three indices for triangles
    tris = v[f]
    # Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each
    # triangle
    n = np.cross(tris[::, 1] - tris[::, 0], tris[::, 2] - tris[::, 0])
    # n is now an array of normals per triangle. The length of each normal is dependent the vertices,
    # we need to normalize these, so that our next step weights each normal equally.
    normalize_v3(n)
    # now we have a normalized array of normals, one per triangle, i.e., per triangle normals.
    # But instead of one per triangle (i.e., flat shading), we add to each vertex in that triangle,
    # the triangles' normal. Multiple triangles would then contribute to every vertex, so we need to normalize again
    # afterwards.
    # The cool part, we can actually add the normals through an indexed view of our (zeroed) per vertex normal array
    norm[f[:, 0]] += n
    norm[f[:, 1]] += n
    norm[f[:, 2]] += n
    normalize_v3(norm)
    return norm

# def MatVecMult(mtx, vec):
#     return mtx.dot(col(vec)).flatten()
#
#
# def VertNormals(v, f):
#     return NormalizedNx3(VertNormalsScaled(v, f))
#
#
# def VertNormalsScaled(v, f):
#     IS = f.flatten()
#     JS = np.array([range(f.shape[0])] * 3).T.flatten()
#     data = np.ones(len(JS))
#
#     IS = np.concatenate((IS * 3, IS * 3 + 1, IS * 3 + 2))
#     JS = np.concatenate((JS * 3, JS * 3 + 1, JS * 3 + 2))  # is this right?
#     data = np.concatenate((data, data, data))
#
#     faces_by_vertex = sp.csc_matrix((data, (IS, JS)), shape=(v.size, f.size))
#
#     # faces_by_vertex should be 3 x wider...?
#     return NormalizedNx3(MatVecMult(faces_by_vertex, TriNormalsScaled(v, f)))
