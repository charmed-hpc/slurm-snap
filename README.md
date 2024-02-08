<div align="center">

<img src=".github/assets/slurm-logo.svg" height="262px" width="240px">

A snap package for the Slurm workload manager - a 
highly scalable cluster management and job scheduling system for 
large and small Linux clusters. Slurm is used by many of the world's 
supercomputers and computer clusters.

</div>

> This snap is currently experimental. If you're interested in the development of
> this snap - and want to contribute - please reach out to me on the 
> [Ubuntu HPC Matrix space](https://matrix.to/#/#ubuntu-hpc:matrix.org).

## Features

Slurm is a workload manager designed for supercomputers. It is scalable, highly
configurable, and supports scheduling for generic computational resources such as
GPUs. This snap package includes:

* `munged`: The daemon responsible for authenticating local MUNGE clients and servicing
  their credential encode & decode requests.
* `slurmctld`: The central management daemon of Slurm.
* `slurmd`: The compute node daemon of Slurm.
* `slurmdbd`: The Slurm database daemon. Provides an interface to a database for Slurm.
* `slurmrestd`: The Slurm REST API daemon. Provides an interface to Slurm via a REST API.
* The command line applications used to interface with both Slurm and MUNGE.
* A configuration API for dynamically configuring various Slurm functionality.

## Usage

### Configuration

Slurm is a highly configurable workload manager. The Slurm snap can be configured using 
`snap set slurm ...`. See the list below for all the possible configuration options
you can set on the snap:

#### slurm

Configuration options related to the Slurm workload manager. Please refer to the 
[_parameters_ section of the _slurm.conf_ configuration file](https://manpages.ubuntu.com/manpages/noble/en/man5/slurm.conf.5.html#parameters) 
manual page for an in-depth description of each configuration option and how it modifies the behaviour of Slurm.

* `account-storage-external-host`
* `accounting-storage-backup-host`
* `accounting-storage-enforce`
* `accounting-storage-host`
* `accounting-storage-parameters` 
* `accounting-storage-pass`
* `accounting-storage-port`
* `accounting-storage-tres`
* `accounting-storage-type`
* `accounting-storage-user`
* `accounting-store-flags`
* `acct-gather-energy-type`
* `acct-gather-filesystem-type`
* `acct-gather-interconnect-type`
* `acct-gather-node-freq`
* `acct-gather-profile-type`
* `allow-spec-resources-usage`
* `auth-alt-parameters`
* `auth-alt-types`
* `auth-info`
* `auth-type`
* `batch-start-timeout`
* `bcast-exclude`
* `bcast-parameters`
* `burst-buffer-type`
* `cli-filter-plugins`
* `cluster-name`
* `communication-parameters`
* `complete-wait`
* `core-spec-plugin`
* `cpu-freq-def`
* `cpu-freq-governors`
* `cred-type`
* `debug-flags`
* `def-cpu-per-gpu`
* `def-mem-per-cpu`
* `def-mem-per-gpu`
* `def-mem-per-node`
* `dependency-parameters`
* `disable-root-jobs`
* `eio-timeout`
* `enforce-part-limits`
* `epilog`
* `epilog-msg-time`
* `epilog-slurmctld`
* `ext-sensors-freq`
* `ext-sensors-type`
* `fair-share-dampening-factor`
* `federation-parameters`
* `first-job-id`
* `get-env-timeout`
* `gpu-freq-def`
* `gres-types`
* `group-update-force`
* `group-update-time`
* `health-check-interval`
* `health-check-node-state`
* `health-check-program`
* `inactive-limit`
* `include`
* `interactive-step-options`
* `job-acct-gather-frequency`
* `job-acct-gather-params`
* `job-acct-gather-type`
* `job-comp-host`
* `job-comp-loc`
* `job-comp-params`
* `job-comp-pass`
* `job-comp-port`
* `job-comp-type`
* `job-comp-user`
* `job-container-type`
* `job-file-append`
* `job-requeue`
* `job-submit-plugins`
* `kill-on-bad-exit`
* `kill-wait`
* `launch-parameters`
* `licenses`
* `log-time-format`
* `mail-domain`
* `mail-prog`
* `max-array-size`
* `max-batch-requeue`
* `max-job-count`
* `max-job-id`
* `max-mem-per-cpu`
* `max-mem-per-node`
* `max-node-count`
* `max-step-count`
* `max-tasks-per-node`
* `mcs-parameters`
* `mcs-plugin`
* `message-timeout`
* `min-job-age`
* `mpi-default`
* `mpi-params`
* `node-features-plugins`
* `over-time-limit`
* `plug-stack-config`
* `plugin-dir`
* `power-parameters`
* `power-plugin`
* `preempt-exempt-time`
* `preempt-mode`
* `preempt-parameters`
* `preempt-type`
* `prep-parameters`
* `prep-plugins`
* `priority-calcp-period`
* `priority-decay-half-life`
* `priority-favor-small`
* `priority-flags`
* `priority-max-age`
* `priority-parameters`
* `priority-site-factor-parameters`
* `priority-site-factor-plugin`
* `priority-type`
* `priority-usage-reset-period`
* `priority-weight-age`
* `priority-weight-assoc`
* `priority-weight-fair-share`
* `priority-weight-job-size`
* `priority-weight-partition`
* `priority-weight-qos`
* `priority-weight-tres`
* `private-data`
* `proctrack-type`
* `prolog`
* `prolog-epilog-timeout`
* `prolog-flags`
* `prolog-slurmctld`
* `propagate-prio-process`
* `propagate-resource-limits`
* `propagate-resource-limits-except`
* `reboot-program`
* `reconfig-flags`
* `requeue-exit`
* `requeue-exit-hold`
* `resume-fail-program`
* `resume-program`
* `resume-rate`
* `resume-timeout`
* `resv-epilog`
* `resv-over-run`
* `resv-prolog`
* `return-to-service`
* `route-plugin`
* `scheduler-parameters`
* `scheduler-time-slice`
* `scheduler-type`
* `scron-parameters`
* `select-type`
* `select-type-parameters`
* `slurm-sched-log-file`
* `slurm-sched-log-level`
* `slurm-user`
* `slurmctld-addr`
* `slurmctld-debug`
* `slurmctld-host`
* `slurmctld-log-file`
* `slurmctld-parameters`
* `slurmctld-pid-file`
* `slurmctld-port`
* `slurmctld-primary-off-prog`
* `slurmctld-primary-on-prog`
* `slurmctld-syslog-debug`
* `slurmctld-timeout`
* `slurmd-debug`
* `slurmd-log-file`
* `slurmd-parameters`
* `slurmd-pid-file`
* `slurmd-port`
* `slurmd-spool-dir`
* `slurmd-syslog-debug`
* `slurmd-timeout`
* `slurmd-user`
* `srun-epilog`
* `srun-port-range`
* `srun-prolog`
* `state-save-location`
* `suspend-exc-nodes`
* `suspend-exc-parts`
* `suspend-exc-states`
* `suspend-program`
* `suspend-rate`
* `suspend-time`
* `suspend-timeout`
* `switch-parameters`
* `switch-type`
* `task-epilog`
* `task-plugin`
* `task-plugin-param`
* `task-prolog`
* `tcp-timeout`
* `tmp-fs`
* `topology-param`
* `topology-plugin`
* `track-wc-key`
* `tree-width`
* `unkillable-step-program`
* `unkillable-step-timeout`
* `use-pam`
* `vsize-factor`
* `wait-time`
* `x11-parameters`

##### Nodes

Configuration options related to compute nodes. Please refer to the 
[_node configuration_ section of the _slurm.conf_ configuration file](https://manpages.ubuntu.com/manpages/noble/en/man5/slurm.conf.5.html#node%20configuration) 
manual page for an in-depth description of each configuration option 
and how it modifies the behaviour of compute nodes.

* `nodes.<node-name>.bcast-addr`
* `nodes.<node-name>.boards`
* `nodes.<node-name>.core-spec-count`
* `nodes.<node-name>.cores-per-socket`
* `nodes.<node-name>.cpu-bind`
* `nodes.<node-name>.cpu-spec-list`
* `nodes.<node-name>.cpus`
* `nodes.<node-name>.features`
* `nodes.<node-name>.gres`
* `nodes.<node-name>.mem-spec-limit`
* `nodes.<node-name>.node-addr`
* `nodes.<node-name>.node-hostname`
* `nodes.<node-name>.node-name`
* `nodes.<node-name>.port`
* `nodes.<node-name>.procs`
* `nodes.<node-name>.real-memory`
* `nodes.<node-name>.reason`
* `nodes.<node-name>.sockets`
* `nodes.<node-name>.sockets-per-board`
* `nodes.<node-name>.state`
* `nodes.<node-name>.threads-per-core`
* `nodes.<node-name>.tmp-disk`
* `nodes.<node-name>.weight`

##### Frontend Nodes

Configuration options related to frontend compute nodes. Please refer to the
[_frontend node configuration_ section of the _slurm.conf_ configuration file](https://manpages.ubuntu.com/manpages/noble/en/man5/slurm.conf.5.html#frontend%20node%20configuration)
manual page for an in-depth description of each configuration option 
and how it modifies the behaviour of frontend compute nodes.

* `frontend-nodes.<frontend-node-name>.allow-groups`
* `frontend-nodes.<frontend-node-name>.allow-users`
* `frontend-nodes.<frontend-node-name>.deny-groups`
* `frontend-nodes.<frontend-node-name>.deny-users`
* `frontend-nodes.<frontend-node-name>.frontend-addr`
* `frontend-nodes.<frontend-node-name>.frontend-name`
* `frontend-nodes.<frontend-node-name>.port`
* `frontend-nodes.<frontend-node-name>.reason`
* `frontend-nodes.<frontend-node-name>.state`

##### Down Nodes

Configuration options related to down compute nodes. Please refer to the
[_down node configuration_ section of the _slurm.conf_ configuration file](https://manpages.ubuntu.com/manpages/noble/en/man5/slurm.conf.5.html#down%20node%20configuration)
manual page for an in-depth description of each configuration option 
and how it modifies the behaviour of compute nodes.

* `down-nodes.nodes`
* `down-nodes.reason`
* `down-nodes.state`

##### Node Sets

Configuration options related to node sets. Please refer to the
[_nodeset configuration_ section of the _slurm.conf_ configuration file](https://manpages.ubuntu.com/manpages/noble/en/man5/slurm.conf.5.html#nodeset%20configuration)
manual page for an in-depth description of each configuration option 
and how it modifies the behaviour of node sets.

* `node-sets.<node-set>.feature`
* `node-sets.<node-set>.nodes`

##### Partitions

Configuration options related to partitions. Please refer to the
[_partition configuration_ section of the _slurm.conf_ configuration file](https://manpages.ubuntu.com/manpages/noble/en/man5/slurm.conf.5.html#partition%20configurationn)
manual page for an in-depth description of each configuration option 
and how it modifies the behaviour of partitions.

* `partitions.<partition-name>.alloc-nodes`
* `partitions.<partition-name>.allow-accounts`
* `partitions.<partition-name>.allow-groups`
* `partitions.<partition-name>.allow-qos`
* `partitions.<partition-name>.alternate`
* `partitions.<partition-name>.cpu-bind`
* `partitions.<partition-name>.def-cpu-per-gpu`
* `partitions.<partition-name>.def-mem-per-cpu`
* `partitions.<partition-name>.def-mem-per-gpu`
* `partitions.<partition-name>.def-mem-per-node`
* `partitions.<partition-name>.default`
* `partitions.<partition-name>.default-time`
* `partitions.<partition-name>.deny-accounts`
* `partitions.<partition-name>.deny-qos`
* `partitions.<partition-name>.disable-root-jobs`
* `partitions.<partition-name>.exclusive-user`
* `partitions.<partition-name>.grace-time`
* `partitions.<partition-name>.hidden`
* `partitions.<partition-name>.lln`
* `partitions.<partition-name>.max-cpus-per-node`
* `partitions.<partition-name>.max-cpus-per-socket`
* `partitions.<partition-name>.max-mem-per-cpu`
* `partitions.<partition-name>.max-mem-per-node`
* `partitions.<partition-name>.max-nodes`
* `partitions.<partition-name>.max-time`
* `partitions.<partition-name>.min-nodes`
* `partitions.<partition-name>.nodes`
* `partitions.<partition-name>.over-subscribe`
* `partitions.<partition-name>.over-time-limit`
* `partitions.<partition-name>.partition-name`
* `partitions.<partition-name>.power-down-on-idle`
* `partitions.<partition-name>.preempt-mode`
* `partitions.<partition-name>.priority-job-factor`
* `partitions.<partition-name>.priority-tier`
* `partitions.<partition-name>.qos`
* `partitions.<partition-name>.req-resv`
* `partitions.<partition-name>.resume-timeout`
* `partitions.<partition-name>.root-only`
* `partitions.<partition-name>.select-type-parameters`
* `partitions.<partition-name>.state`
* `partitions.<partition-name>.suspend-time`
* `partitions.<partition-name>.suspend-timeout`
* `partitions.<partition-name>.tres-billing-weights`

#### munge

* `munge.key`
  * Set the _munge.key_ secret use by the `munged` daemon to authenticate hosts.
* `munge.max-thread-count`
  * Set the maximum number of threads that `munged` can spawn for processing authentication requests.

#### slurmd

* `slurmd.config-server`
  * Set configuration server for `slurmd`. Required when running `slurmd` in  configless mode.
    The daemon will download the _slurm.conf_ configuration file from the primary control server.

#### slurmdbd

Configuration options related to the `slurmdbd` daemon. Please refer to the
[_slurmdbd.conf_ configuration file](https://manpages.ubuntu.com/manpages/noble/en/man5/slurmdbd.conf.5.html)
manual page for an in-depth description of each configuration option 
and how it modifies the behaviour of the `slurmdbd` daemon.

* `slurmd.archive-dir`
* `slurmd.archive-events`
* `slurmd.archive-jobs`
* `slurmd.archive-resvs`
* `slurmd.archive-script`
* `slurmd.archive-steps`
* `slurmd.archive-suspend`
* `slurmd.archive-txn`
* `slurmd.archive-usage`
* `slurmd.auth-alt-parameters`
* `slurmd.auth-alt-types`
* `slurmd.auth-info`
* `slurmd.auth-type`
* `slurmd.commit-delay`
* `slurmd.communication-parameters`
* `slurmd.dbd-addr`
* `slurmd.dbd-backup-host`
* `slurmd.dbd-host`
* `slurmd.dbd-port`
* `slurmd.debug-flags`
* `slurmd.debug-level`
* `slurmd.debug-level-syslog`
* `slurmd.default-qos`
* `slurmd.log-file`
* `slurmd.log-time-format`
* `slurmd.max-query-time-range`
* `slurmd.message-timeout`
* `slurmd.parameters`
* `slurmd.pid-file`
* `slurmd.plugin-dir`
* `slurmd.private-data`
* `slurmd.purge-event-after`
* `slurmd.purge-job-after`
* `slurmd.purge-resv-after`
* `slurmd.purge-step-after`
* `slurmd.purge-suspend-after`
* `slurmd.purge-txn-after`
* `slurmd.purge-usage-after`
* `slurmd.slurm-user`
* `slurmd.storage-backup-host`
* `slurmd.storage-host`
* `slurmd.storage-loc`
* `slurmd.storage-parameters`
* `slurmd.storage-pass`
* `slurmd.storage-port`
* `slurmd.storage-type`
* `slurmd.storage-user`
* `slurmd.tcp-timeout`
* `slurmd.track-slurmctld-down`
* `slurmd.track-wc-key`

#### slurmrestd

* `slurmrestd.max-connections`
  * Set the maximum number of connections to process at one time.
* `slurmrestd.max-thread-count`
  * Set the maximum number of threads to spawn for processing client connections.

## Building the Slurm snap

Want to build and test the Slurm snap locally without pulling from the Snap Store?
Want to bundle in your own custom Slurm plugins? Use the following commands to build 
and install the Slurm snap on your system. These instructions assume that you are 
running on a Linux distribution that supports installing snap packages. 
Please see [this page](https://snapcraft.io/docs/installing-snapd) 
for a list of Linux distributions that support using snap packages.

### Clone Repository

```
git clone git@github.com:NucciTheBoss/slurm-snap.git
cd slurm-snap
```

### Installing and Configuring Prerequisites

```
sudo snap install lxd
sudo lxd init --minimal
sudo snap install snapcraft --classic
```

### Packing and Installing the Snap

```
snapcraft
sudo snap install ./slurm*.snap --dangerous --classic
```

## Project & Community

The Slurm workload manager snap package is a project of the Ubuntu HPC community. It is
an open source project that is welcome to community involvement, contributions, suggestions,
fixes, and constructive feedback. Interested in being involved with the development of
this snap package? Check out the links below:

* [Join our online chat](https://matrix.to/#/#hpc:ubuntu.com)
* [Contributing guidelines](./CONTRIBUTING.md)
* [Snap & Snapcraft documentation](https://snapcraft.io/docs)
* [Code of Conduct](https://ubuntu.com/community/ethos/code-of-conduct)

## License

The Slurm snap is free software, distributed under the Apache Software License, 
version 2.0. See [LICENSE](./LICENSE) for more information. The Slurm workload manager
itself is licensed  under the GNU General Public License, version 2, or any later version. 
See Slurm's [legal notice](https://slurm.schedmd.com/disclaimer.html) for further 
licensing information about Slurm itself.