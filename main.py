# Import the necessary libraries
import matplotlib.pyplot as plt
from My_Functions import *

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