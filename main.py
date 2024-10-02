# Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# Snell's Law: n1 * sin(theta1) = n2 * sin(theta2)
# Refracts a ray from medium 1 to medium 2 towards the normal if n2 > n1
# Returns the angle theta2 after refraction
def snell(n1, n2, theta1):
    sin_theta2 = (n1 * np.sin(theta1))/ n2
    # Ensure the value is within the valid domain of sine
    sin_theta2 = np.clip(sin_theta2, -1, 1)
    return np.arcsin(sin_theta2)


# Equation of a circle: x^2 + y^2 = r^2
# Returns the surface of a circle with radius r and offset to shift in the x-direction
# If the y-coordinate is outside the circle, return NaN
# Adding r to the surface ensures the circle is centered at (r, 0)
def create_surface(r, offset=0.0):  # Used to create the surfaces of the cornea and lens
    def surface(y):
        if abs(y) > r:
            return np.nan
        return -np.sqrt(r ** 2 - y ** 2) + r + offset

    return surface


# Equation of a circle: x^2 + y^2 = r^2
# Returns the surface of a circle with radius r and offset to shift in the x-direction
# If the y-coordinate is outside the circle, return NaN
# Adding r to the surface ensures the circle is centered at (r, 0)
def create_surface_inv(r, offset=0.0):  # Used to create the surfaces of the cornea and lens
    def surface(y):
        if abs(y) > r:
            return np.nan
        return np.sqrt(r ** 2 - y ** 2) + r - offset

    return surface


# Equation of the derivative of a circle: dy/dx = y / sqrt(r^2 - y^2)
# Returns the derivative or slope of the surface of a circle with radius r
# If the y-coordinate is outside the circle, return NaN
# Adding 1e-10 to the denominator ensures when y = r, the derivative is not infinite (divide by zero)
def create_derivative(r):
    def derivative(y):
        if abs(y) > r:
            return np.nan
        return y / np.sqrt(r ** 2 - y ** 2 + 1e-10)

    return derivative


# Equation of the derivative of a circle: dy/dx = y / sqrt(r^2 - y^2)
# Returns the derivative or slope of the surface of a circle with radius r
# If the y-coordinate is outside the circle, return NaN
# Adding 1e-10 to the denominator ensures when y = r, the derivative is not infinite (divide by zero)
def create_derivative_inv(r):
    def derivative(y):
        if abs(y) > r:
            return np.nan
        return -y / np.sqrt(r ** 2 - y ** 2 + 1e-10)

    return derivative

# Refracts a ray from (x0, y0) with angle theta through a surface defined by the function surface(y)
# The surface is defined by the function surface(y) and its derivative derivative(y)
# The ray is refracted from medium n1 to medium n2
# Returns the new position (x, y) and angle theta after refraction
def refract_ray(x0, y0, theta, n1, n2, surface, derivative):
    # Define the function whose root we want to find
    def func(y):
        x_surface = surface(y)
        if np.isnan(x_surface):
            return np.nan
        return y0 + (x_surface - x0) * np.tan(theta) - y  # Difference between ray y and surface y

    # Initial guess for y is current y0
    y_guess = y0

    # Use a root-finding method to find the intersection y
    try:
        y_intersect = optimize.newton(func, y_guess)
    except (RuntimeError, ValueError):
        # If the solver fails, return current position and angle
        return x0, y0, theta

    # Now compute x_intersect
    x_intersect = surface(y_intersect)

    # Calculate the normal angle at the point of intersection
    normal_angle = np.arctan(derivative(y_intersect))

    # Calculate the incident angle
    theta1 = theta - normal_angle

    # Calculate the refracted angle using Snell's Law
    theta2 = snell(n1, n2, theta1)
    if np.isnan(theta2):
        return x_intersect, y_intersect, theta

    # Update the ray angle
    theta_new = theta2 + normal_angle
    return x_intersect, y_intersect, theta_new


# Traces a ray from the object at position x,y through all surfaces
# Returns the path of the ray as a list of (x, y) coordinates
# If the ray does not intersect with a surface, return the path up to that point
def trace_ray(start_x, start_y, surfaces, derivatives, n_indices, pupil_lines):
    x, y, theta = start_x, start_y, 0
    path = [(x, y)]
    for i, (surface, derivative) in enumerate(zip(surfaces, derivatives)):
        x, y, theta = refract_ray(x, y, theta, n_indices[i], n_indices[i + 1], surface, derivative)

        # Check if the ray intersects with the pupil_lines
        for line_x, line_y_min, line_y_max in pupil_lines:
            if x >= line_x and line_y_min <= y <= line_y_max:
                return path

        if np.isnan(x) or np.isnan(y):
            break
        path.append((x, y))
    return path


# Creates the eye model with the surfaces, derivatives, refractive indices, eye length, and eye radius
# Returns the surfaces, derivatives, refractive indices, eye length, and eye radius
def create_eye_model():
    # Updated parameters for the eye
    cornea_front_radius = 7.259
    cornea_back_radius = 5.585
    lens_front_radius = 8.672
    lens_back_radius = 6.328
    cornea_thickness = 0.449
    cornea_to_lens = 2.794
    eye_length = 24.0
    eye_radius = 12.0

    cornea_front = create_surface(cornea_front_radius, 5)
    cornea_back = create_surface(cornea_back_radius, cornea_thickness + 5)
    lens_front = create_surface(lens_front_radius, cornea_thickness + cornea_to_lens + 5)
    lens_back = create_surface_inv(lens_back_radius, -0.566)
    retina = create_surface_inv(eye_radius, -5)

    surfaces = [cornea_front, cornea_back, lens_front, lens_back, retina]

    # Create derivatives
    derivatives = [create_derivative_inv(cornea_front_radius),
                   create_derivative_inv(cornea_back_radius),
                   create_derivative_inv(lens_front_radius),
                   create_derivative(lens_back_radius),
                   create_derivative(eye_radius)]

    # Refractive indices for different parts of the eye
    n_indices = [1.0, 1.376, 1.336, 1.406, 1.337, 1.0] # Air, Cornea, Aqueous humor, Lens, Vitreous humor, Retina
    return surfaces, derivatives, n_indices, eye_length, eye_radius


# Plots the eye model with the surfaces
def plot_eye_model(surfaces, eye_length, eye_radius):
    y = np.linspace(-eye_radius, eye_radius, 1000)  # 1000 points between -eye_radius and eye_radius
    plt.figure(figsize=(14, 10))

    # Plot the internal eye surfaces
    for surface in surfaces:
        surface_points = np.array([surface(yi) for yi in y])  # Calculate the x-coordinates
        plt.plot(surface_points, y, 'k', linewidth=2)  # Plot the surface in black

    plt.gca().set_aspect('equal', adjustable='box')  # Set the aspect ratio of the plot to be equal to keep it circular
    plt.xlim(-10, eye_length + 10)
    plt.ylim(-eye_radius - 1, eye_radius + 1)
    plt.title("Human Eye Refraction Model with Enhanced Light Rays")
    plt.xlabel("Distance (mm)")
    plt.ylabel("Height (mm)")

# Plot colored dots (object) at different y-positions
def plot_colored_dots(x_position):
    colors = ['red', 'green', 'blue', 'brown', 'purple', 'orange', 'pink']
    y_positions = [0, -1.75, 1.75, -3.5, 3.5, -2.25, 2.25]
    for color, y in zip(colors, y_positions):
        plt.plot(x_position, y, 'o', color=color, markersize=5)


# Plot the black_lines for the pupil
def plot_pupil_lines():
    black_line_x = 7
    plt.plot([black_line_x, black_line_x], [4.5, 2.5], 'k-', linewidth=1.5)
    plt.plot([black_line_x, black_line_x], [-4.5, -2.5], 'k-', linewidth=1.5)

    # Return the line position for checking ray intersection
    return [(black_line_x, 2.5, 4.5), (black_line_x, -4.5, -2.5)]

# Main function to create the eye model and trace rays
def main():
    surfaces, derivatives, n_indices, eye_length, eye_radius = create_eye_model()
    plot_eye_model(surfaces, eye_length, eye_radius)

    # Plot colored dots (object)
    dots_x_position = -3
    plot_colored_dots(dots_x_position)

    # Plot the black line for the pupil and get their coordinates for checking ray intersection
    pupil_lines = plot_pupil_lines()

    # Trace rays from colored dots through all surfaces
    colors = ['red', 'green', 'blue', 'brown', 'purple', 'orange', 'pink']
    y_positions = [0, -1.75, 1.75, -3.5, 3.5, -2.25, 2.25]

    for color, start_y in zip(colors, y_positions):
        path = trace_ray(dots_x_position,start_y, surfaces, derivatives, n_indices, pupil_lines)
        xs, ys = zip(*path)
        plt.plot(xs, ys, color=color, linestyle='-', linewidth=1.5)

        # Plot the point where the ray hits the retina or the pupil_lines
        plt.plot(xs[-1], ys[-1], 'o', color=color, markersize=5)
    plt.show()

# Runs when the script is executed directly (not when imported as a module).
if __name__ == "__main__":
    main()