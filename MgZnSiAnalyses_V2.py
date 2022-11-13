"""
"""
from pac import Measure
from pac import Segment
import numpy as np
import tifffile as tf
from skimage.morphology import skeletonize
import skimage.measure
from scipy.spatial import ConvexHull

VERBOSE = True

ofl="/home/eg/Desktop/EG-WateshedAnalysesAvizo/output3/"

inputFile = '/home/eg/Desktop/EG-WateshedAnalysesAvizo/EG-WateshedAnalysesAvizo-ALL.tif'

clm = tf.imread(inputFile)

numPtcl = clm.max()Segment.obtainEuclidDistanceMap

particleData = np.zeros((numPtcl,6)) 	#Index, Volume, Surface area, NumBranches, Hull area, Hull Volume


def classifyNodes(particleMap):
	"""Code used to classify nodes as 
			- end node
			- branch node
	"""
	Print('Under construction')

	return nodeClassifiedMap

def numberOfSegments():
	"""
	"""
	Print('Under construction')


def lengthOfSegment():
	"""
	"""
	Print('Under construction')


def tortuosityOfSegment():
	"""
	"""
	Print('Under construction')



def convexHullDataOfParticle(particleMap):
	"""Get convex hull of the particle
	"""
	particleMap = particleMap//particleMap.max()
	particleData = np.transpose(np.where(particleMap==1))
	
	particleHull = ConvexHull(particleData)

	volume = particleHull.volume
	area = particleHull.area

	return area, volume



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

	# Generate STL
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

	# Getting particle volume
	print('\tGetting particle volume')
	particleData[ptclNo-1,0] = ptclNo
	particleData[ptclNo-1,1] = np.sum(ptcl)
	print('\t\tVolumee:', str(particleData[ptclNo-1,1]))

	# Surface area of particles
	print('\tGetting surface area of particle')
	vertices, faces, _, _ = skimage.measure.marching_cubes(volume=ptcl, 
														 		level=None, 
														 		spacing=(1.0, 1.0, 1.0),
																gradient_direction='descent', 
																step_size=1, 
																allow_degenerate=True, 
																method='lewiner', 
																mask=None)
	particleData[ptclNo-1,2]= skimage.measure.mesh_surface_area(vertices, faces)
	
	# Get number of branches
	print('\tGetting number of branches')
	particleData[ptclNo-1,3] = Segment.getNumberOfBranchesOfSkeleton(ptclSkeleton)
	print('\tPtcl ' + str(ptclNo) + ' has ' + str(particleData[numPtcl-1,3]) + 'branches')


	# Hull Data
	#if particleData[ptclNo-1,3] !=0 :
	print('\tGetting hull data')
	hullArea, hullVolume = convexHullDataOfParticle(ptcl)
	particleData[ptclNo-1,4] = hullArea
	particleData[ptclNo-1,5] = hullVolume


np.savetxt('MgZnSiScan1-Data.csv',particleData,delimiter=',')