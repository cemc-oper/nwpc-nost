# nwpc-nost

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/707d50ccf05b4648af89622487a69f25)](https://www.codacy.com/app/perillaroc/nwpc-nost?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=perillaroc/nwpc-nost&amp;utm_campaign=Badge_Grade)

> nwpc-operation-system-tool

NWPC operation system tool suite, including such components:

* A job submission script using in SMS.
* CLI commands used to manipulate SMS client and SMS server.

## Introduction

Please refer to `README.md` in each component's directory for detailed introductions.

### Slurm Client :sunny:

A CLI client for Slurm in NWPC.

### LoadLeveler Client :sunny:

A CLI client for LoadLeveler in NWPC.

### NWPC Data Client :sunny:

A CLI command to find data in NWPC's HPC.

### Job Submission Tool :cloud:

Including SMS and ecFlow Job Submission script and SMS's job submission analytics script.

#### Submission script

Submit job scripts of SMS to LoadLeveler, and check whether the submission is succeeded.

#### Submission Error Log Analytics Script

A script to analyze the error log of SMS job submissions which are failed.

### SMS CLI :umbrella:

CLI commands to manipulate sms client and sms server.

## License

Copyright &copy; 2016-2019, Perilla Roc.

`nwpc-nost` is licensed under [GPL-3.0](#).

[GPL-3.0]: http://www.gnu.org/licenses/gpl-3.0.en.html
