<div align="center">

<img src=".github/assets/slurm-logo.svg" height="262px" width="240px">

A snap package for the Slurm workload manager - a 
highly scalable cluster management and job scheduling system for 
large and small Linux clusters. Slurm is used by many of the world's 
supercomputers and computer clusters.

</div>

> This snap is currently experimental; it is not complete and will likely not work as
> I am still developing it. Right now this repository is the staging ground for all
> my hacking and wacking on Slurm. If you're interested in the development of
> this snap - and want to contribute - please reach out to me on the 
> [Ubuntu HPC Matrix space](https://matrix.to/#/#ubuntu-hpc:matrix.org).

## Building the Slurm snap

Want to build and test the Slurm snap locally without pulling from the Snap Store? 
Use the following commands to build and install the Slurm snap on your system. 
These instructions assume that you are running on a Linux distribution that supports 
installing snap packages. Please see [this page](https://snapcraft.io/docs/installing-snapd) 
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

## License

The Slurm snap is free software, distributed under the Apache Software License, 
version 2.0. See [LICENSE](./LICENSE) for more information. Slurm itself is licensed
under the GNU General Public License, version 2, or any later version. See Slurm's
[legal notice](https://slurm.schedmd.com/disclaimer.html) for further licensing 
information about Slurm itself.