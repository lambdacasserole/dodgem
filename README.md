<div id="top"></div>



<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/lambdacasserole/dodgem">
    <img src="https://raw.githubusercontent.com/lambdacasserole/dodgem/main/logo.svg" alt="Logo" width="128" height="128">
  </a>

  <h3 align="center">dodgem</h3>

  <p align="center">
    Version bumper for Python project files.
    <br />
    <a href="https://github.com/lambdacasserole/dodgem/issues">Report Bug</a>
    ·
    <a href="https://github.com/lambdacasserole/dodgem/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#example-bump-minor-version">Example: Bump Minor Version</a></li>
        <li><a href="#example-from-commit-message">Example: From Commit Message</a></li>
        <li><a href="#example-custom-tags">Example: Custom Tags</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![dodgem usage][product-screenshot]

Sometimes you need to bump the version in your Python project files automatically. For example, you might:

* Have a CI/CD pipeline, and want to automatically bump the patch version of your library on merge to your `develop` branch
* Have a workflow (e.g. on Bitbucket Pipelines, GitHub actions etc.) that allows developers to automatically perform version bumps by including tags in their commit message (e.g. `[major]`, `[minor]`)
* Just want to reduce the chances of human error when bumping version numbers manually

Dodgem is a command-line utility for doing all of the above, and a bit more, aiming to eventually cover as many Python project file formats as possible, but currently supporting:

* `setuptools` (`setup.py`) with the `version=` named argument
* `pyproject.toml` managed by the [Poetry](https://python-poetry.org/) dependency manager

Named after (version) [bumper cars](https://en.wikipedia.org/wiki/Bumper_cars) which are also sometimes called dodgems in some dialects of English.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

This project uses:

* [Click](https://click.palletsprojects.com/en/8.1.x/) for its CLI
* [Poetry](https://python-poetry.org/) for dependency management
* [Blessings](https://github.com/erikrose/blessings) for colorized and formatted CLI output

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Getting started is straightforward. Dodgem aims to automatically detect as much as possible.

### Prerequisites

You'll need Python 3.7 or newer with pip to install Dodgem.

### Installation

Install Dodgem using pip or your favourite Python dependency manager and you're done.

```bash
pip3 install dodgem
```

Test your installation with:

```bash
dodgem --help
```

You should see help documentation printed.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

You can use `dodgem --help` for detailed information on using the utility:

```
Usage: dodgem [OPTIONS]

  Bump version numbers in a project file.

Options:
  --file TEXT              The file to parse (defaults to automatic
                           detection).
  --file-type TEXT         The file type to parse (defaults to automatic).
  --file-format TEXT       The file format to parse (defaults to automatic).
  --commit-message TEXT    The commit message to infer the version bump from.
  --no-auto-patch BOOLEAN  If given, disables automatic patch version bump if
                           commit message provided.
  --major-tag TEXT         The commit message tag indicating a major version
                           bump.
  --minor-tag TEXT         The commit message tag indicating a minor version
                           bump.
  --patch-tag TEXT         The commit message tag indicating a patch version
                           bump.
  --ignore-tag-case        Ignores capitalization in commit message tags.
  --quiet                  Suppresses all extraneous output.
  --bump-major             If given, performs a major version bump.
  --bump-minor             If given, performs a minor version bump.
  --bump-patch             If given, performs a patch version bump.
  --dry                    If given, does not write the version change to
                           disk.
  --help                   Show this message and exit.
```

### Example: Bump Minor Version

Bump the minor version of your project like this:

```bash
dodgem --bump-minor
```

If you don't want to commit the change to disk, use `--dry` like so:

```bash
dodgem --bump-minor --dry
```

If the informational output given by the CLI is getting in the way of downstream processing, use `--quiet`:

```bash
dodgem --bump-minor --quiet
```

### Example: From Commit Message

Dodgem can bump your project version based on a commit message. By default.

* If the message contains `[major]` then a major version bump will be performed
* If the message contains `[minor]` then a minor version bump will be performed
* Otherwise, a patch version bump will be performed

For example, to use your last `git` commit message to bump your projects version.

```bash
dodgem --commit-message="$(git log -1)"
```

### Example: Custom Tags

If the default `[major]` and `[minor]` tags don't suit you, and you'd perfer `(major)`, `(minor)` and an _explicit_ `(patch)` tag:

```bash
dodgem --commit-message="$(git log -1)" --major-tag='(major)' --minor-tag='(minor)' --patch-tag='(patch)' --no-auto-patch
```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Support `setuptools` (`setup.py`)
- [x] Support [Poetry](https://python-poetry.org/)

See the [open issues](https://github.com/lambdacasserole/dodgem/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Any contributions are very welcome. Please fork the project and open a PR, or open an issue if you've found a bug and/or would like to suggest a feature.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Saul Johnson - [@lambdacasserole](https://twitter.com/lambdacasserole) - saul.a.johnson@gmail.com

Project Link: [https://github.com/lambdacasserole/dodgem](https://github.com/lambdacasserole/dodgem)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

The following resources are awesome:

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template) was used for this readme
* [tomlkit](https://github.com/sdispater/tomlkit/) was used for parsing TOML in a way that preserves comments, order, formatting etc.
* [semver](https://github.com/python-semver/python-semver) was used for parsing and bumping semver numbers

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/lambdacasserole/dodgem.svg?style=for-the-badge
[contributors-url]: https://github.com/lambdacasserole/dodgem/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/lambdacasserole/dodgem.svg?style=for-the-badge
[forks-url]: https://github.com/lambdacasserole/dodgem/network/members
[stars-shield]: https://img.shields.io/github/stars/lambdacasserole/dodgem.svg?style=for-the-badge
[stars-url]: https://github.com/lambdacasserole/dodgem/stargazers
[issues-shield]: https://img.shields.io/github/issues/lambdacasserole/dodgem.svg?style=for-the-badge
[issues-url]: https://github.com/lambdacasserole/dodgem/issues
[license-shield]: https://img.shields.io/github/license/lambdacasserole/dodgem.svg?style=for-the-badge
[license-url]: https://github.com/lambdacasserole/dodgem/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/sauljohnson
[product-screenshot]: https://raw.githubusercontent.com/lambdacasserole/dodgem/main/usage.svg
