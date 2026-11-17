"""Vérifie que MoveItPy fonctionne : le bras va en position « ready », la pince s'ouvre puis se ferme.

    ros2 launch tp_moveit_py moveit_py.launch.py
"""

import time

import rclpy
from rclpy.logging import get_logger
from moveit.planning import MoveItPy


def plan_and_execute(robot, component, logger, sleep_time=1.0):
    """Planifie vers le but défini, puis exécute. Renvoie True si tout s'est bien passé."""
    plan = component.plan()
    if not plan:
        logger.error("Échec de la planification")
        return False
    robot.execute(plan.trajectory, controllers=[])
    time.sleep(sleep_time)
    return True


def main():
    rclpy.init()
    logger = get_logger("verif")

    panda = MoveItPy(node_name="moveit_py")
    arm = panda.get_planning_component("panda_arm")
    hand = panda.get_planning_component("hand")
    logger.info("MoveItPy est prêt")

    resultats = []

    arm.set_start_state_to_current_state()
    arm.set_goal_state(configuration_name="extended")
    resultats.append(("bras -> extended", plan_and_execute(panda, arm, logger)))

    arm.set_start_state_to_current_state()
    arm.set_goal_state(configuration_name="ready")
    resultats.append(("bras -> ready", plan_and_execute(panda, arm, logger)))

    for etat in ["open", "close"]:
        hand.set_start_state_to_current_state()
        hand.set_goal_state(configuration_name=etat)
        resultats.append((f"pince -> {etat}", plan_and_execute(panda, hand, logger)))

    # Bilan, encadré pour être repéré facilement dans le terminal
    nb_ok = sum(1 for _, ok in resultats if ok)
    logger.info("=" * 50)
    for nom, ok in resultats:
        logger.info(f"  [{'OK' if ok else 'ÉCHEC'}] {nom}")
    if nb_ok == len(resultats):
        logger.info(f"  Vérification réussie : {nb_ok}/{len(resultats)}")
        logger.info("  Vous pouvez passer à votre propre script (sequence.py).")
    else:
        logger.error(f"  Vérification échouée : {nb_ok}/{len(resultats)}")
        logger.error("  Relancez la commande ; si l'échec persiste, prévenez l'enseignant.")
    logger.info("=" * 50)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
