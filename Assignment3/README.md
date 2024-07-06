# Tornado 3D Vector Interpolation
This repository contains code for interpolating 3D vector data from a tornado simulation and generating streamlines based on the interpolated vectors.

# Data Description
The zip file provided here contains a dataset named tornado3d_vector.vti. This dataset represents the vector field data of a simulated tornado in 3D space.

# Usage Instructions
Seed Location Input: Upon running the code, you will be prompted to input the seed location. Please enter the coordinates of the seed point from where you want to start the streamline generation.

# Output: The output of the code will be saved in a file named streamline.vtp. This file contains the generated streamlines based on the input seed location and the interpolated vector field data.

# Code Overview
The code utilizes VTK (Visualization Toolkit) library for reading the input vector field data, interpolating vectors, and generating streamlines using the Runge-Kutta 4th order (RK4) integration method.

# Integration Parameters
Step Size: The step size parameter determines the distance covered in each integration step. It is set to 0.05 by default.
Maximum Steps: The maximum number of integration steps taken to generate the streamline. It is set to 1000 by default.
# How to Run
Ensure that you have VTK library installed in your Python environment. You can install it using pip:

pip install vtk
Then, execute the provided Python script. Upon execution, follow the instructions to input the seed location, and the generated streamline will be saved as streamline.vtp.

For any questions or issues, feel free to reach out.

Note: Ensure that the tornado3d_vector.vti file is in the same directory as the Python script or provide the correct path to the file.