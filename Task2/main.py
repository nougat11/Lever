"""This script performs semantic string comparison."""
import re


class Version:
    """This class performs semantic string comparison."""
    def __init__(self, version):
        self.version_core, self.pre_release = self._parse(version)
        self._check_errors()

    @staticmethod
    def _parse(version):
        """This method splits version into 2 parts."""
        version = version.replace('-', '.')
        version = version.split('.')
        version_core = version[:3]
        pre_release = version[3:]
        for index, char in enumerate(version_core[-1]):
            if not char.isdigit():
                pre_release = [version_core[-1][index:]] + pre_release
                version_core[-1] = version_core[-1][:index]
        while len(version_core) < 3:
            version_core.append('0')
        return version_core, pre_release

    def _check_errors(self):
        """This method checks for errors in version."""
        for i in range(len(self.version_core) - 1):
            if re.search(r'\D', self.version_core[i]):
                raise ValueError('ValueError: major versions contains only numbers')

        for version in self.version_core:
            if version[0] == '0' and len(version) > 1:
                raise ValueError('ValueError: version core should not contain leading zeros')

    def __eq__(self, other):
        return self.version_core == other.version_core and self.pre_release == other.pre_release

    def __lt__(self, other):
        if self.version_core < other.version_core:
            return True
        if self.version_core == other.version_core and self.pre_release and not other.pre_release:
            return True
        if self.version_core == other.version_core and self.pre_release < other.pre_release:
            return True
        return False


def main():
    """This method tests semantic string comparison."""
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        ("1.0.0-a.a", "1.0.0-a.b.b"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"

    to_le = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        ("1.0.0-a.a", "1.0.0-a.b.b")
    ]
    for version_1, version_2 in to_le:
        assert Version(version_1) < Version(version_2), "eq failed"

    to_ge = [
        ("2.0.0", "1.0.0"),
        ("1.42.0", "1.0.0"),
        ("1.2.42", "1.2.0"),
        ("1.2.0-alpha", "1.1.0-alpha.1"),
        ("1.0.11b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        ("1.0.0-a.c", "1.0.0-a.b.b")
    ]
    for version_1, version_2 in to_ge:
        assert Version(version_1) == Version(version_2), "ge failed"

    to_eq = [
        ("1.0", "1.0.0"),
        ("1", "1.0.0")
    ]
    for version_1, version_2 in to_eq:
        assert Version(version_1) == Version(version_2), "eq failed"


if __name__ == "__main__":
    main()
