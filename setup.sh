#!/bin/bash

## Create a local gitignore
echo ".local_gitignore" >> .local_gitignore
echo ".log" >> .local_gitignore
echo "setup.sh" >> .local_gitignore

awk 'NR==2{print "\texcludesfile = .local_gitignore"}1' .git/config > temp
cat temp > .git/config
rm temp


## Pre-commit hook
cat << EOF >> .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.2.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/pre-commit/mirrors-yapf
    rev: v0.31.0
    hooks:
    -   id: yapf
        additional_dependencies: [toml]
EOF

## Optional setup - python virt. env and more pre-commit hook
## To add more options, simply extend case statement
for arg in "$@"
do
    case $arg in
        -v|--create-env)
        projName="py-env"
        printf "[.] Creating Python vertual environment...\n"
        python3 -m venv $projName
        source $projName/bin/activate
        printf "[√] Finished creating environment.\n"
        shift
        ;;
        -i|--isort)
        pip3 install isort >> .log
        printf "[√] Installed isort\n"
        cat << EOF >> .pre-commit-config.yaml
-   repo: https://github.com/pycqa/isort
    rev: 5.8.0
    hooks:
    -   id: isort
        name: isort (python)
EOF
        printf "[√] Added isort to pre-commit\n"
        shift
        ;;
    esac
done

pip3 install yapf >> .log
pip3 install pre-commit >> .log
pre-commit install
printf "[√] Installed pre-commit\n"
