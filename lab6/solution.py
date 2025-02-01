"""
author: Dominik Cedro
date: 24.01.2025
description: File contains OOP approach to Boids Flocking animation. User should choose initial parameters and rules.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

COLLISION_AVOID_DISTANCE = 30
NEIGHBOURING_DISTANCE = 40
PLOT_SIZE = 300 # side of the ploat == plot_size * 2
FLOCK_SIZE = 20
class Boid:
    """Represents a single boid in the flock."""

    def __init__(self, position, velocity):
        """Initialize boid with position and velocity."""
        self.position = position
        self.velocity = velocity
        self.acceleration = np.zeros(2)

    def update(self):
        """Update the boid's position and velocity."""
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration = np.zeros(2)
        self.bounce_off_limits()  # Call the method here


    def apply_rules(self, boids):
        """Apply flocking rules to the boid."""
        self.avoid_collisions(boids)
        self.match_velocity(boids)
        self.stay_close(boids)

    def bounce_off_limits(self):
        """Reverse velocity if the boid crosses the limits."""
        if self.position[0] < 0 or self.position[0] > PLOT_SIZE-10:
            self.velocity[0] = -self.velocity[0]
        if self.position[1] < 0 or self.position[1] > PLOT_SIZE-10:
            self.velocity[1] = -self.velocity[1]

    def avoid_collisions(self, boids):
        """Avoid collisions with nearby boids."""
        move = np.zeros(2)
        for boid in boids:
            if boid is not self:
                distance_vector = np.array(self.position) - np.array(boid.position)
                distance = np.linalg.norm(distance_vector)
                if distance < COLLISION_AVOID_DISTANCE:
                    move += distance_vector / distance
        self.acceleration += move

    def match_velocity(self, boids):
        """Match velocity with nearby boids."""
        avg_velocity = np.zeros(2)
        count = 0
        for boid in boids:
            if boid is not self:
                distance_vector = np.array(self.position) - np.array(boid.position)
                distance = np.linalg.norm(distance_vector)
                if distance < NEIGHBOURING_DISTANCE:
                    avg_velocity += boid.velocity
                    count += 1
        if count > 0:
            avg_velocity /= count
            self.acceleration += (avg_velocity - self.velocity) * 0.05

    def stay_close(self, boids):
        """Stay close to nearby boids."""
        center_of_mass = np.zeros(2)
        count = 0
        for boid in boids:
            if boid is not self:
                distance_vector = np.array(self.position) - np.array(boid.position)
                distance = np.linalg.norm(distance_vector)
                if distance < NEIGHBOURING_DISTANCE:
                    center_of_mass += boid.position
                    count += 1
        if count > 0:
            center_of_mass /= count
            self.acceleration += (center_of_mass - self.position) * 0.01

class Flock:
    """Represents a flock of boids."""

    def __init__(self):
        """Initialize the flock with an empty list of boids."""
        self.boids = []

    def update(self):
        """Update all boids in the flock."""
        for boid in self.boids:
            boid.apply_rules(self.boids)
            boid.update()

    def add_boid(self, boid):
        """Add a boid to the flock."""
        self.boids.append(boid)


def visualize_flock(flock):
    """Visualize the flock of boids. I decided to mark each boid with number"""
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 10))

    for _ in range(1000):
        ax.cla()
        for index, boid in enumerate(flock.boids):
            ax.scatter(boid.position[0], boid.position[1], marker=f'${index}$')
        ax.set_xlim(-PLOT_SIZE, PLOT_SIZE)
        ax.set_ylim(-PLOT_SIZE, PLOT_SIZE)
        plt.pause(0.1)
        flock.update()

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    flock = Flock()
    for _ in range(FLOCK_SIZE):
        position = (np.random.rand(2) * 100).tolist()
        velocity = (np.random.rand(2) * 10 - 5).tolist()
        flock.add_boid(Boid(position, velocity))

    visualize_flock(flock)