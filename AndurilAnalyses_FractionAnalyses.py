"""This pipeline is for the analyses of segmented anduril particles.
"""

import sys
sys.path.insert(0,'/home/crg/Documents/Code/pacMan/')

import tifffile as t
import numpy as np
import skimage.morphology as morph
import matplotlib.pyplot as plt


solidSampleName = [	'Sample1_Solid.tif',
					'Sample2_Solid.tif',
					'Sample3_Solid.tif',
					]

voidSampleName = [	'Sample1_InternalVoid.tif',
					'Sample2_InternalVoid.tif',
					'Sample3_InternalVoid.tif',
					]

ifl = '/home/crg/Documents/Datasets/Anduril/PostAvizo/'
ofl = '/home/crg/Documents/Datasets/Anduril/PostAvizo/'

for i in range(0,3):
	"""
	"""
	print(i)
	print('start')

	voidData = t.imread( ofl + voidSampleName[i] ).astype('uint16')
	solidData = t.imread( ofl + solidSampleName[i]).astype('uint16')

	voidData = voidData // voidData.max()
	solidData = solidData // solidData.max()

	internalVoidVolume = voidData.sum()
	solidVolume = solidData.sum()
	totalVolume = solidData.shape[0] * solidData.shape[1] * solidData.shape[2]

	data = np.array([[totalVolume],[solidVolume],[internalVoidVolume]])

	np.savetxt(ofl+'VolumeData-'+str(i+1)+'.csv',data, delimiter=',')