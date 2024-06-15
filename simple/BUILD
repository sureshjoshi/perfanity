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

# TODO: Macro this, or figure out how to nicely parameterize
docker_image(
    name="img_execution_mode_venv_layout_loose",
    instructions=[
        "FROM python:3.9-slim",
        "COPY simple/bin@execution_mode=venv,layout=loose.pex /bin/app",
        'ENTRYPOINT ["/usr/local/bin/python3.9", "/bin/app"]',
    ],
)

docker_image(
    name="img_execution_mode_venv_layout_packed",
    instructions=[
        "FROM python:3.9-slim",
        "COPY simple/bin@execution_mode=venv,layout=packed.pex /bin/app",
        'ENTRYPOINT ["/usr/local/bin/python3.9", "/bin/app"]',
    ],
)

docker_image(
    name="img_execution_mode_venv_layout_zipapp",
    instructions=[
        "FROM python:3.9-slim",
        "COPY simple/bin@execution_mode=venv,layout=zipapp.pex /bin/app",
        'ENTRYPOINT ["/usr/local/bin/python3.9", "/bin/app"]',
    ],
)

docker_image(
    name="img_execution_mode_zipapp_layout_loose",
    instructions=[
        "FROM python:3.9-slim",
        "COPY simple/bin@execution_mode=venv,layout=loose.pex /bin/app",
        'ENTRYPOINT ["/usr/local/bin/python3.9", "/bin/app"]',
    ],
)

docker_image(
    name="img_execution_mode_zipapp_layout_packed",
    instructions=[
        "FROM python:3.9-slim",
        "COPY simple/bin@execution_mode=venv,layout=packed.pex /bin/app",
        'ENTRYPOINT ["/usr/local/bin/python3.9", "/bin/app"]',
    ],
)

docker_image(
    name="img_execution_mode_zipapp_layout_zipapp",
    instructions=[
        "FROM python:3.9-slim",
        "COPY simple/bin@execution_mode=venv,layout=zipapp.pex /bin/app",
        'ENTRYPOINT ["/usr/local/bin/python3.9", "/bin/app"]',
    ],
)
