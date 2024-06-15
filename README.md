# perfanity

A pre-requisite for using this repo is reading Josh Cannon's awesome pex/docker optimization blog post: https://www.pantsbuild.org/blog/2022/08/02/optimizing-python-docker-deploys-using-pants

The aim of this repo is to run a series of experiments to determine the optimal `pex` and `docker` configurations for a given workflow (e.g. what the user deems most important - build size? build speed? execution startup? cache-something? network-something? etc...). 

If some handy macros happen to fall out of this, well that would be gravy.

The current code is a mess, as this is still experimentation, but this is the type of output I'm aiming for:

```bash
step                                             clean               noop           incremental           
goal                                           package   run test package  run test     package   run test
simple:bin@execution_mode=venv,layout=loose       4.02 11.29 1.11    1.00 3.63 0.09        4.10 11.03 1.11
simple:bin@execution_mode=venv,layout=packed      1.23  3.02 0.09    0.09 1.08 0.25        1.17  1.71 1.10
simple:bin@execution_mode=venv,layout=zipapp      6.38  0.94 0.08    0.08 0.89 0.08        6.40  1.51 1.08
simple:bin@execution_mode=zipapp,layout=loose     4.23  9.02 0.09    0.96 8.93 0.09        4.19  9.45 1.04
simple:bin@execution_mode=zipapp,layout=packed    1.15  1.36 0.08    0.08 1.20 0.09        1.15  1.26 1.08
simple:bin@execution_mode=zipapp,layout=zipapp    6.35  1.30 0.08    0.08 1.38 0.16        6.43  1.30 1.06
```