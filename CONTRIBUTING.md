# Contributing to the Slurm workload manager snap

Do you have something that you wish to contribute to the Slurm workload manager snap? __If so, here is how you can help!__

Please take a moment to review this document so that the contribution process will be easy and effective for everyone
involved. Also, please familiarise yourself with the [Snap & Snapcraft documentation](https://snapcraft.io/docs) as it will help 
you better understand how the Slurm workload manager snap works and is developed.

Following these guidelines helps you communicate that you respect the developers managing and developing the Slurm workload manager snap. 
In return, they should reciprocate that respect while they are addressing your issue or assessing your submitted 
patches and features.

Have any questions? Feel free to ask them in the [Ubuntu HPC Matrix space](https://matrix.to/#/#ubuntu-hpc:matrix.org).

### Table of Contents

* [Using the issue tracker](#using-the-issue-tracker)
* [Issues and Labels](#issues-and-labels)
* [Bug Reports](#bug-reports)
* [Feature Requests](#feature-requests)
* [Pull Requests](#pull-requests)
* [Discussions](#discussions)
* [Code Guidelines](#code-guidelines)
* [License](#license)

## Using the issue tracker

The issue tracker is the preferred way for tracking [bug reports](#bug-reports), [feature requests](#feature-requests),
and [submitted pull requests](#pull-requests), but please follow these guidelines for the issue tracker:

* Please __do not__ use the issue tracker for personal issues and/or support requests. 
The [Discussions](#discussions) page is a better place to get help for personal support requests.

* Please __do not__ derail or troll issues. Keep the discussion on track and have respect for the other 
users/contributors of the Slurm workload manager snap.

* Please __do not__ post comments consisting solely of "+1", ":thumbsup:", or something similar. 
Use [GitHub's "reactions" feature](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) 
instead.
  * The maintainers of the Slurm workload manager snap reserve the right to delete comments that violate this rule.

* Please __do not__ repost or reopen issues that have been closed. Please either 
submit a new issue or browser through previous issues.
  * The maintainers of the Slurm workload manager snap reserve the right to delete issues that violate this rule.

## Issues and Labels

The Slurm workload manager snap issue tracker uses a variety of labels to help organize and identify issues. 
Here is a list of some of these labels, and how the maintainers of the Slurm workload manager snap use them:

* `Type: Bug` - Issues reported in the Slurm workload manager snap source code that either produce errors or unexpected behavior.

* `Status: Confirmed` - Issues marked `Type: Bug` that have be confirmed to be reproducible on a separate system.

* `Type: Documentation` - Issues for improving or updating the Slurm workload manager snap's documentation. 
Can also be used for pull requests.

* `Type: Refactor` - Issues that pertain to improving the existing the Slurm workload manager snap code base.

* `Type: Idea Bank` - Issues that pertain to proposing potential improvement to the Slurm workload manager snap.

* `Type: Enhancement` - Issues marked as an agreed upon enhancement to the Slurm workload manager snap. Can also be used for pull requests.

* `Statues: Help wanted` - Issues where we need help from the greater the Slurm workload manager snap community to solve.

For a complete look at the Slurm workload manager snap's labels, see the 
[project labels page](https://github.com/charmed-hpc/slurm-snap/labels).

## Bug Reports

A bug is a *demonstrable problem* that is caused by the Slurm workload manager snap. Good bug reports make the Slurm workload manager snap more robust, so thank 
you for taking the time to report issues in the source code!

Guidelines for reporting bugs in the Slurm workload manager snap:

1. __Validate your code__ &mdash; ensure that your issue is not being caused by either a semantic or syntactic 
error in your own code.

2. __Use the GitHub issue search__ &mdash; check if the issue you are encountering has already been reported by 
someone else.

3. __Check if the issue has already been fixed__ &mdash; try to reproduce your issue using the latest `main` 
in the Slurm workload manager snap repository.

4. __Isolate the problem__ &mdash; the more pinpointed the issue is, the easier time the Slurm workload manager snap developers 
will have fixing it.

A good bug report should not leave others needing to chase you for more information. 
Please try to be as detailed as possible in your report. What is your environment? What steps will reproduce the issue? 
What operating system are you experiencing the problem on? Have you had the same results on a different 
operating system? What would you expect to be the outcome? All these details will help the developers fix any 
potential bugs.

## Feature Requests

All feature requests should be posted to GitHub Discussions and tagged as `Type: Idea Bank`. The maintainers of
the Slurm workload manager snap already know the features they want to incorporate into the Slurm workload manager snap, but they are always open to 
new ideas and potential improvements. GitHub Discussions is the best place to post these types of requests 
because it allows for feedback from the entire community and does not bloat the issue tracker. Please note that not 
all feature requests will be incorporated into the Slurm workload manager snap. Also, feature requests posted on the issue tracker 
will be tagged as `Type: Invalid` and closed. Lastly, please note that spamming the maintainers to incorporate a
feature you want into the Slurm workload manager snap will not improve its likelihood of being implemented; it may result in you receiving
a temporary ban from the repository.

## Pull Requests

Good pull requests &mdash; patches, improvements, new features &mdash; are a huge help. These pull requests should 
remain focused in scope and should not contain unrelated commits.

__Ask first__ before embarking on any __significant__ pull request (e.g. implementing new features, refactoring code, 
incorporating a new test environment provider, etc.), otherwise you risk spending a lot of time working on something 
that the Slurm workload manager snap's developers might not want to merge into the project! For trivial things, or things that do not require 
a lot of your time, you can go ahead and make a pull request.

Adhering to the following process is the best way to get your work
included in the project:

1. [Fork](https://help.github.com/articles/fork-a-repo/) the project, clone your fork,
   and configure the remotes:

   ```bash
   # Clone your fork of the repo into the current directory
   git clone https://github.com/<your-username>/slurm-snap.git
   # Navigate to the newly cloned directory
   cd slurm-snap
   # Assign the original repo to a remote called "upstream"
   git remote add upstream https://github.com/charmed-hpc/slurm-snap.git
   ```

2. If you cloned a while ago, pull the latest changes from the upstream the Slurm workload manager snap repository:

   ```bash
   git checkout main
   git pull upstream main
   ```

3. Create a new topic branch (off the main project development branch) to
   contain your feature, change, or fix:

   ```bash
   git checkout -b <topic-branch-name>
   ```

4. Ensure that your changes pass all tests:

    ```bash
    tox run -e fmt
    tox run -e lint
    ```

5. Commit your changes in logical chunks. Our project follows the 
   [Conventional Commits specification, version 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
   Conventional commits create an explicit commit history; the make it easier for operators
   and external contributors to quickly identify specific commits and understand what was changed.
   Please follow the Conventional Commits specification when authoring your commits or
   your code will unlikely be merged into the main project without. Asked to clean up your
   commits by a slurm-snap maintainer? No problem! You can use Git's
   [interactive rebase](https://help.github.com/articles/about-git-rebase/) feature to 
   tidy up your commits before making them public.

6. Locally merge (or rebase) the upstream development branch into your topic branch:

   ```bash
   git pull [--rebase] upstream main
   ```

7. Push your topic branch up to your fork:

   ```bash
   git push origin <topic-branch-name>
   ```

8. [Open a Pull Request](https://help.github.com/articles/about-pull-requests/)
    with a clear title and description against the `main` branch.

__IMPORTANT__: By submitting a patch, improvement, or new feature, you agree to allow the maintainers of the Slurm workload manager snap to 
license your contributions under the terms of the [Apache Software License, version 2.0](./LICENSE).

## Discussions

GitHub's discussions are a great place to connect with other users of the Slurm workload manager snap as well as discuss potential 
features and resolve personal support questions. It is expected that the users of the Slurm workload manager snap remain respectful of 
each other. Discussion moderators reserve the right to suspend discussions and/or delete posts that do not follow 
this rule.

## Code guidelines

The following guidelines must be adhered to if you are writing code to be merged into the main the Slurm workload manager snap code base:

### Snapcraft

* The `snapcraft` tool does not have a strict style-guide for how you should author snaps, but here 
  are some heuristics that we follow:
  * The _snapcraft.yaml_ file should pass all the [yamllint tests](.yamllint) set for the package.
  * Hooks and wrapper scripts should clearly indicate the shell or interpreter they are meant 
    to be run with using a hashbang. For example, a POSIX shell _configure_ hook should have the
    hashbang `#!/bin/sh -e` as the first line. Snapd will execute this hook using POSIX shell.
  * The snap should bundle all the necessary runtime dependencies that it needs. It should not
    rely on the host system to provide any dependencies unless the snap is clearly a development tool
    meant to use resources provided by the underlying host.
  * Snapcraft and Snap environment variables should be encapsulated with squiggly brackets (`{}`). E.g.
    `$CRAFT_STAGE_DIR` should be referenced as `${CRAFT_STAGE_DIR}`.

### Python

* Adhere to the Python code style guidelines outlined in [Python Enhancement Proposal 8](https://pep8.org/).

* Adhere to the Python docstring conventions outlined in 
[Python Enhancement Proposal 257](https://www.python.org/dev/peps/pep-0257/).
  * *The Slurm workload manager snap's docstrings follow the 
  [Google docstring format](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)*.

## License

By contributing your code to the Slurm workload manager snap, you agree to license your contribution under the 
[Apache Software License, version 2.0](./LICENSE).