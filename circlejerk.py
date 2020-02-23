MIN_DIM = 100
THRESHOLD = 100


from PIL import Image, ImageFilter
import numpy as np
from math import floor, ceil
import os

# Takes in a filename and will identify the images present in the image. Returns numpy array of pixel values.
def get_edges(filename):
    im = Image.open(filename).convert('L')
    
    size = im.size
    # Get a scale factor so the smaller of two dimensions is set to MIN_DIM
    scale = size[0]/MIN_DIM if size[0]/MIN_DIM < size[1]/MIN_DIM else size[1]/MIN_DIM

    # Resize image with scale factor found above
    new_size = (round(size[0]/scale), round(size[1]/scale))
    im = im.resize(new_size)

    # Filter noise
    # im = im.filter(ImageFilter.GaussianBlur(radius=1)) # May want to turn this off
    im = im.filter(ImageFilter.FIND_EDGES)
    
    # Copy image array so modifications can be made
    image = np.asarray(im).copy()
    
    #No image borders should be thought of as edges
    image[0, :] = 0
    image[im.size[1] - 1, :] = 0
    image[:, 0] = 0
    image[:, im.size[0] - 1] = 0
    
    return image

def threshold(image_matrix):
    # WorkingImage is thresholded version of the image array.
    workingImage = image_matrix.copy()
    workingImage = workingImage > THRESHOLD
    # Get rid of points that aren't in threshold
    for row in range(image_matrix.shape[0]):
        for col in range(image_matrix.shape[1]):
            if not workingImage[row][col]:
                image_matrix[row][col] = 0
                
    return image_matrix

def get_coords(image_matrix):
    workingImage = image_matrix.copy()
    workingImage = workingImage > THRESHOLD
    # Coordinates of points being explored
    coords = []
    for row in range(len(workingImage)):
        for col in range(len(workingImage[row])):
            if (workingImage[row][col] and row != 0 and col != 0):
                coords.append((col, row))
                
    return coords

def voting_matrix(image):
    matrix_shape = (image.shape[0], image.shape[1], MIN_DIM//2)
    return np.zeros(matrix_shape, dtype=int, order='C')

def vote(voting_matrix):
    matrix_shape = voting_matrix.shape
    for r in range(matrix_shape[2]): #The r values
        for a,b in coords:
            ymin = b - r if (b-r) > 0 else 0
            ymax = b
            for y in range(ymin, ymax):
                det = (r**2 - (b - y)**2)**(1/2)
                if isinstance(det, complex):
                    continue
                else:
                    x1 = round(a - det)
                    x0 = round(a + det)
                    if x1 < matrix_shape[0] and x1 > 0:
                        voting_matrix[x1, y, r] += 1
                    if x0 < matrix_shape[0] and x0 > 0 and x0 != x1:
                        voting_matrix[x0, y, r] += 1
                        
    return voting_matrix

def get_max_votes(voting_matrix):
    return np.amax(voting_matrix)


# In[633]:


def standardize_votes(voting_matrix, max_votes):
    return counts.copy() / (m/255)
    

def get_max_position(voting_matrix, max_votes):
    return np.where(voting_matrix==max_votes)

def make_output(image_matrix, max_position):
    # Make the output image rgb
    outputImage = np.asarray(Image.fromarray(image_matrix).convert('RGB')).copy()
    
    r = max_position[2][0]
    y0 = max_position[1][0]
    x0 = max_position[0][0]

    xmin = x0 - r
    xmax = x0 + r

    n = np.linspace(xmin,xmax,(xmax-xmin)*10)
    for x in n:
        det = ceil((r**2 - (x - x0)**2)**(1/2))
        y_top = int(y0 + det)
        y_bot = int(y0 - det)
        outputImage[int(round(x)), y_top, 0] = 255
        outputImage[int(round(x)), y_bot, 0] = 255
        det = floor((r**2 - (x - x0)**2)**(1/2))
        y_top = int(y0 + det)
        y_bot = int(y0 - det)
        outputImage[int(round(x)), y_top, 0] = 255
        outputImage[int(round(x)), y_bot, 0] = 255
        
    return Image.fromarray(outputImage)

def generate_animation(standardized_voting_matrix):
    for i in range(standardized_voting_matrix.shape[2]):
        filename = 'frames/frame' + str(i) + '.png'
        Image.fromarray(standardized_voting_matrix[:, :, i]).convert('RGB').save(fp=filename)
        
    
    os.system("ffmpeg -f image2 -r 10 -i ./frames/frame%01d.png -vcodec gif animation2.gif")

def driver(animate):
    image = get_edges('circle1.jpg')
    image = threshold(image)
    coords = get_coords(image)
    counts = voting_matrix(image)
    counts = vote(counts)
    max_votes = get_max_votes(counts)
    c = standardize_votes(counts, max_votes)
    position = get_max_position(counts, max_votes)
    
    if animate:
        generate_animation(c)
        
    return make_output(image, position)

