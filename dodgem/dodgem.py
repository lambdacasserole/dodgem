""" A simple utility to bump versions in Python project files.

Authors:
    Saul Johnson (saul.a.johnson@gmail.com)
Since:
    18/05/2021
"""

import sys
import os
import re
from enum import Enum

import click
import tomlkit
from blessings import Terminal
from semver import VersionInfo

from typing import Any, Optional


term = Terminal()
""" The global Blessing terminal instance used to write colorized output to the console.
"""


KNOWN_PROJECT_FILENAMES = [
    'setup.py',
    'pyproject.toml',
]
""" A list of known project filenames to automatically detect, in order of priority.
"""

SEMVER_REGEX = r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?'
""" The regular expression to use to match semver strings.
"""

suppress_logging = False
""" Whether or not to suppress logging for the utility.
"""


class ProjectFileType(Enum):
    """ An enumeration of project file types (e.g. TOML).
    """

    UNKNOWN = 0
    """ Specifies that a project file type is unknown.
    """

    TOML = 1
    """ Specifies a TOML project file.
    """

    PYTHON = 2
    """ Specified a Python project file.
    """


class ProjectFileFormat(Enum):
    """ An enumeration of project file formats (e.g. Poetry).
    """

    UNKNOWN = 0
    """ Specifies that a project file format is unknown.
    """

    POETRY = 1
    """ Specifies the file format used by the Poetry dependency manager.
    """

    SETUPTOOLS = 2
    """ Specified the setuptools setup.py file format.
    """


def info(msg: str):
    """ Prints an informational message if logging is not suppressed.

    Args:
        msg (str): The message to print.
    """
    if not suppress_logging:
        print('{t.blue}info{t.normal}:'.format(t=term), msg)


def fatal(msg: str, exit_code: int=1):
    """ Prints a fatal error message and then exits the application.

    Args:
        msg (str): The message to print.
        exit_code (int): The exit code to exit with.
    """
    print('{t.red}fatal{t.normal}:'.format(t=term), msg, file=sys.stderr)
    sys.exit(exit_code)


def detect_project_file() -> Optional[str]:
    """ Detects any known project files in the current working directory.

    Returns:
        Optional[str]: The path of the file or None if no files were detected.
    """
    for filename in KNOWN_PROJECT_FILENAMES:
        if os.path.isfile(filename):
            info(f'Detected file "{filename}" automatically.')
            return filename
    return None


def get_file_type(type: str) -> ProjectFileType:
    """ Converts the string representation of a project file type to its corresponding enum member.

    Args:
        format (str): The string representation of the project file type.
    Returns:
        ProjectFileType: The corresponding enum member.
    """
    return {
        'toml': ProjectFileType.TOML,
        'py': ProjectFileType.PYTHON,
    }.get(type, ProjectFileType.UNKNOWN)


def detect_file_type(path: str) -> ProjectFileType:
    """ Detects the type of the project file at the specified path.

    Args:
        path (str): The path of the project file.
    Returns:
        ProjectFileType: The detected file type of the project file.
    """
    return get_file_type(os.path.splitext(path)[1].strip('.'))


def get_file_format(format: str) -> ProjectFileFormat:
    """ Converts the string representation of a project file format to its corresponding enum member.

    Args:
        format (str): The string representation of the file format.
    Returns:
        ProjectFileFormat: The corresponding enum member.
    """
    return {
        'poetry': ProjectFileFormat.POETRY,
        'setuptools': ProjectFileFormat.SETUPTOOLS,
    }.get(format, ProjectFileFormat.UNKNOWN)


def detect_file_format(path: str) -> ProjectFileFormat:
    """ Detects the format of the project file at the specified path.

    Args:
        path (str): The path of the project file.
    Returns:
        ProjectFileFormat: The detected file format of the project file.
    """
    with open(path, encoding='utf-8') as file:
        for line in file:
            if re.match('^\\s*\\[\\s*tool\\.poetry\\s*\\]\\s*$', line): # This line indicates a Poetry project.
                return ProjectFileFormat.POETRY
            elif re.match('^\\s*(from|import)\\s*setuptools\\s*(import\\s+.+)?$', line): # Setuptools setup.py file.
                return ProjectFileFormat.SETUPTOOLS
    return ProjectFileFormat.UNKNOWN # Format not recognized.


def extract_version(data: Any, format: ProjectFileFormat) -> VersionInfo:
    """ Extracts the current semver from the provided project file data according to the format given.

    Args:
        data (Any): The project data to extract the version from.
        format (ProjectFileFormat): The file format of the project data.
    """
    try:
        if format == ProjectFileFormat.POETRY:
            return VersionInfo.parse(data['tool']['poetry']['version'])
        elif format == ProjectFileFormat.SETUPTOOLS:
            matches = re.search('setup\\(.*version\\s*=\\s*[\'\\"](' + SEMVER_REGEX + ')[\'\\"]', data, re.DOTALL)
            return VersionInfo.parse((matches[1]))
    except:
        pass
    fatal(f'Could not locate a well-formed semver to bump.')


def inject_version(data: Any, format: ProjectFileFormat, version: VersionInfo) -> Any:
    """ Injects the specified semver into the provided project file data according to the format given.

    Args:
        data (Any): The project data to inject the version into.
        format (ProjectFileFormat): The file format of the project data.
        version (VersionInfo): The semver to inject.
    """
    try:
        if format == ProjectFileFormat.POETRY:
            data['tool']['poetry']['version'] = str(version)
            return data
        elif format == ProjectFileFormat.SETUPTOOLS:
            return re.sub('(setup\\(.*version\\s*=\\s*[\'\\"])([0-9\\.]+)([\'\\"])', f'\\g<1>{version}\\g<3>', data, 1,
                re.DOTALL)
    except Exception as e:
        print(e)
        pass
    fatal(f'Could not inject new semver into project file data.')


@click.command()
@click.option('--file', default=None, help='The file to parse (defaults to automatic detection).')
@click.option('--file-type', default=None, help='The file type to parse (defaults to automatic).')
@click.option('--file-format', default=None, help='The file format to parse (defaults to automatic).')
@click.option('--commit-message', default=None, help='The commit message to infer the version bump from.')
@click.option('--no-auto-patch',
    is_flag=True,
    default=False,
    help='If given, disables automatic patch version bump if commit message provided.')
@click.option('--major-tag', default='[major]', help='The commit message tag indicating a major version bump.')
@click.option('--minor-tag', default='[minor]', help='The commit message tag indicating a minor version bump.')
@click.option('--patch-tag', default=None, help='The commit message tag indicating a patch version bump.')
@click.option('--prerelease-tag', default='[prerelease]', help='The commit message tag indicating a prerelease version bump.')
@click.option('--ignore-tag-case', is_flag=True, default=False, help='Ignores capitalization in commit message tags.')
@click.option('--quiet', is_flag=True, default=False, help='Suppresses all extraneous output.')
@click.option('--bump-major', is_flag=True, default=False, help='If given, performs a major version bump.')
@click.option('--bump-minor', is_flag=True, default=False, help='If given, performs a minor version bump.')
@click.option('--bump-patch', is_flag=True, default=False, help='If given, performs a patch version bump.')
@click.option('--bump-prerelease', is_flag=True, default=False, help='If given, performs a prerelease version bump.')
@click.option('--bump-build', is_flag=True, default=False, help='If given, performs a build version bump.')
@click.option('--prerelease-token', default=None, help='The prerelease token to append.')
@click.option('--build-token', default=None, help='The build token to append.')
@click.option('--dry', is_flag=True, default=False, help='If given, does not write the version change to disk.')
def main(
    file: Optional[str],
    file_type: Optional[str],
    file_format: Optional[str],
    commit_message: Optional[str],
    no_auto_patch: bool,
    major_tag: str,
    minor_tag: str,
    patch_tag: Optional[str],
    prerelease_tag: str,
    ignore_tag_case: bool,
    quiet: bool,
    bump_major: bool,
    bump_minor: bool,
    bump_patch: bool,
    bump_prerelease: bool,
    bump_build: bool,
    prerelease_token: str,
    build_token: str,
    dry: bool):
    """ Bump version numbers in a project file.
    """

    # Switch logging on or off.
    global suppress_logging
    suppress_logging = quiet

    # If file parameter not provided, attempt to detect it automatically.
    if file is None:
        file = detect_project_file()

        # No project file could be detected automatically, fatal.
        if file is None:
            fatal('No project file name provided and none could be detected automatically.')

    # Fatal error if file not found.
    if not os.path.isfile(file):
        fatal(f'Specified project file "{file}" not found.')

    # Convert provided file type to enum or attempt automatic detection if not provided.
    parsed_file_type = None
    if file_type is None:
        parsed_file_type = detect_file_type(file)
    else:
        parsed_file_type = get_file_type(file_type)

    # Fatal error if project file type unknown.
    if parsed_file_type == ProjectFileType.UNKNOWN:
        fatal('The type of this project file is unknown and could not be detected automatically.')
    info(f'Detected type of file "{file}" automatically as: {parsed_file_type.name}')

    # Convert provided file format to enum or attempt automatic detection if not provided.
    parsed_file_format = None
    if file_format is None:
        parsed_file_format = detect_file_format(file)
    else:
        parsed_file_format = get_file_format(file_format)

    # Fatal error if project file format unknown.
    if parsed_file_format == ProjectFileFormat.UNKNOWN:
        fatal('The format of this project file is unknown and could not be detected automatically.')
    info(f'Detected format of file "{file}" automatically as: {parsed_file_format.name}')

    # Load project file data from disk.
    project_file_data = None
    with open(file, 'r', encoding='utf-8') as file_handle:
        if parsed_file_type == ProjectFileType.TOML:
            project_file_data = tomlkit.load(file_handle)
        else:
            project_file_data = file_handle.read()

    # Extract version from project file data.
    old_version = extract_version(project_file_data, parsed_file_format)
    new_version = old_version

    # Case correction if tag case should be ignored.
    if ignore_tag_case:
        commit_message = commit_message.lower()
        major_tag = major_tag.lower()
        minor_tag = minor_tag.lower()
        patch_tag = patch_tag.lower() if patch_tag is not None else None

    # Perform version bump depending on explicit args and/or commit message/tags.
    if bump_major or (commit_message is not None and major_tag in commit_message):
        new_version = new_version.bump_major()
    elif bump_minor or (commit_message is not None and minor_tag in commit_message):
        new_version = new_version.bump_minor()
    elif bump_patch or (commit_message is not None and patch_tag in commit_message) or not no_auto_patch:
        new_version = new_version.bump_patch()

    # These versions (prerelease/build metadata) can be bumped independently.
    if bump_prerelease or (commit_message is not None and prerelease_tag in commit_message):
        new_version = new_version.bump_prerelease(prerelease_token)
    if bump_build:
        new_version = new_version.bump_build(build_token)

    # If dry flag not specified, write back to disk...
    if not dry:
        project_file_data = inject_version(project_file_data, parsed_file_format, new_version) # Inject new version.
        with open(file, 'w', encoding='utf-8') as file_handle:
            if parsed_file_type == ProjectFileType.TOML:
                tomlkit.dump(project_file_data, file_handle)
            else:
                file_handle.write(project_file_data)

    # Print out version bump.
    print(f'{old_version} -> {new_version}')


# Run main method if invoked directly.
if __name__ == '__main__':
    main()
