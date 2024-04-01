"""This pipeline is for the analyses of the anduril particles.
"""

import sys
sys.path.insert(0,'/home/crg/Documents/Code/pacMan/')

import tifffile as t
from pac import Segment
from pac import Measure 


sampleName = 'PostAvizo_Sample3_p_h1_rr6'
sampleLoc = '/home/crg/Documents/Datasets/Anduril/PostAvizo/S3-p-crop.tif'
h_val = 1 
rr_val = 0.6

ofl = '/home/crg/Documents/Datasets/Anduril/PostAvizo/output/'
binData = t.imread(sampleLoc)

edm_image = Segment.obtainEuclidDistanceMap(binData)

edm_peaks = Segment.obtainLocalMaximaMarkers(	edm_image, 
												method = 'hlocal' , 
												h=h_val, 
												saveImg=True, 
												sampleName=sampleName, 
												outputDir=ofl )

segmented_image = Segment.segmentUsingWatershed(binaryMapToSeg = binData, 
												edmMapForTopo = edm_image,
												edmPeaksForSeed = edm_peaks, 
												addWatershedLine = False, 
												sampleName = sampleName,
												saveImg = True,
												outputDir = ofl 
												)

corrected_segmented_image = Segment.fixErrorsInSegmentation(labelledMapForOSCorr = segmented_image, 
															pad=2, 
															areaLimit = 700, 
															considerEdgeLabels=True,
															checkForSmallParticles = True, 
															voxelVolumeThreshold=1000,
															radiusCheck=True, 
															radiusRatioLimit=rr_val, 
															sampleName=sampleName, 
															saveImg=True, 
															outputDir=ofl)
