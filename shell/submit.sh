<<<<<<< Updated upstream
=======
#!/bin/bash
conda create --name $2 python=3.9
conda activate $2
python -m pip install pytest
gh repo create $1  --public --license gpl-3.0 --gitignore Python
cd $1
gh repo clone $1

cd $1
touch README.md
git add .
git commit -m "first commit"

mkdir src/
mkdir src/pyclassify
touch src/pyclassify/__init__.py
touch src/pyclassify/utils.py
mkdir scripts/
touch scripts/run.py
mkdir shell/
touch shell/submit.sbatch
touch shell/submit.sh
mkdir test/
touch test/test_.py
python -m pip freeze > requirements.txt
echo "#Additional command\n*.dat\n*.data" >> .gitignore

cat <<EOF > pyproject.toml
# Choosing a build backend:
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "pyclassify"
version = "0.0.1"
description = "${5}"
readme = "README.md"
requires-python = ">=3.9"
license = { file = "LICENSE" }
authors = [{ name = "${3}", email = "${4}" }]
dynamic = ["dependencies"]

[tool.setuptools.packages.find]
where = ["src"]
exclude = ["scripts", "tests", "shell", "experiments"]

[tool.setuptools.dynamic]
dependencies = { file = ["requirements.txt"] }

[project.optional-dependencies]
test = ["pytest"]
EOF

git add .
git commit -m "structuring the package"
git push origin HEAD:main
>>>>>>> Stashed changes
