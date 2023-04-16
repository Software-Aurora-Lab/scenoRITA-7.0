import shutil
import subprocess
from pathlib import Path
from time import perf_counter

from loguru import logger

from apollo.container import ApolloContainer
from config import (
    APOLLO_FLAGFILE,
    APOLLO_RELEASE,
    APOLLO_RELEASE_NAME,
    APOLLO_ROOT,
    DATA_DIR,
    DOWNLOAD_DIR,
    PROJECT_NAME,
    SCRIPTS,
    SIM_CONTROL_RELEASE,
    SIM_CONTROL_RELEASE_NAME,
)


def download_apollo():
    if APOLLO_ROOT.exists() and APOLLO_FLAGFILE.exists():
        logger.info("Apollo already installed")
        return
    else:
        logger.info("Installing Apollo ...")
        apollo_release = Path(DOWNLOAD_DIR, "apollo.zip")
        apollo_release.parent.mkdir(parents=True, exist_ok=True)
        if not apollo_release.exists():
            logger.info(f"Downloading release to {apollo_release}")
            subprocess.run(
                f"wget -O {apollo_release} " + APOLLO_RELEASE,
                shell=True,
            )
        else:
            logger.info(f"Release already downloaded to {apollo_release}")

        logger.info("Extracting release ...")
        shutil.unpack_archive(apollo_release, DATA_DIR, "zip")
        shutil.move(Path(DATA_DIR, APOLLO_RELEASE_NAME), APOLLO_ROOT)


def change_script_permissions():
    docker_scripts = APOLLO_ROOT.glob("docker/scripts/*.sh")
    apollo_scripts = APOLLO_ROOT.glob("scripts/*.sh")
    logger.info("Changing script permissions")
    for scripts in [docker_scripts, apollo_scripts]:
        for script in scripts:
            subprocess.run(f"chmod +x {script}", shell=True)


def compile_apollo():
    ctn = ApolloContainer(APOLLO_ROOT, f"{PROJECT_NAME}_installer")
    logger.info("Compiling Apollo")
    ctn.start_container(start_script=SCRIPTS.DEV_START, verbose=True)
    apollo_modules = list(x.name for x in APOLLO_ROOT.glob("modules/*"))
    needed_modules = {
        "dreamview",
        "planning",
        "prediction",
        "routing",
        "cyber",
        "map",
        "common",
        "monitor",
        "common_msgs",  # new in Apollo 8.0.0
    }
    modules = list(needed_modules.intersection(apollo_modules))
    ctn.exec(f"bash apollo.sh build {' '.join(modules)}", verbose=True)


def install_sim_control_standalone():
    target_directory = Path(APOLLO_ROOT, "modules", "sim_control_standalone")
    if target_directory.exists():
        logger.info("Sim control standalone already installed")
        return
    sim_control_release = Path(DOWNLOAD_DIR, "sim_control_standalone.zip")

    logger.info(f"Downloading sim control standalone to {sim_control_release}")

    download_cmd = f"wget -O {sim_control_release} {SIM_CONTROL_RELEASE}"
    print(download_cmd)
    subprocess.run(download_cmd, shell=True)

    logger.info("Extracting sim control standalone")
    shutil.unpack_archive(sim_control_release, DATA_DIR, "zip")
    shutil.move(Path(DATA_DIR, SIM_CONTROL_RELEASE_NAME), target_directory)

    logger.info("Compiling sim control standalone")
    ctn = ApolloContainer(APOLLO_ROOT, f"{PROJECT_NAME}_installer")
    if not ctn.is_running():
        ctn.start_container(start_script=SCRIPTS.DEV_START, verbose=True)
    ctn.exec("bash apollo.sh build sim_control_standalone", verbose=True)


if __name__ == "__main__":
    start = perf_counter()
    download_apollo()
    change_script_permissions()
    compile_apollo()
    install_sim_control_standalone()
    minutes = (perf_counter() - start) / 60
    logger.info(f"Installation completed in {minutes:.2f} minutes")
