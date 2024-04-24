"""This pipeline is for the analyses of segmented anduril particles.
"""

import sys
sys.path.insert(0,'/home/crg/Documents/Code/pacMan/')

import tifffile as t
import numpy as np
import skimage.morphology as morph
import matplotlib.pyplot as plt


solidSampleName = [	'PostAvizo_Sample1_p_h1_rr6-correctedLabelMap-noEdgeCorrectedLabelMap.tif',
					'PostAvizo_Sample2_p_h1_rr6-correctedLabelMap-noEdgeCorrectedLabelMap.tif',
					'PostAvizo_Sample3_p_h1_rr6-correctedLabelMap-noEdgeCorrectedLabelMap.tif',
					]

voidSampleName = [	'PostAvizo_Sample1_v_h3_rr5-correctedLabelMap-noEdgeCorrectedLabelMap.tif',
					'PostAvizo_Sample2_v_h3_rr5-correctedLabelMap-noEdgeCorrectedLabelMap.tif',
					'PostAvizo_Sample3_v_h3_rr5-correctedLabelMap-noEdgeCorrectedLabelMap.tif',
					]

ifl = '/home/crg/Documents/Datasets/Anduril/PostAvizo/output/'
ofl = '/home/crg/Documents/Datasets/Anduril/PostAvizo/output/'

for i in range(0,3):
	"""
	"""
	print(i)
	print('start')

	voidData = t.imread( ofl + voidSampleName[i] ).astype('uint16')
	solidData = t.imread( ofl + solidSampleName[i]).astype('uint16')

	voidData[np.where(voidData != 0)] = 1
	dilVoidData = morph.binary_dilation(voidData).astype('uint16')
	dilVoidData = dilVoidData//dilVoidData.max()
	plt.imshow(dilVoidData[30]);plt.show()

	dilVoidData[np.where(dilVoidData == 1)] = 5000
	voidSolidOverlap = solidData + dilVoidData
	plt.imshow(voidSolidOverlap[30]);plt.show()
	voidSolidOverlap[np.where(voidSolidOverlap <= 5000)] = 0
	plt.imshow(voidSolidOverlap[30]);plt.show()


	listOfParticles = np.unique(voidSolidOverlap)
	listOfParticles -= 5000
	print('end')

	np.savetxt(ofl+'ParticlesWithVoids-'+str(i+1)+'.csv',listOfParticles, delimiter=',')