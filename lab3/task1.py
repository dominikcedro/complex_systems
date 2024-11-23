"""
author: Dominik Cedro
date: 23.11.2024
description: implement oslo model based on instruction from lab3
"""

# initialize the system in arbitrary stable configuration z_i <=z^T _i where z^T _i is the i-th slope threshold - {1,2}

# drive the system by adding a grain at left-most site

#if z_i > z^T _i relax the site i
#   i = 1: z_1 -> z_1-2 ->z_2+1
#   i = 2...L-1: z_i -> z_i-2, z_{i+1} ->z_2+1
#   i = L: z_1 -> z_1-2 ->z_2+1

# todos

# TODO(1) research Oslo rice/grain modeld
# TODO(1) report start with introduction of problem
# TODO(2) what is the goal of exercise
# TODO(3) what tools to use to achieve the goals
# TODO(4) implement tools to achieve goals
# TODO(5) review
