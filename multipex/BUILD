__defaults__(all=dict(resolve="multipex"))

python_requirements(
    name="reqs",
)

python_sources(
    name="lib",
)

# pex_binary(
#     name="multipex-deps",
#     dependencies=[":reqs"],
#     # entry_point="main.py", # <-- If you want to let Pants infer everything
#     layout="packed",
#     include_requirements=True,
#     include_sources=False,
#     # include_tools=True,
# )

# pex_binary(
#     name="multipex-srcs",
#     dependencies=[":lib"],
#     # entry_point="main.py",
#     layout="packed",
#     include_requirements=False,
#     include_sources=True,
#     # include_tools=True,
# )

# # Do we even need this?
# pex_binary(
#     name="multipex",
#     dependencies=[":multipex-deps", ":multipex-srcs"],
#     executable=":multipex-srcs",
#     # entry_point="main.py",
# )
