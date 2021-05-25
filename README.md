# Model calibration protocol examples
This repository contains examples of model calibration.

Step 1 of the protocol, structural identifiability and observability analysis, is performed in MATLAB. The folder 'step1_structural_identifiability' contains MATLAB Live Scripts that reproduce the results reported in the paper. More details are provided in the README file included in the aforementioned folder.

The remaining steps can be reproduced with either the Dockerfile or the Jupyter notebook. The Dockerfile requires basic command-line experience but handles most dependencies, so is recommended over the Jupyter notebook. Furthermore, the Jupyter notebook is setup to reproduce a simplified example, to reduce computation time.

The following sections are related to usage of the Dockerfile to reproduce the example results, except for the last section, which describes usage of the Jupyter notebook as an alternative to the Dockerfile.

For anyone unfamiliar with Python 3, a short tutorial on this subject is recommended.

# Prerequisites
While the toolchain involves tools that are available on most contemporary operating systems, the original work published here was only tested on an Ubuntu 20.04.2 host machine.

Most prerequisites are handled by the Dockerfile. The host machine should have the following tools.
| Tool    | Tested version |
|---------|----------------|
| git     | 2.25.1         |
| docker  | 20.10.6        |

The examples here utilize several packages, including:
- [AMICI](https://github.com/AMICI-dev/AMICI) for simulation with sensitivities for gradient-based optimization,
- [Fides](https://github.com/fides-dev/fides) for efficient optimization methods,
- [PEtab](https://github.com/PEtab-dev/PEtab) for specification of the parameter estimation problem in an interoperable format,
- [pyPESTO](https://github.com/ICB-DCM/pyPESTO) for parameter estimation and uncertainty analysis, and
- [STRIKE-GOLDD](https://github.com/afvillaverde/strike-goldd) for structural identifiability analysis.

The Docker image contains most dependencies required from STEP 3 onwards.

# Setup
Usage of the Docker image involves command-line programs.
1. Download or clone this repository.
```bash
git clone https://github.com/ICB-DCM/model_calibration_protocol_preprint
```

2. Use the `Dockerfile` to build the Docker image.
```bash
docker build -t calibration-pipeline model_calibration_protocol_preprint
```
NB: messages related to "debconf" and "Dialog" were output multiple times but ignored without issue by the authors.

3. Start a Docker container with the Docker image.
```bash
docker run -it --workdir /home/user/model_calibration_protocol_preprint --name calibration-pipeline_container1 calibration-pipeline
```

# Scripts
The `run.py` programs call scripts in the `scripts` directory. These scripts can be edited but note that, in the current setup, altering these scripts will affect their usage in all `settings`.

# Settings
The settings directory contains scripts that specify settings that greatly affect the computational cost of tasks. Included are settings files that specify reduced computational costs, which can be used to quickly test the pipeline; however, results will be poor (for example, insufficient optimization starts or unconverged MCMC chains).

# Usage
- Short tutorials on the Linux command-line or Docker usage is recommended for anyone unfamiliar.
- Basic competence with a command-line text editor (e.g. `nano` or `vim`) can be useful to quickly adjust scripts and settings.
- Alternatively, the Docker volume can be used to transfer files to the host machine for editing.
- The `Bruno_JExpBot2016_quick` setting is provided as a way to quickly try out the pipeline, and specifies simplified calibration tasks. Typical computation time to run all tasks in this setting on a personal laptop should be within 2 hours.

## Run a calibration task
1. (Optional) Customize the task.
    - Edit model-specific settings in the `settings` directory.
    - Edit task commands directly in the `scripts` directory.
2. Execute the task.
    1. Run: `python3 run.py`
    2. Select the setting to use.
    3. Select the task to run.

- Results can be copied to your host machine.
```bash
docker cp calibration-pipeline_container1:/home/user/model_calibration_protocol_preprint/output/. model_calibration_protocol_preprint/output
```

# Jupyter notebook
- A short tutorial on Jupyter notebooks is recommended for anyone unfamiliar.
- Prerequisites for the [AMICI](https://github.com/AMICI-dev/AMICI) tool should be [installed](https://amici.readthedocs.io/en/latest/python_installation.html).
- An installation of Python 3 is also required. The examples have been tested with Python versions 3.7 and 3.8. Use of a Python 3 virtual environment to manage Python dependencies is recommended but not necessary.
- Python environment dependencies are specified in the `requirements.txt` file, as specific package versions to increase reproducibility. This file can be used to automatically install the dependencies into your Python environment. Requirements without specific version are also provided in `general_requirements.txt`, which may be sufficient to use this protocol pipeline with the latest versions of tools.
```bash
pip3 install wheel
pip3 install -r requirements.txt
```
- Notebooks can be run by starting a Jupyter Notebook server. For example:
  1. go to the `notebooks` directory of your local copy of this repository in your terminal; then
  2. launch a notebook server with `jupyter-notebook`; then
  3. a webpage should open in your web browser with a link to the notebook.

# TODO
- change repo names here and in Dockerfile to final repo
- add link to the paper (arxiv, initially)
- switch from test-data to main branch of Benchmark Models
