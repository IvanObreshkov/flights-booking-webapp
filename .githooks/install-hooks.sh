#!/bin/bash

# symlink pre-commit
ln -s $PWD/.githooks/pre-commit $PWD/.git/hooks/pre-commit 
chmod +x $PWD/.git/hooks/pre-commit
ls -l $PWD/.git/hooks/pre-commit
