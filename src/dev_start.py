from apollo.container import ApolloContainer
from config import APOLLO_ROOT, PROJECT_NAME, SCRIPTS

if __name__ == "__main__":
    container = ApolloContainer(APOLLO_ROOT, f"{PROJECT_NAME}_dev_start")
    container.start_container(start_script=SCRIPTS.DEV_START, verbose=True)
