from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PROJECT_NAME = "scenoRITA_V3"
DATA_DIR = Path(PROJECT_ROOT, "data")
DOWNLOAD_DIR = Path(DATA_DIR, "download")

# Docker Configurations
DOCKER_CMD = "docker"

# Apollo Configurations
# APOLLO_RELEASE = "https://github.com/ApolloAuto/apollo/archive/refs/tags/v8.0.0.zip"
# APOLLO_RELEASE_NAME = "apollo-8.0.0"
APOLLO_RELEASE = "https://github.com/YuqiHuai/apollo/archive/refs/tags/v7.0.1.zip"
APOLLO_RELEASE_NAME = "apollo-7.0.1"
APOLLO_ROOT = Path(DATA_DIR, "apollo")
APOLLO_FLAGFILE = Path(APOLLO_ROOT, "modules", "common", "data", "global_flagfile.txt")

# Map Configurations
MAPS_DIR = Path(DATA_DIR, "maps")
SUPPORTED_MAPS = list(x.name for x in MAPS_DIR.iterdir() if x.is_dir())


# Script Configurations
class SCRIPTS:
    SCRIPTS_DIR = Path(PROJECT_ROOT, "scripts")
    DEV_START = Path(SCRIPTS_DIR, "dev_start.sh")
    MULTI_CTN_DEV_START = Path(SCRIPTS_DIR, "multi_ctn_dev_start.sh")


# Other Configurations
SIM_CONTROL_RELEASE = (
    "https://github.com/YuqiHuai/sim_control_standalone/archive/refs/tags/v7.0.0.zip"
)
SIM_CONTROL_RELEASE_NAME = "sim_control_standalone-7.0.0"
LOGGING_PREFIX_REGEX = (
    "^(?P<severity>[DIWEF])(?P<month>\d\d)(?P<day>\d\d) "
    "(?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d)\.(?P<microsecond>\d\d\d) "
    "(?P<filename>[a-zA-Z<][\w._<>-]+):(?P<line>\d+)"
)
LOGGING_FORMAT = (
    "<level>{level.name[0]}{time:MMDD}</level> "
    "<green>{time:HH:mm:ss.SSS}</green> "
    "<cyan>{file}:{line}</cyan>] "
    "<bold>{message}</bold>"
)
