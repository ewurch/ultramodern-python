import tempfile
import nox

nox.options.sessions = "tests"
locations = "src", "tests", "noxfile.py", "docs/conf.py"


@nox.session(python=["3.10", "3.11"])
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)


@nox.session(python=["3.10", "3.11"])
def lint(session):
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-black",
        "flake8-import-order",
        "flake8-bugbear",
        "flake8-bandit",
    )
    session.run("flake8", *args)


@nox.session(python="3.10")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox.session(python="3.10")
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")

@nox.session(python=["3.10", "3.11"])
def mypy(session):
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)

@nox.session(python="3.10")
def docs(session):
    """Build the documentation."""
    session.install("sphinx")
    session.run("sphinx-build", "docs", "docs/_build")

@nox.session(python="3.8")
def docs(session):
    """Build the documentation."""
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")
