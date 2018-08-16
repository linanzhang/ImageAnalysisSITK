from __future__ import print_function
import SimpleITK as sitk

'''
Inputs:
    (1) movie = input ITK image
    (2) outputpath = output path

Outputs:
    (1) newMovie = ITK image
    (2) SpermStep1_CorrectingIllumination.mha saved in the output path
'''

def PreProcessing( movie, outputpath ):

    '''
    Get the size of the movie.
    '''
    n1,n2,n3 = movie.GetSize()

    '''
    Rescale intensity values of the image.
    Note: RescaleIntensityImageFilter does not change pixel type.
    '''
    imadjust = sitk.RescaleIntensityImageFilter()
    imadjust.SetOutputMinimum( 0 )
    imadjust.SetOutputMaximum( 255 )
    movie = imadjust.Execute( movie )   

    '''
    Define erosion and dilation filters.
    '''
    radius = (n1/16,n2/16)
    # Define grayscale erosion.
    imerode = sitk.GrayscaleErodeImageFilter()
    imerode.SetKernelType( sitk.sitkBall )
    imerode.SetKernelRadius( radius )
    # Define grayscale dilation.
    imdilate = sitk.GrayscaleDilateImageFilter()
    imdilate.SetKernelType( sitk.sitkBall )
    imdilate.SetKernelRadius( radius )

    print("  Correcting nonuniform illumination ...  ")

    '''
    Apply grayscale opening to correct nonuniform illumination frame by frame.
    '''
    newMovie = sitk.Image(n1,n2,n3, sitk.sitkUInt16)
    for ii in range(n3):
        newImage = movie[:,:,ii] - imdilate.Execute( imerode.Execute( movie[:,:,ii]) )
        volume = sitk.JoinSeries(newImage)
        newMovie = sitk.Paste(newMovie, volume, volume.GetSize(), destinationIndex=[0,0,ii])

    '''
    Write out the result.
    '''
    imwrite = sitk.ImageFileWriter()
    imwrite.SetFileName( outputpath+"SpermStep1_CorrectingIllumination.mha" )
    imwrite.Execute( newMovie )

    return newMovie
