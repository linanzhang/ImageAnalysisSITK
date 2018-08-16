from __future__ import print_function
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt

''' 
Inputs:
    (1) movie = input ITK image
    (2) outputpath = output path
    (3) sperm = a dictionary which contains some numerics regarding to the segmentation result
    
Outputs:
    (1) SpermStep5_HeadFlagellum.mha saved in the output path
    (2) SpermStep5_HeadTrajectory.png saved in the output path
'''

def Summary( movie, outputpath, sperm ):

    '''
    Initialize two zero-arrays, then convert the array to an ITK image later.
    '''
    (n1,n2,n3) = movie.GetSize()
    newMovie = np.zeros( (n3,n2,n1) )
    headTrajectory = np.zeros( (n2,n1) )
    
    '''
    Get information in sperm.
    '''
    Flagellum = sperm["flagellum"]
    Frame = sperm["frames"]
    Head = sperm["head"]

    print("  Summarizing ...  ")

    '''
    For each frame, plot the head and the flagellum separately.
    '''
    newMovie = np.zeros( (n3,n2,n1) )
    for k in range(n3):
        if k in Frame:
            # Loop in head.
            head = Head[k].astype(int)
            nh1,nh2 = head.shape
            for ii in range(nh1):
                newMovie[k, head[ii,0], head[ii,1] ] = 1
            # Loop in flagellum.
            flagellum = Flagellum[k].astype(int)
            nf1,nf2 = flagellum.shape
            for jj in range(nf1):
                newMovie[k, flagellum[jj,0], flagellum[jj,1] ] = 0.5
        ''' end of if ( k in Frame ) loop on '''
    ''' end of for loop on k '''
    
    '''
    Write out the result.
    '''
    newMovie = sitk.GetImageFromArray(newMovie)
    imwrite = sitk.ImageFileWriter()
    imwrite.SetFileName( outputpath+"SpermStep5_HeadFlagellum.mha" )
    imwrite.Execute( newMovie )

    # Note: Movie SpermStep5_HeadFlagellum.mha is not very clear to see.
    #       To know how accurate the separation result is,
    #       please read the documentation Step05_Summary.pdf.

    '''
    Plot the center of the head in all frames into one figure.
    '''
    # Initialize the center of the head.
    x = []
    y = []
    for k in range(n3):
        if k in Frame:
            head = Head[k].astype(int)
            # Compute the center of the head.
            y.append( np.mean(head[:,0]) )
            x.append( np.mean(head[:,1]) )
    # Write out the result.
    plt.figure()
    plt.plot(x[0], y[0], "r*", label="initial")
    plt.plot(x, y, "b-", label="trajectory")
    x1,x2,y1,y2 = plt.axis()
    plt.axis((0,n2,0,n1))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)
    plt.title("Head Trajectory")
    plt.savefig( outputpath+"SpermStep5_HeadTrajectory.png" )

    return
