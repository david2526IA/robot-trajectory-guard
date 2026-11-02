# Robot Trajectory Guard

An offline validator for sampled robot joint trajectories. It checks position, velocity and acceleration limits before a trajectory is handed to a simulator, planner or robot-specific integration.

It is intentionally not a robot controller: it sends no commands, has no network integration and cannot establish functional safety. Use it as a transparent engineering check alongside a robot manufacturer's requirements, risk assessment and qualified review.

## Input format

`trajectory.json`:

```json
{"joints":["joint_1"],"points":[{"time":0.0,"positions":{"joint_1":0.0}},{"time":1.0,"positions":{"joint_1":0.5}}]}
```

`limits.json`:

```json
{"joint_1":{"min_position":-1.0,"max_position":1.0,"max_velocity":1.0,"max_acceleration":5.0}}
```

## Run

```bash
pip install .
trajectory-guard trajectory.json limits.json --output trajectory_report.json
```

The JSON report explains every violated limit with its sample and joint. It makes no claim that a valid report makes a deployment safe.

## Development

```bash
pip install ".[dev]"
pytest -q
```

## License

MIT
