"""Lance le bras Panda (simulé, sans physique), RViz et un script Python MoveItPy.

Utilisation :
    ros2 launch tp_moveit_py moveit_py.launch.py                    # script de vérification
    ros2 launch tp_moveit_py moveit_py.launch.py script:=sequence   # votre script
    ros2 launch tp_moveit_py moveit_py.launch.py log_level:=info    # afficher aussi tous les messages de MoveIt

Les autres nœuds (RViz, ros2_control…) écrivent dans les fichiers de log (~/.ros/log/), pas dans le terminal.
Dans le processus du script, seuls les avertissements et erreurs de MoveIt s'affichent (log_level:=warn par
défaut), tandis que les messages de vos scripts (loggers verif, sequence, prise) restent affichés.

Fichier adapté du tutoriel officiel MoveItPy (moveit2_tutorials, licence BSD) :
https://github.com/moveit/moveit2_tutorials/tree/main/doc/examples/motion_planning_python_api
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    tp_share = get_package_share_directory("tp_moveit_py")
    panda_share = get_package_share_directory("moveit_resources_panda_moveit_config")

    # Description du robot, configuration MoveIt et contrôleurs (bras + pince)
    moveit_config = (
        MoveItConfigsBuilder(robot_name="panda", package_name="moveit_resources_panda_moveit_config")
        .robot_description(file_path="config/panda.urdf.xacro")
        .trajectory_execution(file_path="config/gripper_moveit_controllers.yaml")
        .moveit_cpp(file_path=os.path.join(tp_share, "config", "moveit_py.yaml"))
        .to_moveit_configs()
    )

    script_arg = DeclareLaunchArgument(
        "script",
        default_value="verif",
        description="Script Python du package tp_moveit_py à lancer (verif, sequence, ...)",
    )

    log_level_arg = DeclareLaunchArgument(
        "log_level",
        default_value="warn",
        description="Niveau des messages de MoveIt dans le terminal (debug, info, warn, error)",
    )

    # Votre script Python MoveItPy : les messages de MoveIt sont filtrés (log_level),
    # ceux de vos scripts restent au niveau info.
    moveit_py_node = Node(
        name="moveit_py",
        package="tp_moveit_py",
        executable=LaunchConfiguration("script"),
        output="both",
        parameters=[moveit_config.to_dict()],
        ros_arguments=[
            "--log-level", LaunchConfiguration("log_level"),
            "--log-level", "verif:=info",
            "--log-level", "sequence:=info",
            "--log-level", "prise:=info",
        ],
    )

    # Visualisation
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="log",
        arguments=["-d", os.path.join(tp_share, "config", "panda_moveit_py.rviz")],
        parameters=[moveit_config.robot_description, moveit_config.robot_description_semantic],
    )

    static_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="static_transform_publisher",
        output="log",
        arguments=["--frame-id", "world", "--child-frame-id", "panda_link0"],
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="log",
        parameters=[moveit_config.robot_description],
    )

    # ros2_control avec un matériel simulé (mock) : le bras suit exactement les consignes
    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[os.path.join(panda_share, "config", "ros2_controllers.yaml")],
        remappings=[("/controller_manager/robot_description", "/robot_description")],
        output="log",
    )

    spawners = [
        ExecuteProcess(cmd=[f"ros2 run controller_manager spawner {controller}"], shell=True, output="log")
        for controller in ["panda_arm_controller", "panda_hand_controller", "joint_state_broadcaster"]
    ]

    return LaunchDescription(
        [script_arg, log_level_arg, moveit_py_node, robot_state_publisher, ros2_control_node, rviz_node, static_tf]
        + spawners
    )
