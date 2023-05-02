import subprocess

from apollo.container import ApolloContainer
from config import APOLLO_ROOT, PROJECT_NAME, SCRIPTS

if __name__ == "__main__":
    container = ApolloContainer(APOLLO_ROOT, f"{PROJECT_NAME}_dev_start")
    container.start_container(start_script=SCRIPTS.MULTI_CTN_DEV_START, verbose=True)
    container.start_dreamview()
    print(f"Dreamview running at {container.dreamview_url}")
    subprocess.run(
        f"docker exec -u $USER -it {container.container_name} /bin/bash", shell=True
    )
