"""This pipeline is for the analyses of the anduril particles.
"""

import tifffile as t
from pac import Filter
from pac import Segment
from pac import Measure 


binDataName = "/home/crg/Documents/Datasets/Anduril/Sample1/Sample1_Bin-Closed.tif"

edm_image = Segment.obtainEuclidDistanceMap()
edm_peaks = Segment.obtainLocalMaximaMarkers()
segmented_image = Segment.segmentUsingWatershed(	binaryMapToSeg = binDataName,
							
							
						)
corrected_segmented_image = Segment.fixErrorsInSegmentation()


