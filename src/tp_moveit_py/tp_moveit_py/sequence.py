"""Étape 4 : enchaîner des mouvements du Panda avec MoveItPy.

Lancement :
    ros2 launch tp_moveit_py moveit_py.launch.py script:=sequence

Complétez les parties marquées TODO. Pas besoin de recompiler après une modification
si le workspace a été compilé avec « colcon build --symlink-install ».
"""

import time

import rclpy
from rclpy.logging import get_logger
from moveit.planning import MoveItPy
from geometry_msgs.msg import Pose, PoseStamped
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive


def plan_and_execute(robot, component, logger, sleep_time=1.0):
    """Planifie vers le but défini, puis exécute. Renvoie True si tout s'est bien passé."""
    plan = component.plan()
    if not plan:
        logger.error("Échec de la planification")
        return False
    robot.execute(plan.trajectory, controllers=[])
    time.sleep(sleep_time)
    return True


def pose_pince_vers_le_bas(x, y, z):
    """Pose de panda_link8 (bout du bras) à la position (x, y, z) en mètres, pince tournée vers le bas."""
    pose = PoseStamped()
    pose.header.frame_id = "panda_link0"
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z
    # Rotation de 180° autour de x : la pince pointe vers le bas
    pose.pose.orientation.x = 1.0
    pose.pose.orientation.y = 0.0
    pose.pose.orientation.z = 0.0
    pose.pose.orientation.w = 0.0
    return pose


def ajouter_boite(planning_scene_monitor, nom, position, dimensions):
    """Ajoute une boîte (obstacle) dans la scène de planification de MoveIt."""
    with planning_scene_monitor.read_write() as scene:
        objet = CollisionObject()
        objet.header.frame_id = "panda_link0"
        objet.id = nom

        boite = SolidPrimitive()
        boite.type = SolidPrimitive.BOX
        boite.dimensions = list(dimensions)

        pose = Pose()
        pose.position.x, pose.position.y, pose.position.z = position
        pose.orientation.w = 1.0

        objet.primitives.append(boite)
        objet.primitive_poses.append(pose)
        objet.operation = CollisionObject.ADD

        scene.apply_collision_object(objet)
        scene.current_state.update()


def main():
    rclpy.init()
    logger = get_logger("sequence")

    panda = MoveItPy(node_name="moveit_py")
    arm = panda.get_planning_component("panda_arm")
    hand = panda.get_planning_component("hand")
    scene = panda.get_planning_scene_monitor()

    # 1. Pose nommée : position de départ « ready »
    arm.set_start_state_to_current_state()
    arm.set_goal_state(configuration_name="ready")
    plan_and_execute(panda, arm, logger)

    # 2. Pose cartésienne : bout du bras à 40 cm devant, 20 cm à gauche, 40 cm de haut
    arm.set_start_state_to_current_state()
    arm.set_goal_state(pose_stamped_msg=pose_pince_vers_le_bas(0.4, 0.2, 0.4), pose_link="panda_link8")
    plan_and_execute(panda, arm, logger)

    # 3. TODO : ouvrir puis fermer la pince
    #    (groupe « hand », poses nommées « open » et « close »)

    # 4. TODO : ajouter un obstacle avec ajouter_boite(...) entre deux poses,
    #    par exemple une boîte de 5 cm x 40 cm x 50 cm centrée en (0.45, 0.0, 0.25)

    # 5. TODO : enchaîner trois poses cartésiennes de part et d'autre de l'obstacle,
    #    et vérifier dans RViz que le bras le contourne

    # 6. Retour à la position de départ
    arm.set_start_state_to_current_state()
    arm.set_goal_state(configuration_name="ready")
    plan_and_execute(panda, arm, logger)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
