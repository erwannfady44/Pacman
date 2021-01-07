import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="PsyqoSlither",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["resources"]}},
    description="Simple Snake Game",
    executables=executables,
    version="0.1"
)
