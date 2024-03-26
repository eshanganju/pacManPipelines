"""This pipeline is for the analyses of the anduril particles.
"""

import sys
sys.path.insert(0,'/home/crg/Documents/Code/pacMan/')

import tifffile as t
from pac import Segment
from pac import Measure 


ofl = '/home/crg/Documents/Datasets/Anduril/output/'
sampleName = 'Sample3-Test_06'
sampleLoc = '/home/crg/Documents/Datasets/Anduril/Sample3/Scan3-Clean-1-Bin-Test.tif'

binData = t.imread(sampleLoc)

edm_image = Segment.obtainEuclidDistanceMap(binData)

edm_peaks = Segment.obtainLocalMaximaMarkers(edm_image)

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
															radiusRatioLimit=0.6, 
															sampleName=sampleName, 
															saveImg=True, 
															outputDir=ofl)
