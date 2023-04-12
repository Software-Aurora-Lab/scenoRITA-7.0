import os
import subprocess
from pathlib import Path

import docker
import docker.errors

from config import DOCKER_CMD, PROJECT_NAME, PROJECT_ROOT, SCRIPTS


class ApolloContainer:
    def __init__(self, apollo_dir: Path, ctn_name: str) -> None:
        self.apollo_dir: Path = apollo_dir
        self.ctn_name: str = ctn_name

    def __repr__(self):
        return f"ApolloContainer(ctn_name={self.ctn_name})"

    def start_container(self, start_script=SCRIPTS.MULTI_CTN_DEV_START, verbose=False):
        if self.is_running():
            return True
        options = "-y -l -f"
        docker_script_dir = Path(self.apollo_dir, "docker", "scripts")
        cmd = f"bash {start_script} {options}"
        subprocess.run(
            cmd,
            env={
                "CURR_DIR": docker_script_dir,
                "DEV_CONTAINER": self.ctn_name,
                "USER": os.environ.get("USER"),
                "PROJECT_ROOT": PROJECT_ROOT.absolute(),
                "PROJECT_NAME": f"/{PROJECT_NAME}",
            },
            shell=True,
            capture_output=not verbose,
        )

    def rm_container(self):
        if self.is_running():
            for op in ["stop", "rm"]:
                cmd = f"docker {op} {self.container_name}"
                subprocess.run(cmd, shell=True, capture_output=True)

    @property
    def container_name(self) -> str:
        return self.ctn_name

    def container_ip(self) -> str:
        """
        Gets the ip address of the container
        :returns: IP address of this container
        """
        assert self.is_running(), f"Container {self.container_name} is not running."
        ctn = docker.from_env().containers.get(self.container_name)
        return ctn.attrs["NetworkSettings"]["IPAddress"]

    def exists(self) -> bool:
        """
        Checks if the container exists
        :returns: True if exists, False otherwise
        """
        try:
            docker.from_env().containers.get(self.container_name)
            return True
        except (docker.errors.NotFound, docker.errors.DockerException):
            return False

    def is_running(self) -> bool:
        """
        Checks if the container is running
        :returns: True if running, False otherwise
        """
        try:
            return (
                docker.from_env().containers.get(self.container_name).status
                == "running"
            )
        except Exception:
            return False

    @property
    def dreamview_url(self) -> str:
        """
        Gets the Dreamview url of the container
        :returns: Dreamview url of this container
        """
        return f"http://{self.container_ip()}:8888"

    def exec(self, cmd: str, detached=False, verbose=False):
        """
        Executes a command in the container
        :param cmd: Command to execute
        :param detached: Whether the command should be executed in detached mode
        """
        exe = (
            f"{DOCKER_CMD} exec "
            + "-u $USER "
            + f'{"-d " if detached else ""}{self.container_name} {cmd}'
        )
        return subprocess.run(exe, shell=True, capture_output=not verbose)

    def start_dreamview(self):
        self.exec("bash /apollo/scripts/dreamview.sh start")

    def restart_dreamview(self):
        self.exec("bash /apollo/scripts/dreamview.sh restart")

    def start_bridge(self):
        self.exec("bash /apollo/scripts/bridge.sh", detached=True)

    def start_planning(self):
        self.exec("bash /apollo/scripts/planning.sh start")

    def start_routing(self):
        self.exec("bash /apollo/scripts/routing.sh start")

    def start_prediction(self):
        self.exec("bash /apollo/scripts/prediction.sh start")

    def start_ads_modules(self):
        # self.start_bridge()
        self.start_routing()
        self.start_prediction()
        self.start_planning()

    def stop_ads_modules(self):
        cmd = "pkill --signal SIGKILL -f 'planning|routing|prediction|cyber_bridge'"
        self.exec(cmd)

    def start_sim_control(self, x: float, y: float, heading: float):
        executable = "/apollo/bazel-bin/modules/sim_control_standalone/main"
        cmd = f"{executable} {x} {y} {heading}"
        self.exec(cmd, detached=True)

    def stop_sim_control(self):
        cmd = "pkill --signal SIGKILL -f 'sim_control_standalone'"
        self.exec(cmd)

    def start_replay(self, filename: str):
        # cyber_recorder play -f <file>
        cyber_recorder = "/apollo/bazel-bin/cyber/tools/cyber_recorder/cyber_recorder"
        cmd = f"{cyber_recorder} play -f {filename}"
        self.exec(cmd, detached=True)

    def stop_replay(self):
        cmd = "pkill --signal SIGINT -f 'cyber_recorder play'"
        self.exec(cmd)

    def start_recorder(self, filename: str):
        # cyber_recorder record -o <file>
        cyber_recorder = "/apollo/bazel-bin/cyber/tools/cyber_recorder/cyber_recorder"
        cmd = f"{cyber_recorder} record -a -o {filename}"
        self.exec(cmd, detached=True)

    def stop_recorder(self):
        cmd = "pkill --signal SIGINT -f 'cyber_recorder record'"
        self.exec(cmd)
