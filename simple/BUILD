__defaults__(all=dict(resolve="simple"))

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
#     name = "img",
#     repository = "app",
#     instructions = [
#         "FROM python:3.10-slim",
#         'ENTRYPOINT ["/usr/local/bin/python3.10", "/bin/app"]',
#         "COPY dist./binary.pex /bin/app",
#     ]
# )
