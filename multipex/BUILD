__defaults__(all=dict(resolve="multipex"))

python_requirements(
    name="reqs",
)

python_sources(
    name="lib",
)

pex_binary(
    name="multipex-deps",
    dependencies=[":reqs"],
    # entry_point="main.py", # <-- If you want to let Pants infer everything
    execution_mode=parametrize("venv", "zipapp"),
    include_requirements=True,
    include_sources=False,
    layout=parametrize("loose", "packed", "zipapp"),
    # include_tools=True,
)

pex_binary(
    name="multipex-srcs",
    dependencies=[":multipex-deps", ":lib"],
    execution_mode=parametrize("venv", "zipapp"),
    include_requirements=False,
    include_sources=True,
    layout=parametrize("loose", "packed", "zipapp"),
    # include_tools=True,
)

pex_binary(
    name="multipex",
    dependencies=[":multipex-deps", ":multipex-srcs"],
    executable=":multipex-srcs",
    include_requirements=False,
    include_sources=False,
    # entry_point="main.py",
)

# docker_image(

# )