__defaults__(all=dict(resolve="multipex"))

python_requirements(
    name="reqs",
)

python_sources(
    name="lib",
)

pex_binary(
    name="multipex-deps",
    # dependencies=[":reqs"],
    entry_point="main.py", # <-- If you want to let Pants infer everything
    execution_mode="venv",
    include_requirements=True,
    include_sources=False,
    include_tools=True,
    layout="packed",
)

pex_binary(
    name="multipex-srcs",
    # dependencies=[":lib"],
    entry_point="main.py", # <-- If you want to let Pants infer everything
    execution_mode="venv",
    include_requirements=False,
    include_sources=True,
    include_tools=True,
    layout="packed",
)

docker_image(
    name="img",
    instructions=[
        "FROM python:3.9-slim as deps",
        "COPY multipex/multipex-deps.pex /deps.pex",
        "RUN PEX_TOOLS=1 /usr/local/bin/python3.9 /deps.pex venv --scope=deps --bin-path prepend --compile --rm all /app",

        "FROM python:3.9-slim as srcs",
        "COPY multipex/multipex-srcs.pex /srcs.pex",
        "RUN PEX_TOOLS=1 /usr/local/bin/python3.9 /srcs.pex venv --scope=srcs --bin-path prepend --compile --rm all /app",

        "FROM python:3.9-slim",
        "COPY --from=deps /app /app",
        "COPY --from=srcs /app /app",
        'ENTRYPOINT ["/app/pex"]',
    ],
)

docker_image(
    name = "img-deps",
    # registry=["companyname"],
    image_tags=["deps"],
    skip_push=True,
    instructions = [
        "FROM python:3.9-slim as builder",
        "COPY multipex/multipex-deps.pex /deps.pex",
        "RUN PEX_TOOLS=1 /usr/local/bin/python3.9 /deps.pex venv --scope=deps --bin-path prepend --compile --rm all /app",

        # This removes the copy of the pex file - which can save a couple hundred megs, at the cost of a COPY
        "FROM python:3.9-slim",
        "COPY --from=builder /app /app",
    ]
)

docker_image(
    name = "img-srcs",
    # registry=["companyname"],
    image_tags=["srcs"],
    skip_push=True,
    instructions = [
        "FROM python:3.9-slim",
        "COPY multipex/multipex-srcs.pex /srcs.pex",
        "RUN PEX_TOOLS=1 /usr/local/bin/python3.9 /srcs.pex venv --scope=srcs --bin-path prepend --compile --rm all /app",
    ]
)

docker_image(
    name = "img1",
    dependencies=[":img-srcs", ":img-deps"],
    instructions = [
        "FROM python:3.9-slim",
        'ENTRYPOINT ["/app/pex"]',
        "COPY --from=companyname/app:deps /app /app",
        "COPY --from=companyname/app:srcs /app /app",
    ]
)