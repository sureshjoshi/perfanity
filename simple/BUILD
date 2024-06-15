__defaults__(all=dict(resolve="simple"))

python_requirements(
    name="reqs",
)

python_sources(
    name="lib",
)

pex_binary(
    name="bin",
    dependencies=[":lib"],
    entry_point="main.py",
    execution_mode=parametrize("venv", "zipapp"),
    layout=parametrize("loose", "packed", "zipapp"),
)
