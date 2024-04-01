"""This pipeline is for the analyses of segmented anduril particles.
"""

import sys
sys.path.insert(0,'/home/crg/Documents/Code/pacMan/')

import tifffile as t
from pac import Segment
from pac import Measure 


sampleName = [	'PostAvizo_Sample1_p_h1_rr6-correctedLabelMap.tif',
				'PostAvizo_Sample1_v_h3_rr5-correctedLabelMap.tif',
				'PostAvizo_Sample2_p_h1_rr6-correctedLabelMap.tif',
				'PostAvizo_Sample2_v_h3_rr5-correctedLabelMap.tif',
				'PostAvizo_Sample3_p_h1_rr6-correctedLabelMap.tif',
				'PostAvizo_Sample3_v_h3_rr5-correctedLabelMap.tif',
				]

ifl = '/home/crg/Documents/Datasets/Anduril/PostAvizo/output/'
ofl = '/home/crg/Documents/Datasets/Anduril/PostAvizo/output/'

for sample in sampleName:
	sampleLoc = ifl + sample
	clmData = t.imread(sampleLoc)

	#Remove edge labels
	cleanCLMData = Segment.removeEdgeLabels(labelledMapForEdgeLabelRemoval = clmData, 
											pad=0, 
											sampleName=sample.split(".")[0], 
											saveImg=True, 
											outputDir=ofl )

	#Compute and save size
	psArray = Measure.getParticleSizeArray( labelledMapForParticleSizeAnalysis = cleanCLMData, 
											calibrationFactor=1,
											getCaDia=True,
											getFeretDia=False,
											saveData=True, 
											sampleName=sample.split(".")[0], 
											outputDir=ofl)