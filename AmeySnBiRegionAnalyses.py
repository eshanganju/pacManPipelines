"""Basic script for the analyses of regions in Amey's samples for "regions"
"""

import numpy as np
import tifffile as tf

# Limits
solidLimit = 8
voidLimit = 8

# Read EDMs, and corrected label maps
solidLabelMap = tf.imread('/home/eg/Desktop/Amey-SnBi/regionsAnalyses/SolderRegion_001_Crop-Bin-Clean-Lite-dist-watershed.tif').astype('uint32')
voidLabelMap = tf.imread('/home/eg/Desktop/Amey-SnBi/regionsAnalyses/SolderRegion_001_Crop-Bin-Clean-Dark-dist-watershed.tif').astype('uint32')

solidEDM = tf.imread('/home/eg/Desktop/Amey-SnBi/regionsAnalyses/SolderRegion_001_Crop-Bin-Clean-Lite-dist.tif')
voidEDM = tf.imread('/home/eg/Desktop/Amey-SnBi/regionsAnalyses/SolderRegion_001_Crop-Bin-Clean-Dark-dist.tif')

ofl="/home/eg/Desktop/Amey-SnBi/regionsAnalyses/output/"

# Create LOF maps
lofVoid = np.zeros_like(voidLabelMap)
lofSolid = np.zeros_like(solidLabelMap)

# Analyzed label size for each void label
for voidLabel in range(1, voidLabelMap.max()+1):
	print("VOID")
	print('\tChecking void ' + str(voidLabel) + '/' +  str(voidLabelMap.max()))
	maxInscSph = voidEDM[np.where(voidLabelMap == voidLabel)].max()
	
	if maxInscSph <= voidLimit:
		lofVoid[np.where(voidLabelMap == voidLabel)] = 1

tf.imwrite( (ofl+'lof-void_' + str(voidLimit) + '.tif'), lofVoid)


# Analyzed label size for each solid label
for solidLabel in range(1, solidLabelMap.max()+1):
	print("SOLID")
	print('\tChecking solid ' + str(solidLabel) + '/' +  str(solidLabelMap.max()))
	maxInscSph = solidEDM[np.where(solidLabelMap == solidLabel)].max()
	
	if maxInscSph <= solidLimit:
		lofSolid[np.where(solidLabelMap == solidLabel)] = 1

tf.imwrite( (ofl+'lof-solid_' + str(solidLimit) + '.tif'), lofSolid)

combinedMap = lofVoid +  lofSolid
if combinedMap.max() > 1:
	print('Overlap')
	combinedMap[np.where(combinedMap>1)]=1

tf.imwrite((ofl+'lof-solid_' + str(solidLimit) +'-void_' + str(voidLimit) + '.tif'), combinedMap)