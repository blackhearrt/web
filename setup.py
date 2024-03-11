from setuptools import setup, find_namespace_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(name = "personal_cli_assistant",
      version = "0.0.5",
      author = "Group_03",
      url = "https://github.com/mykhailooprelyansky/personal_assistant_group_03.git",
      license = "MIT",
      readme = "README.md",
      include_package_data=True,
      classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        ],
      description= "'Personal assistant' with a command line interface.",
      long_description = long_description, long_description_content_type="text/markdown",
      entry_points = {
          'console_scripts': ['start_cli = personal_assistant_group_03.main:main'] 
      },
      packages = find_namespace_packages(),         
)