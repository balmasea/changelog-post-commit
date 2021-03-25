import re
import pdb


HEADER_SIZE = 1
HEADER = "# Changelog"


class Group:

    def __init__(self, title):
        self.__title = title
        self.__lines = ""

    def has_content(self):
        return self.__lines != ""

    def add_line(self, line):
        line = line.replace("* ", "")
        self.__lines += f"* {line}"

    def title_matches(self, title):
        return title.upper() in self.__title.upper()

    def __str__(self):
        content = ""
        if self.has_content():
            content += f"{self.__title}\n\n"
            for line in self.__lines:
                content += f"{line}"
            content += "\n"
        return content

class Version:

    def __init__(self, version_title):
        self.__version_title = version_title
        self.__groups = []

    def add_commit_line(self, line):
        group_title_pattern = r"(?P<type_of_change>:[A-Z]+:)"
        m = re.search(group_title_pattern, line)
        line = re.sub(group_title_pattern, "", line).lstrip()
        try:
            title = m.group("type_of_change").replace(":", "")
            group = self.find_group(title)
            group.add_line(line)
        except AttributeError:
            print("Syntax is not correct for the commit. Rejected!")
            exit(-1)

    def set_line(self, line):
        group_title_pattern = r"(?P<type_of_change>### \w+)"
        m = re.search(group_title_pattern, line)
        try:
            title = m.group("type_of_change")
            self.__groups.append(Group(title))
        except AttributeError:
            self.__groups[-1].add_line(line)

    def version_title_matches(self, version_title):
        return version_title in self.__version_title

    def find_group(self, title):
        try:
            iterator = filter(lambda group: group.title_matches(title) is True, self.__groups)
            return next(iterator)
        except StopIteration:
            self.__groups.append(Group(f"### {title.capitalize()}"))
            return self.__groups[-1]

    def __str__(self):
        content = f"{self.__version_title}\n"
        for group in self.__groups:
            content += f"{group}"
        content += "\n"
        return content


class Changelog:

    def __init__(self):
        self.__versions = []

    def push_version(self, version):
        self.__versions.insert(0, version)

    def add_version(self, version):
        self.__versions.append(version)

    def update_version(self, version, index):
        self.__versions[index] = version

    def analyze_changelog_file(self, changelog_path):
        try:
            with open(changelog_path, "r") as cl:
                changelog_lines = cl.readlines()
        except FileNotFoundError:
            changelog_lines = [HEADER]
        iterator = filter(lambda line: line != "\n", changelog_lines)
        changelog_lines = list(iterator)
        version_pattern = r"## v(\d+\.\d+\.\d+)"
        current_version = None
        for line in changelog_lines[HEADER_SIZE:]:
            m = re.search(version_pattern, line)
            if m:
                if current_version:
                    self.add_version(current_version)
                current_version = Version(line)
            else:
                current_version.set_line(line)
        if current_version:
            self.add_version(current_version)

    def add_line_in_version(self, release_line, line):
        iterator_index = (i for i, version in enumerate(self.__versions) if version.version_title_matches(release_line))
        try:
            index = next(iterator_index)
            version = self.__versions[index]
            version.add_commit_line(line)
            self.update_version(version, index)
        except StopIteration:
            version = Version(release_line)
            version.add_commit_line(line)
            self.push_version(version)

    def __str__(self):
        content = f"{HEADER}\n\n"
        for version in self.__versions:
            content += version.__str__()
        return content


def main():
    changelog = Changelog()
    changelog.analyze_changelog_file("CHANGELOG.md")
    changelog.add_line_in_version(
        "## v0.3.0 (March 31 2021)\n",
        ":CHANGE: testing change"
    )
    print(changelog)


if __name__ == "__main__":
    main()
