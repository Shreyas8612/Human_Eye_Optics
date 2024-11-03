# __Human Eye Refraction Model with Enhanced Light Rays__

This project simulates the refraction of light through the human eye using Python. It models the eye's optical components—such as the cornea, lens, and retina—and traces light rays from an object through these components to visualize how images are formed on the retina.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Functions Explained](#functions-explained)
- [Acknowledgements](#acknowledgements)

## Overview

The simulation uses geometric optics principles, particularly __Snell's Law__, to model how light refracts when passing through different media in the eye. The program:

- Creates mathematical representations of the cornea, lens, and retina.
- Plots these components to visualize the eye.
- Traces multiple colored light rays from an object through the eye.
- Shows how these rays converge (or not) on the retina.

## Features

- **Eye Model Visualization**: Plots the anatomical structures of the eye.
- **Light Ray Tracing**: Simulates the path of light rays through the eye.
- **Interactive Visualization**: Generates a graphical representation using Matplotlib.
- **Customizable Parameters**: Eye dimensions and refractive indices can be adjusted.

## Requirements

- Python 3.6 or higher
- Libraries:
  - `numpy`
  - `scipy`
  - `matplotlib`

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/eye-refraction-model.git
   cd eye-refraction-model
   ```

2. **Create a Virtual Environment (Optional)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```

3. **Install Dependencies**

   ```bash
   pip install numpy scipy matplotlib
   ```

## Usage

1. **Ensure Both Scripts Are in the Same Directory**

   - `main.py`: The main script that runs the simulation.
   - `My_Functions.py`: Contains all the helper functions used by the main script.

2. **Run the Simulation**

   ```bash
   python main.py
   ```

3. **View the Output**

   - A Matplotlib window will open displaying the eye model and the traced light rays.
   - Close the window to end the program.

## Project Structure

- **`main.py`**: The main script that sets up the simulation and plots the results.
- **`My_Functions.py`**: Contains all the functions for calculations and plotting.

## Functions Explained

### In `My_Functions.py`

- **`snell(n1, n2, theta1)`**
  - Applies Snell's Law to calculate the refracted angle when light passes between two media.
  - __Parameters__:
    - `n1`: Refractive index of the first medium.
    - `n2`: Refractive index of the second medium.
    - `theta1`: Incident angle (in radians).
  - __Returns__: Refracted angle `theta2` (in radians).

- **`create_surface(r, offset=0.0)`**
  - Creates a function representing a circular surface (e.g., cornea, lens surfaces).
  - __Parameters__:
    - `r`: Radius of the circle.
    - `offset`: Horizontal shift of the circle.
  - __Returns__: A function `surface(y)` that calculates `x` for a given `y`.

- **`create_derivative(r)`**
  - Creates a function for the derivative (slope) of the circular surface.
  - __Parameters__:
    - `r`: Radius of the circle.
  - __Returns__: A function `derivative(y)` that calculates the slope at point `y`.

- **`refract_ray(x0, y0, theta, n1, n2, surface, derivative)`**
  - Calculates the new position and angle of a ray after refraction at a surface.
  - __Parameters__:
    - `x0`, `y0`: Starting coordinates of the ray.
    - `theta`: Incident angle.
    - `n1`, `n2`: Refractive indices before and after the surface.
    - `surface`: Function representing the surface.
    - `derivative`: Function representing the slope of the surface.
  - __Returns__: New coordinates `(x, y)` and angle `theta_new`.

- **`trace_ray(start_x, start_y, surfaces, derivatives, n_indices, pupil_lines)`**
  - Traces a ray through all optical components of the eye.
  - __Parameters__:
    - `start_x`, `start_y`: Starting coordinates of the ray.
    - `surfaces`: List of surface functions.
    - `derivatives`: List of derivative functions.
    - `n_indices`: List of refractive indices for each medium.
    - `pupil_lines`: Coordinates representing the pupil for intersection checks.
  - __Returns__: A list `path` of coordinates that the ray follows.

- **`create_eye_model()`**
  - Sets up the eye model by defining surfaces, derivatives, and refractive indices.
  - __Returns__: `surfaces`, `derivatives`, `n_indices`, `eye_length`, `eye_radius`.

- **`plot_eye_model(surfaces, eye_length, eye_radius)`**
  - Plots the eye's anatomical structures.
  - __Parameters__:
    - `surfaces`: List of surface functions.
    - `eye_length`: Total length of the eye model.
    - `eye_radius`: Radius for plotting limits.

- **`plot_colored_dots(x_position)`**
  - Plots the object points (colored dots) from which rays will be traced.
  - __Parameters__:
    - `x_position`: Horizontal position of the dots.

- **`plot_pupil_lines()`**
  - Plots lines representing the pupil and returns their positions for intersection checks.
  - __Returns__: `pupil_lines`, a list of tuples with pupil line coordinates.

### In `main.py`

- **`main()`**
  - The main function that orchestrates the simulation.
  - __Steps__:
    1. Creates the eye model.
    2. Plots the eye structures.
    3. Plots the object points.
    4. Plots the pupil.
    5. Traces rays from each object point through the eye.
    6. Displays the final plot.

## Acknowledgements

This project is inspired by optical models of the human eye and utilizes fundamental principles of geometric optics.

---

Feel free to customize the parameters in `My_Functions.py` to simulate different eye conditions or to enhance the model further.

