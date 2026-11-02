from robot_trajectory_guard.validator import validate_trajectory


LIMITS = {"joint_1": {"min_position": -1.0, "max_position": 1.0, "max_velocity": 1.0, "max_acceleration": 5.0}}


def test_valid_trajectory_passes() -> None:
    report = validate_trajectory({"joints": ["joint_1"], "points": [{"time": 0.0, "positions": {"joint_1": 0.0}}, {"time": 1.0, "positions": {"joint_1": 0.5}}]}, LIMITS)
    assert report["valid"] is True


def test_position_velocity_and_acceleration_violations_are_explained() -> None:
    report = validate_trajectory({"joints": ["joint_1"], "points": [{"time": 0.0, "positions": {"joint_1": 0.0}}, {"time": 0.1, "positions": {"joint_1": 2.0}}, {"time": 0.2, "positions": {"joint_1": 0.0}}]}, LIMITS)
    codes = {item["code"] for item in report["violations"]}
    assert {"position_limit", "velocity_limit", "acceleration_limit"} <= codes


def test_empty_trajectory_is_invalid() -> None:
    assert validate_trajectory({}, LIMITS)["valid"] is False
