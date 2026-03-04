# -*- coding: utf-8 -*-
# Much of the core functionality in these scripts comes from
# the fine tutorial demonstrations on the Mayavi website.
# I've included the original boilerplate for attribution
# below.

# Author: Gael Varoquaux <gael.varoquaux@normalesup.org>
# Copyright (c) 2008, Enthought, Inc.
# License: BSD Style.

from __future__ import division
import numpy as np
import Hydrogenic as hyd
from mayavi import mlab
import time

# Create a dense grid of points - These are each three dimensional arrays
x, y, z = np.mgrid[- 20:20:150j, - 20:20:150j, - 20:20:150j]

# Convert those points into spherical space
r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
phi = np.arccos(z/r)
theta = np.arctan(y/x)

# Pull the functions for a 3pz orbital from my Hydrogenic module
orbital = hyd.Orbital(3, 1, 0, 1)
L = orbital.radial
A = orbital.angular

# find values of Ψ, Ψ*Ψ, and the phase at all points
Psi = L(r) * A(theta, phi)
Density = (np.conj(Psi)*Psi).real # Ψ*Ψ
phase = np.angle(Psi)

# Now we need to find the correct isovalue
# First collapse the three-dimensional array into a one-dimensional array
collapsed = np.ndarray.flatten(Density)
# Sort the array in descending order
sorted_list = np.sort(collapsed)[::-1]
total = np.sum(sorted_list)
# Add up the values until 75% is reached
running_total = 0
index = 0
while running_total < 0.75*total:
    this_val = sorted_list[index]
    running_total = running_total + this_val
    index = index + 1
isovalue = this_val
# Plot it ####################################################################

mlab.figure(1, fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))
# We create a scalar field with the module of Phi as the scalar
src = mlab.pipeline.scalar_field(x, y, z, Density)

# And we add the phase of Phi as an additional array
# This is a tricky part: the layout of the new array needs to be the same
# as the existing dataset, and no checks are performed. The shape needs
# to be the same, and so should the data. Failure to do so can result in
# segfaults.
src.image_data.point_data.add_array(phase.T.ravel())
# We need to give a name to our new dataset.
src.image_data.point_data.get_array(1).name = 'angle'
# Make sure that the dataset is up to date with the different arrays:
src.update()

# We select the 'scalar' attribute, ie the norm of Phi
src2 = mlab.pipeline.set_active_attribute(src)#,
                                    #point_scalars='scalar')

# Cut isosurfaces of the norm
contour = mlab.pipeline.contour(src2)
contour.filter.contours= [isovalue]

# Now we select the 'angle' attribute, ie the phase of Phi
contour2 = mlab.pipeline.set_active_attribute(contour,
                                    point_scalars='angle')

# And we display the surface. The colormap is the current attribute: the phase.
mlab.pipeline.surface(contour2, colormap='hsv', vmax=np.pi, vmin=-np.pi)
mlab.colorbar(title='Phase', orientation='vertical', nb_labels=5)
mlab.view(-10, 90)
mlab.show()

# Now a trial to see just how long it takes to animate

# Create an mlab scene
mlab.figure(1, fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))
# We create a scalar field with the module of Phi as the scalar
src = mlab.pipeline.scalar_field(x, y, z, Density)

# And we add the phase of Phi as an additional array
# This is a tricky part: the layout of the new array needs to be the same
# as the existing dataset, and no checks are performed. The shape needs
# to be the same, and so should the data. Failure to do so can result in
# segfaults.
src.image_data.point_data.add_array(phase.T.ravel())
# We need to give a name to our new dataset.
src.image_data.point_data.get_array(1).name = 'angle'
# Make sure that the dataset is up to date with the different arrays:
src.update()

# We select the 'scalar' attribute, ie the norm of Phi
src2 = mlab.pipeline.set_active_attribute(src)#,
                                    #point_scalars='scalar')

# Cut isosurfaces of the norm
contour = mlab.pipeline.contour(src2)
contour.filter.contours= [isovalue]

# Now we select the 'angle' attribute, ie the phase of Phi
contour2 = mlab.pipeline.set_active_attribute(contour,
                                    point_scalars='angle')

# And we display the surface. The colormap is the current attribute: the phase.
mlab.pipeline.surface(contour2, colormap='hsv', vmax=np.pi, vmin=-np.pi)
mlab.colorbar(title='Phase', orientation='vertical', nb_labels=5)
mlab.view(-10, 90)
mlab.show()

last_time = time.time()
for t in np.linspace(0,np.pi/2.0,10):
    orbital1 = hyd.Orbital(3, 1, 0, 1)
    L1 = orbital.radial
    A1 = orbital.angular

    orbital2 = hyd.Orbital(2, 0, 0, 1)
    L2 = orbital2.radial
    A2 = orbital2.angular
    # find values of Ψ, Ψ*Ψ, and the phase at all points
    Psi = np.cos(t)*(L(r) * A(theta, phi)) + np.sin(t)*(L2(r)*A2(theta,phi))
    Density = (np.conj(Psi)*Psi).real # Ψ*Ψ
    phase = np.angle(Psi)

    # Now we need to find the correct isovalue
    # First collapse the three-dimensional array into a one-dimensional array
    collapsed = np.ndarray.flatten(Density)
    # Sort the array in descending order
    sorted_list = np.sort(collapsed)[::-1]
    total = np.sum(sorted_list)
    # Add up the values until 75% is reached
    running_total = 0
    index = 0
    while running_total < 0.75*total:
        this_val = sorted_list[index]
        running_total = running_total + this_val
        index = index + 1
    isovalue = this_val
    # Plot it ####################################################################

    mlab.clf()
    # We create a scalar field with the module of Phi as the scalar
    src = mlab.pipeline.scalar_field(x, y, z, Density)

    # And we add the phase of Phi as an additional array
    # This is a tricky part: the layout of the new array needs to be the same
    # as the existing dataset, and no checks are performed. The shape needs
    # to be the same, and so should the data. Failure to do so can result in
    # segfaults.
    src.image_data.point_data.add_array(phase.T.ravel())
    # We need to give a name to our new dataset.
    src.image_data.point_data.get_array(1).name = 'angle'
    # Make sure that the dataset is up to date with the different arrays:
    src.update()

    # We select the 'scalar' attribute, ie the norm of Phi
    src2 = mlab.pipeline.set_active_attribute(src)#,
                                        #point_scalars='scalar')

    # Cut isosurfaces of the norm
    contour = mlab.pipeline.contour(src2)
    contour.filter.contours= [isovalue]

    # Now we select the 'angle' attribute, ie the phase of Phi
    contour2 = mlab.pipeline.set_active_attribute(contour,
                                        point_scalars='angle')

    # And we display the surface. The colormap is the current attribute: the phase.
    mlab.pipeline.surface(contour2, colormap='hsv', vmax=np.pi, vmin=-np.pi)
    mlab.colorbar(title='Phase', orientation='vertical', nb_labels=5)
    mlab.view(-10, 90)
    new_time = time.time()
    print(isovalue)
    print(new_time-last_time)
    last_time = new_time