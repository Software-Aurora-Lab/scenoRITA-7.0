function check_code() {
    poetry run mypy src
    poetry run isort src
    poetry run black src
    poetry run ruff src
}

function clean() {
    rm -rf out
    git clean -dfx data/maps
}

function reset_docker() {
    docker stop $(docker ps -aq)
    docker rm $(docker ps -aq)
}

function main() {
    if [ "$#" -eq 0 ]; then
        check_code
        exit 0
    fi
    local cmd="$1"
    case "${cmd}" in
        "check")
            check_code
            ;;
        "clean")
            clean
            ;;
        "reset_docker")
            reset_docker
            ;;
        *)
            check_code
            ;;
    esac
}

main "$@"
