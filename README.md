# _

## labs accumulated for computer vision course
All the subprojects use uv for dependency management and marimo notebooks for
tasks

### prerequisites
You need to have uv and zlib installed (for numpy)

In order to compile reports you need to have texlive, see guix.scm for more
details

To collect all development dependencies you can use guix, run
```sh
guix shell -CNFm guix.scm $your_development_packages
```

### structure
Usually subprojects are defined like that:
```
lab$n
├── notebooks
│   ├── task1.py
│   ├── ... 
│   └── task$m.py
├── pyproject.toml
├── README.md
├── report
│   ├── report.tex
│   └── Makefile # run to build the report
└── src
    └── lab$n # modules needed for tasks
```

### instructions to run
```sh
uv sync
marimo edit notebooks/task$n.py
```
