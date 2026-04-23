# TurtleBot3 Maze Navigator — ROS2 Jazzy

Autonomous wall-following robot that navigates a maze using only
LiDAR data, built with ROS2 Jazzy + Gazebo Harmonic.

![demo](demo.gif)

## Overview

The robot subscribes to `/scan` (360° LaserScan) and publishes
velocity commands to `/cmd_vel` (TwistStamped). A right-hand
wall-following algorithm processes the LiDAR sectors in real time
to keep the robot moving through the maze without hitting walls.

## System requirements

- Ubuntu 24.04
- ROS2 Jazzy
- Gazebo Harmonic
- TurtleBot3 packages (built from source)

## Installation

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/YOUR_USERNAME/maze_navigator.git
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select maze_navigator
source install/setup.bash
```

## Run

Terminal 1 — launch Gazebo:
```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Terminal 2 — run the navigator:
```bash
ros2 run maze_navigator maze_navigator
```

## How the algorithm works

| Sensor condition | Action |
|---|---|
| Obstacle ahead < 0.5m | Turn left |
| No wall on right | Turn right to find wall |
| Too close to right wall | Steer left |
| Corner detected ahead-right | Early left turn |
| Clear path, wall in range | Go straight |

## Key concepts covered

- ROS2 publisher / subscriber pattern
- LaserScan message — reading and slicing range sectors
- TwistStamped vs Twist (Gazebo Harmonic breaking change)
- TF2 coordinate frames
- RViz2 visualization
- ament_python package structure

## Troubleshooting

**Robot not moving** — Gazebo Harmonic requires `TwistStamped`
on `/cmd_vel`, not plain `Twist`. This is a breaking change from
earlier ROS2 versions. The node handles this correctly.

**`/scan` topic missing** — the `ros_gz_bridge` didn't start.
Kill and relaunch `turtlebot3_world.launch.py`.

**`Package not found`** — run `source ~/ros2_ws/install/setup.bash`
after every `colcon build`.

## Roadmap

- [ ] Nav2 integration for goal-based navigation
- [ ] SLAM Toolbox for real-time map building
- [ ] Physical TurtleBot3 deployment

## Author

Your Name
[LinkedIn](https://linkedin.com/in/YOUR_PROFILE)
