from __future__ import print_function
import numpy as np
import SimpleITK as sitk

from Step4Helpers import *

''' 
Inputs:
    (1) movie = input ITK image
    (2) outputpath = output path
    (3) dt = time elapsed between two consecutive frames
    (4) scale = nm/pixel
    (5) threshold1 = integer, the threshold value which determines outliers in the body
    (6) maxheadwidth = integer, the maximum width (in pixels) of the head
    (7) headbodyratio = float, if the ratio of head length to body length exceeds
            2*headbodyratio, the frame is considered as a valid frame; if not, 
            no further calculations using the information of this frame.
    (8) threshold2 = integer, the threshold value which determines outliers in the head
    
Outputs:
    (1) newMovie = ITK image
    (2) sperm = a dictionary which contains some numerics regarding to the segmentation result
    (3) SpermStep4_GoodFramesOnly.mha saved in the output path
'''

def DetectingSpermBody( movie, outputpath, dt, scale,
                        threshold1, maxheadwidth, headbodyratio, threshold2 ):

    '''
    Convert the ITK image to a numpy array.
    '''
    (n1,n2,n3) = movie.GetSize()
    movie = np.array( sitk.GetArrayFromImage( movie ) )

    '''
    Initialize some features that characterize sperm motility.
    '''
    Body = []
    Flagellum = []
    Frame = []
    Head = []
    Horizontality = []

    print("  Sperating head and flagellum ...  ")

    '''
    Analyze sperm motility frame by frame.
    '''
    for k in range(n3):
        A = movie[k,:,:]

        '''
        Step 4.1 Remove outliers.
            - pixels_raw = 2-column np.array in (y,x) pairs
            - body = 2-column np.array in (y,x) pairs
        '''
        # Find the indicies (i,j) such that A[i,j] = 1.
        row,col = np.where( A == 1 )
        # pixels_raw = list of (i,j) such that A[i,j] = 1.
        pixels_raw = np.array([row,col]).transpose()
        # body = pixels_raw - outliers
        body = RemoveOutliers2D( pixels_raw, threshold1 )
        # Count the unique values in x-axis and y-axis, respectively.
        xnum = len( np.unique( body[:,1] ) )
        ynum = len( np.unique( body[:,0] ) )
        
        '''
        Step 4.2 Determine horizontality.
            - lowercurve = 2-column np.array in (y,x) pairs
            - uppercurve = 2-column np.array in (y,x) pairs
        '''
        if xnum>=ynum:
            # The sperm is swimming horizontally.
            horizontality = 1
            # Sort the array such that the 2nd column is ascending.
            body = body[ np.argsort( body[:, 1] ) ]
            # Compute the lower and upper curves.
            lowercurve = SimplifyX(body,1)
            uppercurve = SimplifyX(body,0)
        else:
            # The sperm is swimming vertically.
            horizontality = 0
            # Sort the array such that the 1st column is ascending.
            body = body[ np.argsort( body[:, 0] ) ]
            # Compute the lower and upper curves.
            lowercurve = SimplifyY(body,1)
            uppercurve = SimplifyY(body,0)
        ''' end of if ( xnum >= ynum ) loop '''
        
        '''
        Step 4.3 Determine whether this frame is a good frame.
            - goodframe = boolean
            - data, head = 2-column np.array in (x,y) pairs if xnum>=ynum,
                            in (y,x) pairs if xnum<ynum
        '''
        # Check whether a decent portion of the flagellum has been segmented.
        # That is, length(head)/length(body) can not exceed headbodyratio.
        if xnum>=ynum:
            # Make (x,y) pairs.
            lowercurve1 = np.fliplr(lowercurve)
            uppercurve1 = np.fliplr(uppercurve)
            body1 = np.fliplr(body)
            goodframe, data, head = GoodFrameTest(lowercurve1,uppercurve1,body1,
                                                  maxheadwidth,headbodyratio)
        else:
            lowcurve = np.fliplr(lowercurve)
            uppcurve = np.fliplr(uppercurve)
            goodframe, data, head = GoodFrameTest(lowercurve,uppercurve,body,
                                                  maxheadwidth,headbodyratio)
        ''' end of if ( xnum >= ynum ) loop '''
        
        '''
        Step 4.4 Separate body into head and flagellum.
            - head = 2-column np.array in (y,x) pairs
            - flagellum = 2-column np.array in (y,x) pairs
        '''
        # If length(head)/length(body) < headbodyratio, do further calculations.
        # Otherwise, go to ii = ii+1.
        if goodframe:
            if xnum>=ynum:
                head1, flagellum1, orientation = SeparateHeadTail(lowercurve1,uppercurve1,
                                                     body1,data,head,threshold2)
                # Make (y,x) pairs.
                head = np.fliplr(head1)
                flagellum = np.fliplr(flagellum1)
            else:
                head, flagellum, orientation = SeparateHeadTail(lowercurve,uppercurve,
                                                   body,data,head,threshold2)
            ''' end of if ( xnum >= ynum ) loop '''

            '''
            Step 4.5 Put the results together.
            '''
            Body.append( body )
            Flagellum.append( flagellum )
            Frame.append( k )
            Head.append( head )
            Horizontality.append( (horizontality,orientation) )

        else:
            Body.append( 'empty' )
            Flagellum.append( 'empty' )
            Head.append( 'empty' )
            Horizontality.append( 'empty' )
            # Erase the information about "bad" frames.
            movie[k,:,:] = np.zeros( (n2,n1) )
        ''' end of if ( goodframe ) loop '''            
    ''' end of for loop on k '''

    '''
    Step 4.5 Put the results together (continued).
    '''
    sperm = {}
    sperm["body"] = Body
    sperm["deltaT"] = dt
    sperm["flagellum"] = Flagellum
    sperm["frames"] = Frame
    sperm["head"] = Head
    sperm["horizontality"] = Horizontality
    sperm["scale"] = scale
    sperm["size"] = (n1,n2)

    '''
    Step 4.6 Write out the result.
    '''
    newMovie = sitk.GetImageFromArray(movie)
    imwrite = sitk.ImageFileWriter()
    imwrite.SetFileName( outputpath+"SpermStep4_GoodFramesOnly.mha" )
    imwrite.Execute( newMovie )

    return newMovie, sperm
