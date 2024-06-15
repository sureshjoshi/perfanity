__defaults__(all=dict(resolve="multistage"))

python_requirements(
    name="reqs",
)

python_sources(
    name="lib",
)

python_tests()

pex_binary(
    name="bin",
    dependencies=[":lib"],
    entry_point="main.py",
    execution_mode=parametrize("venv", "zipapp"),
    layout=parametrize("loose", "packed", "zipapp"),
)

# docker_image(
    
# )