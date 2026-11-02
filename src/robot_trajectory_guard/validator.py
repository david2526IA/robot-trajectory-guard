"""Small, dependency-free joint-space trajectory validator."""

from __future__ import annotations

from typing import Any


def validate_trajectory(trajectory: dict[str, Any], limits: dict[str, dict[str, float]]) -> dict[str, Any]:
    """Inspect sampled joint positions against position, velocity and acceleration limits.

    Input uses seconds and radians (or another consistent unit declared by the caller).
    The result is an offline review artifact, never a motion command.
    """
    points = trajectory.get("points", [])
    joints = trajectory.get("joints", [])
    violations: list[dict[str, Any]] = []
    if not joints or not points:
        return {"valid": False, "samples": len(points), "violations": [{"code": "empty_trajectory", "message": "joints and points are required"}]}
    previous_velocity: dict[str, float] | None = None
    for index, point in enumerate(points):
        time = point.get("time")
        positions = point.get("positions", {})
        if not isinstance(time, (int, float)) or set(positions) != set(joints):
            violations.append({"code": "invalid_sample", "sample": index, "message": "every sample needs time and all declared joints"})
            continue
        if index and time <= points[index - 1].get("time", float("inf")):
            violations.append({"code": "non_monotonic_time", "sample": index, "message": "sample timestamps must increase"})
            continue
        velocities: dict[str, float] = {}
        for joint in joints:
            limit = limits.get(joint)
            position = positions[joint]
            if limit is None:
                violations.append({"code": "missing_limit", "sample": index, "joint": joint, "message": "no limits configured"})
                continue
            if not limit["min_position"] <= position <= limit["max_position"]:
                violations.append({"code": "position_limit", "sample": index, "joint": joint, "value": position})
            if index:
                delta_t = time - points[index - 1]["time"]
                velocity = (position - points[index - 1]["positions"][joint]) / delta_t
                velocities[joint] = velocity
                if abs(velocity) > limit["max_velocity"]:
                    violations.append({"code": "velocity_limit", "sample": index, "joint": joint, "value": velocity})
                if previous_velocity is not None:
                    acceleration = (velocity - previous_velocity[joint]) / delta_t
                    if abs(acceleration) > limit["max_acceleration"]:
                        violations.append({"code": "acceleration_limit", "sample": index, "joint": joint, "value": acceleration})
        if index:
            previous_velocity = velocities
    return {"valid": not violations, "samples": len(points), "joints": joints, "violations": violations}
