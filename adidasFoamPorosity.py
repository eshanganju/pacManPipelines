"""Calculate the porosity in the samples
"""

import numpy as np
from numba import jit
import tifffile as tf
import time

VERBOSE = True


@jit(nopython=True)
def getPorosityMap(binMap,patchSize=50):
	"""Calculates the porosity (volume of pores/total volume) for the sample with a patch size
	"""
	porosityMap = np.zeros_like(binMap)

	strtIdx = patchSize//2 
	endIdxZ = binMap.shape[0] - patchSize//2  
	endIdxY = binMap.shape[1] - patchSize//2  
	endIdxX = binMap.shape[2] - patchSize//2  

	
	for z in range(strtIdx,endIdxZ):
		for y in range(strtIdx,endIdxY):
			for x in range(strtIdx,endIdxX):
				print(str(z) + "," + str(y) + "," + str(x))

				subVolZStart = z - patchSize//2
				subVolZEnd = z + patchSize//2 + 1
				subVolYStart = y - patchSize//2
				subVolYEnd = y + patchSize//2 + 1
				subVolXStart = x - patchSize//2
				subVolXEnd = x + patchSize//2 + 1

				subVolume = binMap[subVolZStart:subVolZEnd, subVolYStart:subVolYEnd, subVolXStart:subVolXEnd]
				porosity = (np.sum(subVolume)/(patchSize**3))*100
				print(np.sum(subVolume))
				print(porosity)
				porosityMap[z,y,x] = int(porosity)

	return porosityMap


ifl	= "/home/eg/Desktop/Adidas-PoreHeatMap/heel-bin-test.tif"
fN 	= "RF-DNA-Heel-small"
pS 	= 50
ofl	= "/home/eg/Desktop/Adidas-PoreHeatMap/heel-porosity-test/"

print("Reading input file")
inputFile = tf.imread(ifl)[0:75,:,:]

print("Computing porosity map")
startTime = time.time()
porosityMap = getPorosityMap(binMap=inputFile,patchSize=pS)
endTime = time.time()
print("\tTime for completion: " + str(np.round( (endTime-startTime)//60 )) + " mins")

print("Saving porosity map")
tf.imwrite( (ofl + fN + "-porosityMap.tif") , porosityMap.astype('uint8'))