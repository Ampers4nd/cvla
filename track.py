__author__ = 'john'


from scipy import ndimage
import numpy as np
from scipy import ndimage
from PIL import Image


def display(im, title2):
    # assume input image is floating point data,
    # and values are not normalized
    #
    # would it be better to take the abs(im)
    # instead of lifting the values?
    #
    immax = im.max()
    immin = im.min()

    im_norm = (im - immin) / (immax - immin)
    im_display = Image.fromarray( (im_norm * 255.0).astype(np.uint8) );
    im_display.show(title=title2)


def make_covariance(ix, iy):
    # there is an error here!
    A = np.matrix( [[ix*ix, ix*iy], [iy*ix, iy*iy]])
    return A


def calculate_score(Ix, Iy):
    # M = [ [a,b], [c,d] ]
    # tr(M) = a*d
    # det( a*d - b*c )
    #
    # A = [ [Ix*Ix, Ix*Iy], [Iy*Ix, Iy*Iy] ]
    # tr(A) = Ix*Ix * Iy*Iy
    # det(A) = Ix*Ix * Iy*Iy  -  Ix*Iy * Iy*Ix
    #
    # score = det(A) / (tr(A)+eps)
    Ixx = Ix*Ix
    Iyy = Iy*Iy
    IxxIyy = Ixx * Iyy
    Ixy = Ix*Iy
    IxyIxy = Ixy*Ixy
    traA = IxxIyy
    detA = IxxIyy - IxyIxy
    eps = np.array( [0.1], dtype=np.float32 )
    Iscore = detA / (traA+eps)
    return Iscore


def detect_features(filename):
    im = ndimage.imread(filename, flatten=True).astype(np.float32)

    kernel = np.array( [-1, 1], np.float32 ) # choosing floating point type
    Ix = ndimage.convolve1d(im, kernel, axis=0, mode='constant', cval=0.0)
    Iy = ndimage.convolve1d(im, kernel, axis=1, mode='constant', cval=0.0)

    display(Ix, 'Ix')
    display(Iy, 'Iy')

    # need to fix this function!
    #A = make_covariance(Ix,Iy)
    Iscore = calculate_score(Ix, Iy)
    display(Iscore, 'score')
    return Iscore


def main():
    Ifeature = detect_features('testFeatures2.jpg')

if __name__ == '__main__':
    main()
