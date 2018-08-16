from __future__ import print_function
import SimpleITK as sitk

'''
Inputs:
    (1) movie = input ITK image
    (2) outputpath = output path
    (3) medfiltRadius = integer, parameter for MedianImageFilter, which sets the radius of the neighborhood

Outputs:
    (1) newMovie = ITK image
    (2) SpermStep2_Blurring.mha saved in the output path
'''

def Blurring( movie, outputpath, medfiltRadius ):
    
    '''
    Get the size of the movie.
    '''
    (n1,n2,n3) = movie.GetSize()

    '''
    Define a 2D blurring filter.
    '''
    medfilt2 = sitk.MedianImageFilter()
    medfilt2.SetRadius( medfiltRadius )

    print("  Performing median filtering ...  ")

    '''
    Apply median friltering frame by frame.
    '''
    newMovie = sitk.Image(n1,n2,n3, sitk.sitkUInt16)
    for ii in range(n3):
        newImage = medfilt2.Execute( movie[:,:,ii] )
        volume = sitk.JoinSeries(newImage)
        newMovie = sitk.Paste(newMovie, volume, volume.GetSize(), destinationIndex=[0,0,ii])

    '''
    Write out the result.
    '''
    imwrite = sitk.ImageFileWriter()
    imwrite.SetFileName( outputpath+"SpermStep2_Blurring.mha" )
    imwrite.Execute( newMovie )

    return newMovie
