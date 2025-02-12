# Security policy

## Supported versions

Security updates for the Slurm snap will be released after vulnerabilities have been identified and fixed to
the `latest/candidate` and `latest/stable` release channels.

## Reporting a vulnerability

Please provide a description of the issue, the steps you took to create the issue, affected versions, and, if known,
mitigations for the issue.

The preferred way to report a security issue is through [GitHub Security Advisories][gsa]. See
[Privately reporting a security vulnerability][how-to-sec-vuln] for instructions on how to report a security vulnerability
using GitHub's security advisory feature.

[gsa]: https://github.com/charmed-hpc/slurm-snap/security/advisories/new
[how-to-sec-vuln]: https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability

You may also send email to [security@ubuntu.com](mailto:security@ubuntu.com). Email may optionally be encrypted to OpenPGP
key [4072 60F7 616E CE4D 9D12 4627 98E9 740D C345 39E0][pgp-key].

[pgp-key]: https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x407260f7616ece4d9d12462798e9740dc34539e0

The Charmed HPC core developer team will be notified of the issue and will work with you to determine whether the issue
qualifies as a security issue and, if so, in which component. We will then figure out a fix, get a CVE assigned, and
coordinate the release of the fix.

If you have a deadline for public disclosure, please let us know. Our vulnerability management team intends to respond
within 3 working days of your report. This project aims to resolve all vulnerabilities within 90 days.

The [Ubuntu Security disclosure and embargo policy](https://ubuntu.com/security/disclosure-policy) contains more
information about how can contact us, what you can expect when you contact us, and what we expect from you.
