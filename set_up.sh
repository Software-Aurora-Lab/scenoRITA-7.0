bash data/scripts/install/install_docker.sh && \
    bash data/scripts/install/install_python311.sh && \
    bash data/scripts/install/install_poetry.sh && \
    echo "export PATH=$PATH:$HOME/.poetry/bin" >> ~/.bashrc && \
    source ~/.bashrc && \
    poetry install && \
    poetry run python src/install.py
    