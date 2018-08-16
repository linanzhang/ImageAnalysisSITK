import numpy as np


'''
Inputs:
    A = n*2 numpy array
    outliercriterion = the threshold value which determines outliers
Output:
    C = A - outlier entries
'''

def RemoveOutliers2D(A,outliercriterion):
    # Compute statistics.
    xmu = np.mean( A[:,0] )
    ymu = np.mean( A[:,1] )
    xsd = np.std( A[:,0] )
    ysd = np.std( A[:,1] )

    # Compute the non-outlier region.
    xmin = xmu - xsd * outliercriterion
    xmax = xmu + xsd * outliercriterion
    ymin = ymu - ysd * outliercriterion
    ymax = ymu + ysd * outliercriterion

    # Remove outliers.
    n1,n2 = A.shape
    C = np.zeros( (n1,n2) ).astype('float')
    for i in range(n1):
        if A[i,0]>=xmin and A[i,0]<=xmax and A[i,1]>=ymin and A[i,1]<=ymax :
            C[i,:] = A[i,:]
        else:
            C[i,0] = np.nan
            C[i,1] = np.nan
    ''' end of for loop '''

    # Remove nan entries.
    C = C[~np.isnan(C).any(axis=1)]
    
    return C


'''
Inputs:
    A = n*2 numpy array, (y,x) pairs
        - x is increasing along the 2nd colunm.
        - For fixed x, y is increasing along the 1st column.
    b = boolean
        - b=1: find smallest y for fixed x
        - b=0: find largest y for fixed x
Output:
    C = a simplied n*2 array from A such that the 2nd column is unique
'''

def SimplifyX(A,b):
    # Find the unique elements in the 2nd column.
    xvalues = np.unique( A[:,1] )
    # Initialize C and set the 2nd column.
    n = len( xvalues )
    C = np.zeros((n,2))
    C[:,1] = xvalues

    for ii in range(n):
        # Find indicies (r,1) such that M[r,1] = xvalues[ii].
        row = np.where( A[:,1] == xvalues[ii] )
        # Set the 1st column of C.
        if b == 1:
            C[ii,0] = A[np.amin(row),0]
        elif b == 0:
            C[ii,0] = A[np.amax(row),0]
    return C


'''
Inputs:
    A = n*2 numpy array, (y,x) pairs
        - y is increasing along the 1st colunm.
        - For fixed y, x is increasing along the 2nd column.
    b = boolean
        - b=1: find smallest x for fixed y
        - b=0: find largest x for fixed y
Output:
    C = a simplied n*2 array from A such that the 1st column is unique
'''

def SimplifyY(A,b):
    # Find the unique elements in the 1st column.
    yvalues = np.unique( A[:,0] )
    # Initialize C and set the 1st column.
    n = len( yvalues )
    C = np.zeros((n,2))
    C[:,0] = yvalues

    for ii in range(n):
        # Find indicies (r,0) such that M[r,0] = yvalues[ii].
        row = np.where( A[:,0] == yvalues[ii] )
        # Set the 2nd column of C.
        if b == 1:
            C[ii,1] = A[np.amin(row),1]
        elif b == 0:
            C[ii,1] = A[np.amax(row),1]
    return C


'''
Input:
    lowercurve, uppercurve = two 2-column arrays with almost identical first columns
        The 1st column in each matrix has no repeated elements.
    body = array, which contains both lowercurve and uppercurve
    maxheadwidth = maximum head width
        Set maxheadwidth = 12.
    headbodyratio = smallest (half head length)/(body length) of a segmentation result
        which is considered as a good segmentation
        Set headbodyratio = 1/4.

Outputs:
    goodframe = boolean
        goodframe=1 : the segmentation of this frame is acceptable,
                      resume computaion with the function SeparateHeadTail
        goodframe=0 : the segmentation of this frame is not acceptable,
                      to further computation
'''
def GoodFrameTest(lowercurve,uppercurve,body,maxheadwidth,headbodyratio):
    # Put two curves together.
    head = np.concatenate( (lowercurve, uppercurve), axis=0 )
    # Rearange the rows so that the 1st column (i.e. x values) is increasing.
    head = head[ np.argsort( head[:,0] ) ]
    # Find the unique elements in the 1st column., i.e. find unique x values
    xvalues = np.unique( head[:,0] )
    n = len( xvalues )
    # data is a temporary array that can be used to determine whether a segementation result
    # is good enough to be used in further calculations.
    data = np.zeros((n,2))
    data[:,0] = xvalues

    # Determine the values in the 2nd column.
    for ii in range(n):
        xx = xvalues[ii]
        if np.in1d( xx, lowercurve[:,0] ):
            if np.in1d( xx, uppercurve[:,0] ):
                # If xx is both in lowercurve and upper curve, then find the indices r1, r2 
                # such that lowercurve[r1,0] = xx, uppercurve[r2,0] = xx.
                r1 = np.amin( np.where( lowercurve[:,0]==xx ) )
                r2 = np.amin( np.where( uppercurve[:,0]==xx ) )
                # Compute the difference of the 2nd components.
                d = np.absolute( lowercurve[r1,1] - uppercurve[r2,1] )
                # If d does not exceed maximum head width, then set data[ii,1] equal to d.
                if d <= maxheadwidth:
                    data[ii,1] = d
                ''' end of if ( d <= maxheadwidth ) loop '''
        ''' end of if ( np.in1d( xx, lowercurve[:,0] ) ) loop '''
    ''' end of for loop '''

    # Find the index where the maximum appears.
    p = np.argmax( data[:,1] )
    if float(p-1)/n <= headbodyratio or float(n-p)/n <= headbodyratio:
        # If the segmentation result has a decent head/body ratio,
        # then the frame is considered as a good one.
        goodframe = 1
    else:
        goodframe = 0

    return goodframe, data, head


'''
Input:
    lowercurve, uppercurve = two 2-column arrays with almost identical first columns
        The 1st column in each matrix has no repeated elements.
    body = array, which contains both lowercurve and uppercurve
    data = an intermediate result from the previous step GoodFrameTest
    head = an intermediate result from the previous step GoodFrameTest
    outliercriterion = the threshold value which determines outliers

Outputs:
    head = array, pixels that form the head, (x,y) pairs
    tail = array, pixels that form the flagellum in full width, (x,y) pairs
    ori = boolean
        ori=0 : the head points toward a smaller independent variable e.g. leftward or downward
        ori=1 : the head points toward a greater independent variable e.g. rightward or upward
'''

def SeparateHeadTail(lowercurve,uppercurve,body,data,head,outliercriterion):
    # Separate head and tail.
    p = np.argmax(data[:,1])
    n,n2 = data.shape
    if n-p>=p-1:
        # p is in the 1st half.
        ori = 1
        x = data[2*p-1,0]
        # Remove the elements in head which is bigger than or equal to x.
        r = np.where( head[:,0]==x )
        head = head[0:np.amin(r),:]
        # Remove the elements in head which is less than x.
        if np.in1d( x, lowercurve[:,0] ):
            r = np.where( lowercurve[:,0]==x )
            tail = lowercurve[np.amin(r):,:] 
        else:
            r = np.where( uppercurve[:,0]==x ) 
            tail = uppercurve[np.amin(r):,:]  
    else:
        # p is in the 2nd half.
        ori = 0
        x = data[2*p-n,0]
        # Remove the elements in head which is bigger than or equal to x
        r = np.where( head[:,0]==x )
        head = head[np.amin(r):,:] 
        # Remove the elements in head which is less than x.
        if np.in1d( x, lowercurve[:,0] ):
            r = np.where( lowercurve[:,0]==x )
            tail = lowercurve[0:np.amin(r),:] 
        else:
            r = np.where( uppercurve[:,0]==x )
            tail = uppercurve[0:np.amin(r),:]

    # Determine the outliers in head and move them to the tail.
    m1,m2 = head.shape
    xmin = np.mean(head[:,0]) - outliercriterion
    xmax = np.mean(head[:,0]) + outliercriterion
    ymin = np.mean(head[:,1]) - outliercriterion
    ymax = np.mean(head[:,1]) + outliercriterion
    for ii in range(m1):
        if head[ii,0]<=xmin or head[ii,0]>=xmax or head[ii,1]<=ymin or head[ii,1]>=ymax:
            tail = np.concatenate( (tail, head[ii,:]), axis=0 )
            head[ii,:] = np.array([0,0])
    head[~np.all(head == 0, axis=1)]

    return head, tail, ori

