from __future__ import print_function
import numpy as np
import SimpleITK as sitk

'''
Inputs:
    (1) movie = input ITK image
    (2) outputpath = output path
    (3) radius = integer, parameter for Thresholding, which sets the radius of the neighborhood
    (4) threshold = integer, parameter for Thresholding
    (5) stain = numpy array with 4 columns, regions of stains, [xmin, xmax, ymin, ymax]
    
Outputs:
    (1) newMovie = ITK image
    (2) SpermStep3_Thresholding.mha saved in the output path
'''

def Thresholding( movie, outputpath, radius, threshold, stain ):    

    '''
    Initialize a zero-array, then convert the array to an ITK image later.
    '''
    (n1,n2,n3) = movie.GetSize()
    newMovie = np.zeros( (n3,n2,n1) )

    '''
    Get the number of stains, i.e. ns1.
    '''
    ns1,ns2 = stain.shape

    print("  Thresholding ...  ")

    '''
    Do the following thresholding method frame by frame.
    '''
    for k in range(n3):
        A = np.array( sitk.GetArrayFromImage( movie[:,:,k] ) )
        for i in range( 3*radius+1, n2-3*radius ):
            for j in range(3*radius+1,n1-3*radius):
                
                # Compute the average intensity of a square centered at (i,j).
                center = np.mean( A[ i-radius : i+radius+1 , j-radius : j+radius+1 ] )

                # Compute the average intensity of its four neighboring squares.
                neiU = np.mean( A[ i-radius : i+radius+1 , j-3*radius-1 : j-radius ] )
                neiD = np.mean( A[ i-radius : i+radius+1 , j+radius+1 : j+3*radius+2 ] )
                neiL = np.mean( A[ i-3*radius-1 : i-radius , j-radius : j+radius+1 ] )
                neiR = np.mean( A[ i+radius+1 : i+3*radius+2 , j-radius : j+radius+1 ] )

                # Compute the differences.
                dU = np.absolute( neiU - center )
                dD = np.absolute( neiD - center )
                dL = np.absolute( neiL - center )
                dR = np.absolute( neiR - center )
                
                # If at least one difference exceeds the threshold value,
                # then mark the index (i,j).
                if dU > threshold or dD > threshold or dL > threshold or dR > threshold:
                    newMovie[k,i,j] = 1
                ''' end of if loop '''
            ''' end of for loop on j '''
        ''' end of for loop on i '''

        # Remove stains from the thresholding result.
        for i in range(ns1):
            newMovie[k, stain[i,2]:stain[i,3], stain[i,0]:stain[i,1] ].fill(0)
        ''' end of for loop on i '''
    ''' end of for loop on k '''

    '''
    Write out the result.
    '''
    newMovie = sitk.GetImageFromArray(newMovie)
    imwrite = sitk.ImageFileWriter()
    imwrite.SetFileName( outputpath+"SpermStep3_Thresholding.mha" )
    imwrite.Execute( newMovie )

    return newMovie
