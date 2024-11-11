import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk

# Configuration class for simulation parameters
class SimulationConfig:
    def __init__(self, alpha=0.000023, dx=0.01, dy=0.01, dt=0.001, nx=50, ny=50, nt=100, Q=0.05):
        self.alpha = alpha
        self.dx = dx
        self.dy = dy
        self.dt = dt
        self.nx = nx
        self.ny = ny
        self.nt = nt
        self.Q = Q

# Initialize the temperature grid
def initialize_grid(config: SimulationConfig) -> np.ndarray:
    T = np.zeros((config.nx, config.ny))
    T[int(config.nx / 4):int(3 * config.nx / 4), int(config.ny / 4):int(3 * config.ny / 4)] = 100
    return T

# Apply boundary conditions
def apply_boundary_conditions(T: np.ndarray, config: SimulationConfig, boundary_type="insulated"):
    if boundary_type == "insulated":
        T[0, :] = T[1, :]
        T[-1, :] = T[-2, :]
        T[:, 0] = T[:, 1]
        T[:, -1] = T[:, -2]
    elif boundary_type == "fixed":
        T[0, :] = 0
        T[-1, :] = 0
        T[:, 0] = 0
        T[:, -1] = 0
    return T

# Update temperature function
def update_temperature(T: np.ndarray, config: SimulationConfig) -> np.ndarray:
    T_new = np.copy(T)
    for i in range(1, config.nx - 1):
        for j in range(1, config.ny - 1):
            T_new[i, j] = T[i, j] + config.dt * (
                config.alpha * ((T[i + 1, j] - 2 * T[i, j] + T[i - 1, j]) / config.dx**2 +
                                (T[i, j + 1] - 2 * T[i, j] + T[i, j - 1]) / config.dy**2) + config.Q
            )
    T_new = apply_boundary_conditions(T_new, config, boundary_type="insulated")
    return T_new

# Animate the simulation
def animate_simulation(initial_T: np.ndarray, config: SimulationConfig):
    fig, ax = plt.subplots()
    mat = ax.matshow(initial_T, cmap='hot')
    plt.colorbar(mat)

    # Define a nested function to update the temperature at each frame
    def update(frame, T):
        T[:] = update_temperature(T, config)
        mat.set_data(T)
        return [mat]

    ani = animation.FuncAnimation(fig, update, fargs=(initial_T,), frames=config.nt, blit=False)
    plt.show()

# GUI to take input parameters
def run_gui():
    def start_simulation():
        # Retrieve values from the entries
        config = SimulationConfig(
            alpha=float(entry_alpha.get()),
            dx=float(entry_dx.get()),
            dy=float(entry_dy.get()),
            dt=float(entry_dt.get()),
            nx=int(entry_nx.get()),
            ny=int(entry_ny.get()),
            nt=int(entry_nt.get()),
            Q=float(entry_Q.get())
        )

        # Initialize the temperature grid
        T = initialize_grid(config)
        
        # Run the simulation with real-time visualization
        animate_simulation(T, config)

    # Create the main window
    root = tk.Tk()
    root.title("Heat Transfer Simulation Parameters")

    # Add input fields
    fields = [
        ("Thermal diffusivity (alpha)", "0.000023"),
        ("Spatial step in x direction (dx)", "0.01"),
        ("Spatial step in y direction (dy)", "0.01"),
        ("Time step (dt)", "0.001"),
        ("Number of grid points in x direction (nx)", "50"),
        ("Number of grid points in y direction (ny)", "50"),
        ("Number of time steps (nt)", "100"),
        ("Heat source term (Q)", "0.05")
    ]
    entries = {}

    for idx, (label, default) in enumerate(fields):
        tk.Label(root, text=label).grid(row=idx, column=0, padx=5, pady=5)
        entry = tk.Entry(root)
        entry.insert(0, default)
        entry.grid(row=idx, column=1, padx=5, pady=5)
        entries[label] = entry

    # Assigning each entry to a variable
    entry_alpha = entries["Thermal diffusivity (alpha)"]
    entry_dx = entries["Spatial step in x direction (dx)"]
    entry_dy = entries["Spatial step in y direction (dy)"]
    entry_dt = entries["Time step (dt)"]
    entry_nx = entries["Number of grid points in x direction (nx)"]
    entry_ny = entries["Number of grid points in y direction (ny)"]
    entry_nt = entries["Number of time steps (nt)"]
    entry_Q = entries["Heat source term (Q)"]

    # Add a button to start the simulation
    tk.Button(root, text="Start Simulation", command=start_simulation).grid(row=len(fields), column=0, columnspan=2, pady=10)

    root.mainloop()

# Run the GUI
run_gui()
