set -eo pipefail
#pipefail은 실행해 나아가다 실패하면 밑으로 진행하지 않는다)

COLOR_GREEN=`tput setaf2;`
COLOR_NC=`tput sgr0;`

echo "Starting black"
poetry run black .
echo "OK"
echo "Starting ruff"
poetry run ruff check --select I --fix
poetry run ruff check --fix
echo "OK"
echo "Starting mypy"
poetry run dmypy run -- .
echo "OK"
echo "Starting pytest with coverage"
poetry run coverage run -m pytest
poetry run coverage report -m
poetry run coverage html
echo "OK"

echo "${COLOR_GREEN}All tests passed successfully${COLOR_NC}"