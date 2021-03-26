# COMMIT-MSG HOOK

This repository contains a hook that modifies the CHANGELOG.md file when setting a special commit message.

It combines some requirements from [IaC definitions](https://bitbk.roche.com/projects/ITG/repos/idlc/browse/templates/iac_CHANGELOG.md) with other Global Network Automation requirements. However, those requirements can be easily edited in the hook header, as they are defined as constants.

```python
# Changelog constants
HEADER = "# Changelog"
HEADER_SIZE = 1

# Script constants
CHANGELOG_FILE = "CHANGELOG.md"
WEDNESDAY = 2
WEEK_NUMBER_OF_DAYS = 7
ESCAPE_STRING = ":fix:"
JIRA_LINK = "https://jira.intranet.roche.com/jira/browse/"
TASK_PREFIX = "GNAP-"
CHANGELOG_SUBTITLE = r"(?P<type_of_change>:[A-Z]+:)"
GNAP_REGEX = r"(?P<jira_task>%s\d+)" % TASK_PREFIX
```

## How to install

1. Download or copy file `commit-msg` file

2. Copy it in `.git/hooks/` folder of your repo
```bash
$ mv commit-msg {REPOSITORY_FOLDER}/.git/hooks/
```

where {REPOSITORY_FOLDER} is the folder of the repository where hook is going to be installed.

3. Grant execution permissions for the hook.
```bash
$ chmod a+x {REPOSITORY_FOLDER}/.git/hooks/commit-msg
```

## How to use

When some development has been finished in some branch and the developer is ready to include task information in the `CHANGELOG.md` file, it is as simple as include two tags in commit message:
* `:fix:` to set that commit message shall be included in changelog
* `:<GROUP>:` to set the group where the group belongs. Group can be:
    * NEW
    * CHANGES
    * FIX
    * DOCUMENTATION

Attention: GROUP needs to be in **capital letters**, otherwise, it will not be added to changelog file.

### Jira links

To include Jira task link, it only needs to include `GNAP-{NUMBER}` string inside the commit message.

### Examples

* If this commit is done on March 26th:

```bash
$ git commit -m ':fix: :NEW: First draft of hook'
```

this will be `CHANGELOG.md` content:
```markdown

# Changelog

## v0.1.0 (March 31 2021)
### New

* First draft of hook
```

* If this commit is done on March 26th over that former changelog and with a Jira task:

```bash
$ git commit -m ':fix: :FIX: GNAP-1986 - Unbowed, Unbent, Unbroken
```

this will be `CHANGELOG.md` content:
```markdown

# Changelog

## v0.1.0 (March 31 2021)
### New

* First draft of hook

### Fix

* [GNAP-1986](https://jira.intranet.roche.com/jira/browse/GNAP-1986) - Unbowed, Unbent, Unbroken
```
