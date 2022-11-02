"""
"""



from pac import Measure
from pac import Segment
import numpy as np
import tifffile as tf
from skimage.morphology import skeletonize
import skimage.measure


ofl="/home/eg/Desktop/EG-WateshedAnalysesAvizo/output3/"

inputFile = '/home/eg/Desktop/EG-WateshedAnalysesAvizo/EG-WateshedAnalysesAvizo-ALL.tif'

clm = tf.imread(inputFile)

numPtcl = clm.max()

branchArray = np.zeros((numPtcl,2))

def classifyNodes():
	"""Code used to classify nodes as 
			- end node
			- branch node
	"""

	# For each 


for ptclNo in range(1, numPtcl + 1):
	
	print('Checking particle ' + str(ptclNo) + '/' + str(numPtcl))	

	currFileName = 'MgZnSiScan1-' + str(ptclNo)

	# Extract particle subvolume
	print('\tCropping')
	ptcl = Segment.cropAndPadParticle(labelledMap=clm,
										label=ptclNo,
										pad=5,
										saveData=True,
										fileName= currFileName,
										outputDir=ofl)

	tf.imwrite( (ofl+currFileName+'.tiff'), ptcl.astype('uint8'))

	print('\tMaking Stl')
	Segment._generateInPlaceStlFile( ptcl, 
										stepSize = 1, 
										saveImg=True, 
										sampleName=currFileName, 
										outputDir=ofl)

	# Skeletonize particle subvolume
	print('\tSkeletonizing')
	ptclSkeleton = skeletonize(ptcl)
	ptclSkeleton = ptclSkeleton//ptclSkeleton.max()

	tf.imwrite( (ofl+currFileName+'-skeleton.tiff'), ptclSkeleton.astype('uint8'))


	# Compute EDM of particle subvolume
	print('\tEDMing')
	edmPtcl = Segment.obtainEuclidDistanceMap( binaryMapForEDM=ptcl, 
												scaleUp = int(1), 
												saveImg=False, 
												sampleName=currFileName, 
												outputDir=ofl )

	# Get product of skeleton EDM
	print('\tGetting EDM on skeleton')
	skeletonEDM = ptclSkeleton*edmPtcl

	# Get list of ED along skeleton
	nonZeroEDMVal = (skeletonEDM[np.nonzero(skeletonEDM)]).flatten()
	np.savetxt(ofl+currFileName+'-edmSkeleton.csv', nonZeroEDMVal, delimiter=',')

	# Get number of branches
	print('\tGetting number of branches')
	branchArray[ptclNo-1,0] = ptclNo
	branchArray[ptclNo-1,1] = Segment.getNumberOfBranchesOfSkeleton(ptclSkeleton)
	print('\tPtcl ' + str(ptclNo) + ' has ' + str(branchArray[numPtcl-1,1]) + 'branches')

	# Surface area of particles
	vertices, faces, _, _ = skimage.measure.marching_cubes( volume=ptcl, 
														 level=None, *, 
														 spacing=(1.0, 1.0, 1.0),
														 gradient_direction='descent', 
														 step_size=1, 
														 allow_degenerate=True, 
														 method='lewiner', 
														 mask=None)

	surfArea = skimage.measure.mesh_surface_area(vertices, faces)

	# Volume of particles
	volumeOfPtcl = np.sum(ptcl)

	surfAreaPerVol = surfArea/volumeOfPtcl

	# Classification of nodes

	# Number of segments

	# Length of segments

	# Tortuosity of segments
		# Straight line length vs shortest path

	# Convex hull of particles
		# scipy.spatial.ConvexHull


np.savetxt('MgZnSiScan1-branchNums.csv',branchArray,delimiter=',')