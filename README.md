# Slurm snap

[![CI](https://github.com/charmed-hpc/slurm-snap/actions/workflows/ci.yaml/badge.svg)](https://github.com/charmed-hpc/slurm-snap/actions/workflows/ci.yaml)
[![Release](https://github.com/charmed-hpc/slurm-snap/actions/workflows/release-to-candidate.yaml/badge.svg?branch=main)](https://github.com/charmed-hpc/slurm-snap/actions/workflows/release-to-candidate.yaml)
![GitHub License](https://img.shields.io/github/license/charmed-hpc/slurm-snap)
[![Matrix](https://img.shields.io/matrix/ubuntu-hpc%3Amatrix.org?logo=matrix&label=ubuntu-hpc)](https://matrix.to/#/#hpc:ubuntu.com)

An all-in-one snap package for the [Slurm workload manager](https://slurm.schedmd.com).

Slurm is used by many of the world's supercomputers and computer clusters. It is a
highly scalable cluster management and job scheduling system for large and small
Linux clusters. It is scalable, highly configurable, and supports scheduling for
generic computational resources such as GPUs. This snap package includes:

* `munged`: The daemon responsible for authenticating local MUNGE clients and servicing
  their credential encode & decode requests.
* `mungectl`: A command line tool for getting, setting, and generating MUNGE munge keys.
* `slurmctld`: The central management daemon of Slurm.
* `slurmd`: The compute node daemon of Slurm.
* `slurmdbd`: The Slurm database daemon. Provides an interface to a database for Slurm.
* `slurmrestd`: The Slurm REST API daemon. Provides an interface to Slurm via a REST API.
* The MUNGE and Slurm CLI commands
* A CLI-based configuration API for configuring Slurm.

## ✨ Getting started

### Installing the Slurm snap

The latest, stable version of the Slurm snap can installed using the following command:

```shell
sudo snap install slurm --classic
```

### Manage the munge key

`mungectl` can be used to manage the _munge.key_ file inside the Slurm snap:

```shell
slurm.mungectl key generate               # Generate new munge key file.
slurm.mungectl key get                    # Get munge key file as base64-encoded string.
cat new.key.b64 | slurm.mungectl key set  # Set new munge key using base64-encoded key.
```

### Configuring Slurm

Slurm configuration files such as _slurm.conf_ and _slurmdbd.conf_ can be found
under the `/var/snap/slurm/common/etc/slurm` directory. Files in this directory
can be edited directly to configure your Slurm deployment.

Some of the services provided by the Slurm snap can be configured by using the
`snap set slurm ...` command. See the sections below for the service options that
can be modified using `snap`:

#### munge

* `munged.max-thread-count`
  * Set the maximum number of threads that `munged` can spawn for processing authentication requests.

#### slurmd

* `slurmd.config-server`
  * Set configuration server for `slurmd`. Required when running `slurmd` in  configless mode.
    The daemon will download the _slurm.conf_ configuration file from the primary control server.

#### slurmrestd

* `slurmrestd.max-connections`
  * Set the maximum number of connections to process at one time.
* `slurmrestd.max-thread-count`
  * Set the maximum number of threads to spawn for processing client connections.

## 🤔 What's next?

If you want to learn more about all the things you can do with the Slurm snap, here are some further resources for you to explore:

* [Open an issue](https://github.com/charmed-hpc/slurm-snap/issues)
* [Ask a question on GitHub](https://github.com/orgs/charmed-hpc/discussions)

## 🛠️ Development

We use [just](https://just.systems) as the command runner for this project.
The project's [justfile](./justfile) provides some useful recipes that will definitely help
you while you're hacking on the Slurm snap:

```shell
just snap  # Build snap
just fmt   # Apply formatting standards to project
just lint  # Check project against coding style standards
just unit  # Run unit tests
```

To run the integration tests for the Slurm snap, you'll need to have both
[LXD](https://ubuntu.com/lxd) and [gambol](https://snapcraft.io/gambol) installed on your machine:

```shell
just integration  # Run integration tests
```

If you're interested in contributing your work to the Slurm snap, take a look at our
[contributing guidelines](./CONTRIBUTING.md) for further details.

## 🤝 Project and community

The Slurm snap a project of the [Ubuntu High-Performance Computing community](https://ubuntu.com/community/governance/teams/hpc).
Interested in contributing bug fixes, new editors, documentation, or feedback? Want to join the Ubuntu HPC community? You’ve come to the right place 🤩

Here’s some links to help you get started with joining the community:

* [Ubuntu Code of Conduct](https://ubuntu.com/community/ethos/code-of-conduct)
* [Contributing guidelines](./CONTRIBUTING.md)
* [Join the conversation on Matrix](https://matrix.to/#/#hpc:ubuntu.com)
* [Get the latest news on Discourse](https://discourse.ubuntu.com/c/hpc/151)
* [Ask and answer questions on GitHub](https://github.com/orgs/charmed-hpc/discussions/categories/q-a)

## 📋 License

The Slurm snap is free software, distributed under the Apache Software License,
version 2.0. See the [Apache-2.0 LICENSE](./LICENSE) file for further details.
The Slurm workload manager itself is licensed  under the GNU General Public License,
version 2, or any later version. See Slurm's [legal notice](https://slurm.schedmd.com/disclaimer.html) for further
licensing information about Slurm itself.
