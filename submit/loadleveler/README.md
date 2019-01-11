# llsubmit2 / llsubmit4

SMS 作业提交脚本

## 简介

llsubmit2 和 llsubmit4 脚本用于将 SMS (Supervisor Monitoring Scheduler) 业务系统调度软件中的作业脚本提交到 [LoadLeveler](#) 中。

针对 IBM 服务器中 LoadLeveler 的不稳定情况，进行诸多优化。

## 安装

llsubmit2 和 llsubmit4 脚本目前仅在 IBM AIX 系统中测试过。另外，系统中需要安装 python。

将脚本拷贝到 SMS 服务器可以访问的目录，建议拷贝到 `$HOME/bin` 目录下，并将该目录添加到 PATH 环境变量中。

```bash
export PATH=$HOME/bin:$PATH
```

## 配置

脚本需要使用环境变量 `WORKDIR`，如果尚未设置，请在 profile 中设置或替换脚本中的 `WORKDIR` 变量。

请检查 sms 服务器的名称 `nameofsms`。默认名称与用户名有关，见下表：

用户名 | SMS 服务器名 |
------------ | ------------- |
nwp | nwpc_op |
nwp_qu | nwpc_qu |
nwp_sp | nwpc_nwp_sp |
nwp_ex | nwpc_ex |
nwp_xp | nwpc_xp | |
nwpc_pd | nwpc_pd |
其它用户 | nwpc_$USER |

如果 sms 服务器名称不符合默认设置，请修改源码，设置 nameofsms 值。

## 使用

### llsubmit2

```bash
llsubmit2 %SMSJOB% %SMSNAME% [%SMSJOBOUT%]
```

各参数均为SMS变量，含义如下：

  * `SMSJOB`：任务脚本路径
  * `SMSNAME`：SMS中节点的路径
  * `SMSJOBOUT`：重定向标准输出的文件，默认将 SMSJOB 的 `*.job[0-9]` 替换为 `*.[0-9]`

使用示例

```bash
llsubmit2 /cma/g1/nwp/SMSOUT/gmf_gsi_v1r5/T639/00/prods/micaps_base/base_156.job1 \
    /gmf_gsi_v1r5/T639/00/prods/micaps_base/base_156 \
    /gmf_gsi_v1r5/T639/00/prods/micaps_base/base_156.1
```

### llsubmit4

```bash
llsubmit4 %SMSJOB% %SMSNAME% %SMSTRIES% %SMSTRYNO% 
```

各参数均为SMS变量，含义如下：

  * `SMSJOB`：任务脚本路径
  * `SMSNAME`：SMS中节点的路径
  * `SMSTRIES`：自动重复提交的次数
  * `SMSTRYNO`：当前提交次数

使用示例

```bash
llsubmit4 /cma/g1/nwp/SMSOUT/gmf_gsi_v1r5/T639/00/prods/micaps_base/base_156.job1 \
    /gmf_gsi_v1r5/T639/00/prods/micaps_base/base_156 2 1
```

### 在SMS中使用

将 SMS 任务的 `SMSCMD` 变量设为上面的命令，覆盖默认的任务运行命令。

## 功能

### 检测提交状态

提交成功时，将 [LoadLeveler](#) 的作业号保存到 SMS 任务的 `SMSRID` 变量。

提交失败时，`llsubmit2` 将 SMS 任务设为 aborted 状态，`llsubmit4` 根据设置自动重新提交脚本。

### 延迟提交

提供自动延时提交功能，避免同一时刻提交大量作业导致 LoadLeveler 服务无法响应的情况。

`llsubmit4` 脚本会根据重复提交次数，修改延迟提交时间窗。

### 日志

llsubmit4 提供下列日志：

  * 提交日志：llsubmit4.submit.log
  * 错误日志：llsubmit4.error.log
  * 调试日志：llsubmit4.submit.log

默认放在 `$WORKDIR/sublog`

## 后续开发

使用 [ecflow](#) 替代 sms 已基本敲定，后续将开发 ecflow 的作业提交脚本。

## 致谢

本项目在已有 `llsubmit2` 脚本基础上开发，特此向其开发者表示敬意。

在开发过程中受到多位同事的指导，感谢他们提供的诸多建议。

[ecflow]: https://software.ecmwf.int/wiki/display/ECFLOW/Home
[LoadLeveler]: http://www.ibm.com/systems/power/software/loadleveler/