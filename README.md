# perfanity

A pre-requisite for using this repo is reading Josh Cannon's awesome pex/docker optimization blog post: https://www.pantsbuild.org/blog/2022/08/02/optimizing-python-docker-deploys-using-pants

The aim of this repo is to run a series of experiments to determine the optimal `pex` and `docker` configurations for a given workflow (e.g. what the user deems most important - build size? build speed? execution startup? cache-something? network-something? etc...). 

If some handy macros happen to fall out of this, well that would be gravy.

The current code is a mess, as this is still experimentation, but this is the type of output I'm aiming for:

```bash
step                                             clean               noop           incremental           
goal                                           package   run test package  run test     package   run test
simple:bin@execution_mode=venv,layout=loose       0.99 12.56 1.71    1.03 3.51 0.09        5.05 11.22 1.20
simple:bin@execution_mode=zipapp,layout=loose     4.88  9.23 0.14    1.06 9.32 0.09        4.81  9.14 1.16
simple:bin@execution_mode=venv,layout=packed      1.24  1.92 0.13    0.08 1.01 0.09        1.18  1.35 1.08
simple:bin@execution_mode=zipapp,layout=packed    1.15  1.18 0.09    0.15 1.11 0.09        1.15  1.15 1.16
simple:bin@execution_mode=venv,layout=zipapp      6.97  1.48 0.08    0.08 0.92 0.09        6.42  1.64 1.04
simple:bin@execution_mode=zipapp,layout=zipapp    6.41  1.32 0.08    0.08 1.29 0.08        6.39  1.36 1.06
```