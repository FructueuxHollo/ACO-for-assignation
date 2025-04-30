import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm

from utils.method.generatepath import generate_paths
from utils.method.visualization import visualize_network
from utils.method.pheromone_update import pheromone_update_minmax, init_min_max_pheromones
from utils.method.evaluate import evaluate, format_duration

def ACO_elitist_minmax(jobs,
        workers,
        matches,
        ants,
        alpha,
        beta,
        evap_coeff,
        Q,
        max_iterations=100,
        tolerance=1e-5,
        patience=10,
        verbose=0,
        animate=0,
        learning_curve=0):
    """
    Runs the Elitist Min–Max Ant Colony Optimization (ACO) algorithm to find optimal job-worker assignments.

    :param jobs: List of jobs.
    :param workers: List of worker resources (for visualization).
    :param matches: List of Match objects (job-worker pairs with pheromone and processing duration).
    :param ants: List of Ant objects, where each ant has a `path` attribute.
    :param alpha: Pheromone influence factor.
    :param beta: Heuristic information influence factor.
    :param evap_coeff: Coefficient for pheromone evaporation (ρ).
    :param Q: Constant for pheromone deposition.
    :param max_iterations: Maximum number of iterations.
    :param tolerance: Threshold for convergence (change in makespan).
    :param patience: Number of iterations without improvement before stopping.
    :param verbose: Verbosity flag.
    :param animate: Flag to generate an animation of the search.
    :param learning_curve: Flag to plot and save the learning curve.
    :return: Tuple (best_global_path, best_global_length).
    """
    # 1) Initial global best from current pheromones
    best_global_path, best_global_length = evaluate(jobs, matches)

    # 2) Initialize Min–Max pheromone bounds
    tau_min, tau_max = init_min_max_pheromones(evap_coeff,
                                               best_global_length,
                                               n_decisions=len(jobs))

    makespans = []
    previous_duration = float('inf')
    no_improve_count = 0
    iteration = 0

    # Setup animation if requested
    if animate:
        fig, ax = plt.subplots(figsize=(12, 8))
        frames = []
        temp_dir = "./frames"
        os.makedirs(temp_dir, exist_ok=True)

    # Main loop
    while iteration < max_iterations:
        # Animate: clear previous frame
        if animate:
            ax.clear()

        # 3) Construct solutions
        ants = generate_paths(ants, jobs, matches, alpha, beta)

        # 4) Pheromone update (Elitist Min–Max)
        matches = pheromone_update_minmax(ants,
                                          matches,
                                          evap_coeff,
                                          Q,
                                          best_global_path,
                                          best_global_length,
                                          tau_min,
                                          tau_max)

        # Animate: capture current network state
        if animate:
            visualize_network(jobs, workers, matches, ax)
            ax.set_title(f"Iteration {iteration}")
            fname = os.path.join(temp_dir, f"frame_{iteration}.png")
            plt.savefig(fname, dpi=300)
            frames.append(fname)

        # 5) Evaluate current best from pheromones
        current_path, current_length = evaluate(jobs, matches)
        makespans.append(current_length)

        # 6) Update global best if improved
        if current_length < best_global_length:
            best_global_path, best_global_length = current_path, current_length
            tau_min, tau_max = init_min_max_pheromones(evap_coeff,
                                                       best_global_length,
                                                       n_decisions=len(jobs))

        # 7) Convergence check
        diff = abs(previous_duration - current_length)
        if diff < tolerance:
            no_improve_count += 1
        else:
            no_improve_count = 0

        if no_improve_count >= patience:
            if verbose:
                print(f"No improvement for {patience} iterations. Stopping at iter {iteration}.")
            break

        previous_duration = current_length
        iteration += 1

    # Build animation GIF if requested
    if animate and frames:
        images = [plt.imread(f) for f in frames]
        ani = animation.ArtistAnimation(
            fig,
            [[plt.imshow(img, animated=True)] for img in images],
            interval=500,
            blit=True
        )
        os.makedirs("output", exist_ok=True)
        ani.save("output/ACO_animation.gif", writer="pillow", fps=2)
        # Clean up
        for f in frames:
            os.remove(f)
        os.rmdir(temp_dir)

    # Plot learning curve
    if learning_curve:
        os.makedirs("output", exist_ok=True)
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(makespans)), makespans, marker='o')
        plt.title("Learning Curve of ACO")
        plt.xlabel("Iteration")
        plt.ylabel("Makespan (Total Duration)")
        plt.grid()
        plt.savefig("output/learning_curve.png", dpi=300)
        plt.show()

    # Final output
    if verbose:
        print(f"Best makespan: {format_duration(best_global_length)}")
    return best_global_path, best_global_length


