#!/bin/sh
echo "==> Running Tests <=="
coverage run -m py.test \
    && echo "==> Coverage <==" && \
    coverage report
echo "==> Flake8 <=="
flake8
echo "==> isort <=="
isort -rc --diff -c slackbotframework
echo "If errors present, apply changes with isort -rc --atomic --apply slackbotframework"
echo "==> Bandit <== "
bandit -r slackbotframework
echo "==> Done <=="
