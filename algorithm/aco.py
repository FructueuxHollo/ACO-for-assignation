import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils.method.generatepath import generate_paths
from utils.method.visualization import visualize_network
from utils.method.pheromone_update import pheromone_update
from utils.method.evaluate import evaluate, format_duration


def ACO(jobs, workers, matches, ants, alpha, beta, evap_coeff, Q, max_iterations=100, tolerance=1e-5, patience=20, verbose=0, animate=0, learning_curve=0):
    """
    Runs the Ant Colony Optimization (ACO) algorithm to find the optimal job-worker assignments.
    
    :param jobs: List of jobs.
    :param matches: List of Match objects (job-worker pairs with pheromone and processing duration).
    :param ants: List of Ant objects, where each ant has a path.
    :param alpha: Pheromone influence factor.
    :param beta: Heuristic information influence factor.
    :param evap_coeff: Coefficient for pheromone evaporation (ρ).
    :param Q: Constant value for pheromone deposition.
    :param max_iterations: Maximum number of iterations to run.
    :param tolerance: Threshold to stop the algorithm when the change in total duration is small enough.
    :param patience: Number of consecutive iterations without significant improvement before stopping.
    :return: A tuple containing the optimal path and the total processing duration.
    """
    makespans = []
    previous_duration = float('inf')  # Start with an infinitely large duration
    iteration = 0
    no_improvement_count = 0  # Counter for iterations without significant improvement
    if animate:
        fig, ax = plt.subplots(figsize=(12, 8))
        frames = []

        # Directory to store frames temporarily
        temp_dir = "./frames"
        os.makedirs(temp_dir, exist_ok=True)

    while iteration < max_iterations:
        if animate:
            # Clear axis to prevent overlap
            ax.clear()
        
        # Generate paths for ants based on current pheromone levels
        ants = generate_paths(ants, jobs, matches, alpha, beta)

        # Update pheromone levels based on the paths taken by the ants
        matches = pheromone_update(ants, matches, evap_coeff, Q)

        if animate:
            # Capture frame
            visualize_network(jobs, workers, matches, ax)
            ax.set_title(f"Iteration {iteration}")
    
            # Save the current figure as an image file and store the filename
            filename = os.path.join(temp_dir, f"frame_{iteration}.png")
            plt.savefig(filename, dpi= 300)
            frames.append(filename)

        # Evaluate the current best path and its total duration
        optimal_path, total_duration = evaluate(jobs, matches)

        makespans.append(total_duration)

        # Calculate the difference in total duration between iterations
        duration_difference = abs(previous_duration - total_duration)

        # Check if the difference is below the tolerance (convergence criteria)
        if duration_difference < tolerance:
            no_improvement_count += 1
        else:
            no_improvement_count = 0  # Reset the count if there's significant improvement

        # If there has been no significant improvement for a certain number of iterations, break
        if no_improvement_count >= patience:
            if verbose:
                print(f"No significant improvement for {patience} consecutive iterations. Stopping.")
                print(f"Converged at iteration {iteration} with duration difference {duration_difference}")
            break

        # Update previous duration and increment iteration counter
        previous_duration = total_duration
        iteration += 1

    if animate:
        # Compile images into an animation
        images = [plt.imread(frame) for frame in frames]
        ani = animation.ArtistAnimation(fig, [[plt.imshow(img, animated=True)] for img in images], interval=500, blit=True)
        ani.save("output/ACO_animation.gif", writer="pillow", fps=2)
    
        # Clean up temporary frame files
        for frame in frames:
            os.remove(frame)
        os.rmdir(temp_dir)

    plt.show()

    if learning_curve:
        # Plot the learning curve
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(makespans)), makespans, marker='o')
        plt.title("Learning Curve of ACO")
        plt.xlabel("Iteration")
        plt.ylabel("Makespan (Total Duration)")
        plt.grid()
        plt.savefig("output/learning_curve.png", dpi=300)
        plt.show()
    
    # Return the best path found and its total processing duration
    print(format_duration(total_duration))
    return optimal_path, total_duration
