# Contribution guidelines

These guidelines instruct how to submit issues and contribute code to the
[Robot Framework Assistant](https://github.com/andriyko/sublime-robot-framework-assistant)
project.

# Table of Contents
- [Submitting issues](Submitting_issues)
  - [Reporting bugs](Reporting_bugs)
  - [Enhancement requests](Enhancement_requests)
- [Code contributions](Code_contributions)
  - [Choosing something to work on](Choosing_something_to_work_on)
  - [Pull requests](Pull_requests)
  - [Coding conventions](Coding_conventions)
    - [General guidelines](General_guidelines)
    - [Whitespace](Whitespace)
    - [Docstrings](Docstrings)
  - [Tests](Tests)
    - [Acceptance tests](Acceptance_tests)
    - [Unit tests](Unit_tests)
  - [Finalizing pull requests](Finalizing_pull_requests)
  - [AUTHORS.txt](AUTHORS.txt)
  - [Resolving conflicts](Resolving_conflicts)
  - [Squashing commits](Squashing_commits)

# Submitting issues

Bugs and enhancements are tracked in the
[issue tracker](https://github.com/andriyko/sublime-robot-framework-assistant/issues).
If you are unsure if something is a bug or is a feature worth implementing,
you can first ask on
[robotframework-users](https://groups.google.com/forum/#!forum/robotframework-users).
mailing list or [Slack](https://robotframework-slack.herokuapp.com).
These and other similar forums, not the issue tracker, are also places
where to ask general questions.

Before submitting a new issue, it is always a good idea to check is the
same bug or enhancement already reported. If it is, please add your comments
to the existing issue instead of creating a new one.

## Reporting bugs
Explain the bug you have encountered so that others can understand it
and preferably also reproduce it. Key things to have in good bug report:

1. Version information
   - Sublime version
   - Plugin version
   - Robot Framework version
   - Operating system name and version

2. Steps to reproduce the problem. With more complex problems it is often
   a good idea to create a short, self contained, correct example
   [(SSCCE)](http://sscce.org).

3. Possible error message and traceback.
   - When internal database is created and updated, a log file is
     created, by default, in the plugin installation directory, in the
     `database` folder.
   - It is good idea to check the Sublime console for a traceback.

Notice that all information in the issue tracker is public. Do not include
any confidential information there.

## Enhancement requests

Describe the new feature and use cases for it in as much detail as possible.
Especially with larger enhancements, be prepared to contribute the code
in form of a pull request as explained below or to pay someone for the work.
Consider also would it be better to implement this functionality as a separate
tool outside the core plugin.

# Code contributions

If you have fixed a bug or implemented an enhancement, you can contribute
your changes via GitHub's pull requests. This is not restricted to code,
on the contrary, fixes and enhancements to documentation_ and tests_ alone
are also very valuable.

## Choosing something to work on

Often you already have a bug or an enhancement you want to work on in your
mind, but you can also look at the `issue tracker` to find bugs and
enhancements submitted by others. The issues vary significantly in complexity
and difficulty, so you can try to find something that matches your skill level
and knowledge.

## Pull requests

On GitHub pull requests are the main mechanism to contribute code. They
are easy to use both for the contributor and for person accepting
the contribution, and with more complex contributions it is easy also
for others to join the discussion. Preconditions for creating a pull
requests are having a [GitHub account](https://github.com/)
installing [Git](https://git-scm.com) and forking the
[Robot Framework Assistant project](https://github.com/andriyko/sublime-robot-framework-assistant).

GitHub has good articles explaining how to
[set up Git](https://help.github.com/articles/set-up-git/),
[fork a repository](https://help.github.com/articles/fork-a-repo/) and
[use pull requests](https://help.github.com/articles/using-pull-requests)
and we do not go through them in more detail. We do, however,
recommend to create dedicated branches for pull requests instead of creating
them based on the master branch. This is especially important if you plan to
work on multiple pull requests at the same time.

## Coding conventions

### General guidelines

Robot Framework Assistant uses the general Python code conventions defined in
[PEP-8](https://www.python.org/dev/peps/pep-0008/). In addition to that, we try
to write
[idiomatic Python](http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html)
with all new code. An important guideline is that the code should be
clear enough that comments are generally not needed.

Code that directly uses
[Sublime Text API](https://www.sublimetext.com/docs/3/api_reference.html),
must be compatible with Python 3.3. This mostly includes code in the
[commands](https://github.com/andriyko/sublime-robot-framework-assistant/tree/master/commands)
and
[setting](https://github.com/andriyko/sublime-robot-framework-assistant/tree/master/setting)
folders. This is required because the Sublime Text 3 contains
internal version of Python 3.3 which is used for API calls.

All code the
[dataparser](https://github.com/andriyko/sublime-robot-framework-assistant/tree/master/dataparser)
folder must support the Python 2 and Python 3. The plugin uses latest
versions of
[Robot Framework API](https://robot-framework.readthedocs.io/en/latest/)
to parse the test data and libraries. And the latest Robot Framework
versions support both Python 2 and Python 3.

The
[command_helper](https://github.com/andriyko/sublime-robot-framework-assistant/tree/master/command_helper)
folder also needs support for Python 2 and Python 3. The Python 2
support is required because the unit tests are run in
[Travis](https://travis-ci.org/andriyko/sublime-robot-framework-assistant)
with Python 2. The Python 3 support is required, because the modules
in `command_helper` folder are used by plugin `commands`.

### Whitespace

We are pretty picky about using whitespace. We use blank lines and whitespace
in expressions as dictated by `PEP-8`, but we also follow these rules:

- Indentation using spaces, not tabs.
- No trailing spaces.
- No extra empty lines at the end of the file.
- Files must end with a newline.

The above rules are good with most other code too. Any decent editor or IDE
can be configured to automatically format files according to them.

### Docstrings

Docstrings should be added when needed to clarify functionality. At least classes
should have documentation what the class is used for. When docstrings are added,
they should follow [PEP-257](https://www.python.org/dev/peps/pep-0257/).

## Tests

When submitting a pull request with a new feature or a fix, you should
always include tests for your changes. These tests prove that your changes
work, help prevent bugs in the future, and help document what your changes
do. Depending an the change, you may need unit tests, acceptance tests
or both.

Make sure to run all of the tests before submitting a pull request to be sure
that your changes do not break anything. If you can, test in multiple
environments. (Windows, Linux and OS X). Pull requests are also
automatically tested on
[Travis](https://travis-ci.org/andriyko/sublime-robot-framework-assistant).

#### Acceptance tests

There are very little acceptance test for the plugin and Robot Framework
is used to run the test. Most of the features should not be tested
with acceptance tests.

#### Unit tests

Unit tests are great for testing internal logic and should be added when
appropriate. It is not possible directly to test sublime commands.
Instead the feature functionality should be divided in such way that
the command core functionality does not require use the Sublime Text API.
The command core functionality should be unit tested.

## Finalizing pull requests

Once you have code, documentation and tests ready, it is time to finalize
the pull request.

### AUTHORS.txt

If you have done any non-trivial change and would like to be credited,
add yourself to
[AUTHORS.txt](https://github.com/andriyko/sublime-robot-framework-assistant/blob/master/AUTHORS.txt) file.

### Resolving conflicts

Conflicts can occur if there are new changes to the master that touch the
same code as your changes. In that case you should
[sync your fork](https://help.github.com/articles/syncing-a-fork) and
[resolve conflicts](https://help.github.com/articles/resolving-a-merge-conflict-from-the-command-line)
to allow for an easy merge.

The most common conflicting file is the aforementioned `AUTHORS.txt`, but
luckily fixing those conflicts is typically easy.

### Squashing commits

If the pull request contains multiple commits, it is recommended that you
squash them into a single commit before the pull request is merged.
See `
[Squashing Github pull requests into a single commit](http://eli.thegreenplace.net/2014/02/19/squashing-github-pull-requests-into-a-single-commit)
article for more details about why and how.

Squashing is especially important if the pull request contains lots of
temporary commits and changes that have been later reverted or redone.
Squashing is not needed if the commit history is clean and individual
commits are meaningful alone.
