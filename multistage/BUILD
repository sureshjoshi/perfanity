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
    include_tools=True,
    layout=parametrize("loose", "packed", "zipapp"),
)

# TODO: Can probably remove the `rm` as that's what multi-stage builders should already take care of
# TODO: Check if the intermediate builder images are cached, if so, this might matter
docker_image(
    name="img_execution_mode_venv_layout_packed",
    image_tags=["multistage"],
    instructions=[
        "FROM python:3.9-slim as deps",
        "COPY multistage/bin@execution_mode=venv,layout=packed.pex /deps.pex",
        "RUN PEX_TOOLS=1 /usr/local/bin/python3.9 /deps.pex venv --scope=deps --bin-path prepend --compile --rm all /app",
        "FROM python:3.9-slim as srcs",
        "COPY multistage/bin@execution_mode=venv,layout=packed.pex /srcs.pex",
        "RUN PEX_TOOLS=1 /usr/local/bin/python3.9 /srcs.pex venv --scope=srcs --bin-path prepend --compile --rm all /app",
        "FROM python:3.9-slim",
        "COPY --from=deps /app /app",
        "COPY --from=srcs /app /app",
        'ENTRYPOINT ["/app/pex"]',
    ],
)
