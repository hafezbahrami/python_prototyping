# template-python-package
Simple python package template.

**NOTE:** This template is provided as a convenient way to get a basic python project started that includes testing and
static analysis tools. It is up to you to choose how you will manage environments/dependencies and if you will use tools
such as `pipenv`, `uv`, or `pixi`.

## Getting Started
- Install [copier](https://copier.readthedocs.io/en/stable/#installation) if you don't already have it.
- Make a new git repo or directory with your package name using kebab case i.e. `new-python-project`
- Copy this template by running `copier copy <This git repo URL> <New project directory path>`
- Create a virtual environment using the tool of your choice and install the project requirements by running
`pip install -e .[dev]`. This will install all development dependencies and an editable version of the project in your
virtual environment.
- Some common development tasks have been included in `tasks.py`. Run static code analysis and unit tests using the 
following commands: `inv validate` and `inv test`.

## Next Steps
- Edit the README.md for your project.
- Add your own dependency/environment management tool (`pipenv`, `uv`, `pixi`...) files if you want.
- Add project specific automation tasks in `tasks.py`.
- Start writing code and tests.
