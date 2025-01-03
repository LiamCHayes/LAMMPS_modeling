"""
Functions to initialize bacteria from the numpy data file
"""

import numpy as np
import matplotlib.pyplot as plt


# Calculate the "line" for each bacteria
def bacteria_function(mean_x, mean_y, eigen_bacteria_vector, x_points, y_points, end_points=False):
    """
    Takes the bacteria line parameters and evaluates them to get points to define the bacteria on

    args:
        mean_x (float): average of the x (column) coordinates
        mean_y (float): average of the y (row) coordinates
        bacteria_slope (float): slope of the bacteria
        x_points (numpy array): are the column values of the bacteria
        end_points (bool): True if you only want the end points, False if you want the individual particles of the bacteria

    returns:
        bacteria_x, bacteria_y (numpy arrays): If end_points==False. x and y coordinates for the bacteria line of best fit
        bacteria_start, bacteria_end (numpy arrays): If end_points==True. Coordinates for the start and end of the bacteria
    """
    # Get slope of line
    bacteria_slope = eigen_bacteria_vector[0] / eigen_bacteria_vector[1]

    # Get length of bacteria
    bacteria_length = np.sqrt((np.min(x_points) - np.max(x_points))**2 + (np.min(y_points) - np.max(y_points))**2)
    
    # Change eigenvector to quadrant 1 coordinates instead of numpy coordinates
    neg_y = np.array([1, -1])
    eigen_bacteria_vector_q1 = eigen_bacteria_vector[::-1] * neg_y

    # Get points along the bacteria line, centered at the centroid, of the same length as the bacteriaoid = np.array([mean_x, mean_y])
    bacteria_centroid = np.array([mean_x, mean_y])
    bacteria_start = bacteria_centroid - eigen_bacteria_vector_q1 * bacteria_length / 2
    bacteria_end = bacteria_centroid + eigen_bacteria_vector_q1 * bacteria_length / 2
    
    # Make y coordinate negative so it matches the original
    bacteria_start = bacteria_start * neg_y
    bacteria_end = bacteria_end * neg_y

    # Return end points or dots on the line
    if end_points:
        return bacteria_start, bacteria_end
    else:
        bacteria_x = np.linspace(bacteria_start[0], bacteria_end[0], round(bacteria_length))
        bacteria_y = -bacteria_slope * (bacteria_x - mean_x) + mean_y

        return bacteria_x, -bacteria_y

def get_coords(data, end_points=False):
    """
    Gets the coordinates of each bacteria from an input file
    
    args:
        data (numpy array): Input file of bacteria locations
        end_points (bool): True if we only want the end points, False if we want points in between
        
    returns:
        bacteria_lines (list): A list of coordinates. If end_points is True, each element in the list 
        is a tuple that contains (start_coordinates, end_coordinates). if end_points is False,
        each element in the list is a tuple that contains (x_coordinates, y_coordinates) for a line of 
        points representing the bacteria.
    """
    # Get the numbers assigned to the bacteria
    bacteria_numbers = np.unique(data)
    bacteria_numbers = bacteria_numbers[bacteria_numbers != 0]

    # Loop through the bacteria numbers and get the line of best fit for the bacteria
    bacteria_lines = []
    for num in bacteria_numbers:
        # Center the bacteria coordinates
        bacteria_coords = np.where(data==num)
        mean_row, mean_col = np.mean(bacteria_coords, axis=1)
        bacteria_coords_centered = np.array([
            bacteria_coords[0] - mean_row,
            bacteria_coords[1] - mean_col
        ])

        # Compute the bacteria covariance and get eigenvalues to determine the orientation of the bacteria
        bacteria_covariance = np.cov(bacteria_coords_centered[0], bacteria_coords_centered[1])
        eigen_bacteria = np.linalg.eig(bacteria_covariance)

        # Get the vector that describes the longest axis of the bacteria
        eigen_bacteria_vector = eigen_bacteria.eigenvectors[np.where(eigen_bacteria.eigenvalues == max(eigen_bacteria.eigenvalues))][0]

        bacteria_line = bacteria_function(mean_col, mean_row, eigen_bacteria_vector, bacteria_coords[1], bacteria_coords[0], end_points)
        bacteria_lines.append(bacteria_line)

    return bacteria_lines

def transform_coords(bacteria_start, bacteria_end, x_size, y_size):
    """
    Transforms coords of a single bacteria for lammps to initialize them

    args:
        bacteria_start: The coordiantes of an end point of a bacteria
        bacteria_end: The coordiantes of the other end point of a bacteria
        x_size (int): range of x coordiantes in the data
        y_size (int): range of y coordinates int the data
    """
    # Add z coordinate for lammps
    bacteria_start = np.append(bacteria_start, 0)
    bacteria_end = np.append(bacteria_end, 0)

    # Translate to be centered around 0, 0, 0 
    bacteria_start = bacteria_start + np.array([-x_size/2, y_size/2, 0])
    bacteria_end = bacteria_end + np.array([-x_size/2, y_size/2, 0])

    return bacteria_start, bacteria_end


if __name__ == "__main__":
    # Get data
    data = np.load('./label_fr13.npy')

    # Get bacteria coords
    end_points = True
    bacteria_lines = get_coords(data, end_points)

    #  Plot original
    plt.imshow(data)
    plt.show()

    # Plot points
    for bacteria in bacteria_lines:
        if end_points:
            bx = np.array([bacteria[0][0], bacteria[1][0]])
            by = np.array([bacteria[0][1], bacteria[1][1]])
            plt.plot(bx, by, 'o-')
        else:
            plt.scatter(bacteria[0], bacteria[1])
    ax = plt.gca()
    ax.set_aspect(1)
    plt.show()
