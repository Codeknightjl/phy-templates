import numpy as np
import matplotlib.pyplot as plt

def plot_parallel_wires(I_1, x_c1, y_c1, I_2, x_c2, y_c2, arrow_density):
    # Define the mesh grid of points
    x, y, z = np.meshgrid(np.linspace(-2, 2, arrow_density), np.linspace(-2, 2, arrow_density), [0])
    # Define the magnetic field components due to the currents
    r1 = np.sqrt((x-x_c1)**2 + (y-y_c1)**2 + (z)**2)
    B_x1 = I_1 * (y-y_c1) / r1**3
    B_y1 = -I_1 * (x-x_c1) / r1**3
    r2 = np.sqrt((x-x_c2)**2 + (y-y_c2)**2 + (z)**2)
    B_x2 = I_2 * (y-y_c2) / r2**3
    B_y2 = -I_2 * (x-x_c2) / r2**3
    B_x = B_x1 + B_x2
    B_y = B_y1 + B_y2
    B_z = np.zeros_like(r1)
    # Plot the magnetic field lines
    fig, ax = plt.subplots(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    # Create the quiver plot of the magnetic field
    ax.quiver(x, y, z, B_x, B_y, B_z, length=4/arrow_density, normalize=True)
    # Plot the wire carrying the current
    z_wire1 = np.linspace(-2, 2, 50)
    x_wire1 = np.full_like(z_wire1, x_c1)
    y_wire1 = np.full_like(z_wire1, y_c1)
    ax.plot(x_wire1, y_wire1, z_wire1, lw=3, color='black')
    z_wire2 = np.linspace(-2, 2, 50)
    x_wire2 = np.full_like(z_wire2, x_c2)
    y_wire2 = np.full_like(z_wire2, y_c2)
    ax.plot(x_wire2, y_wire2, z_wire2, lw=3, color='black')

    # Set the plot limits and axis labels
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    # Show the plot
    plt.show()

plot_parallel_wires(1.0, -1.0, 0.0, -1.0, 1.0, 0.0, 20)
