nwpc-operation-system-tool
=====

NWPC operation system tool suite, including such components:

* A job submission script using in SMS.
* CLI commands used to manipulate SMS client and SMS server.

Introduction
----

### Slurm Client :sunny:

A CLI client for Slurm in NWPC.

### LoadLeveler Client :sunny:

A CLI client for LoadLeveler in NWPC.

Please refer to `README.md` in each component's directory for detailed introductions.

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

License
-------

Copyright &copy; 2016-2018, Perilla Roc.

`nwpc-operation-system-tool` is licensed under [GPL-3.0](#).

[GPL-3.0]: http://www.gnu.org/licenses/gpl-3.0.en.html
