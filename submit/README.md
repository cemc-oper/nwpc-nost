# llsubmt2 / llsubmi4

SMS作业提交脚本

## 简介

用于在 SMS 业务系统调度软件中，将作业脚本提交到 LoadLeveler 中。针对 HPC 中 LoadLeveler 的不稳定情况，进行诸多优化。

检测提交是否成功：

* 提交成功时，将 loadleveler 的作业号保存到 SMS 任务的 SMSRID 变量；
* 提交失败时，llsubmit2 将 SMS 任务设为 aborted 状态，llsubmit4 根据设置自动重新提交脚本。

提供自动延时提交功能，避免同一时刻提交大量作业。

## 环境

本项目目前仅支持从 SMS 提交任务到 LoadLeveler 中。另外，系统中需要安装 python。

## 安装和配置

将脚本拷贝到 SMS 服务器可以访问的目录，建议拷贝到 $HOME/bin 目录下，并将该目录添加到 PATH 环境变量中。

~~~
export PATH=$HOME/bin:$PATH
~~~

脚本需要使用环境变量 WORKDIR，如果尚未设置，请在 profile 中设置或替换脚本中的 WORKDIR 变量。

请检查 sms 服务器的名称 nameofsms。默认名称与用户名有关，见下表：

用户名 | SMS 服务器名
------------ | -------------
nwp | nwpc_op
nwp_qu | nwpc_qu
nwp_sp | nwpc_nwp_sp
nwp_ex | nwpc_ex
nwp_xp | nwpc_xp
nwpc_pd | nwpc_pd
其它用户 | nwpc_$USER

如果 sms 服务器名称不符合默认设置，请修改源码，设置 nameofsms 值。

## 使用

### llsubmit2

~~~
llsubmit2 %SMSJOB% %SMSNAME% [%SMSJOBOUT%]
~~~

### llsubmit4

~~~
llsubmit4 %SMSJOB% %SMSNAME% %SMSTRIES% %SMSTRYNO% 
~~~

## 日志

llsubmit4 提供下列日志：

* 提交日志：llsubmit4.submit.log
* 错误日志：llsubmit4.error.log
* 调试日志：llsubmit4.submit.log

默认放在 $WORKDIR/sublog

## 后续开发

使用 ecflow 替代 sms 已基本敲定，后续将开发 ecflow 的作业提交脚本。

## 致谢

本项目在已有 llsubmit2 脚本基础上开发，特此向其开发者表示敬意。

在开发过程中收到多位同事的指导，感谢他们提供的诸多建议。
