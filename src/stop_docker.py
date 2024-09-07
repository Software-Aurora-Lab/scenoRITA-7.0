from typing import List
import docker
from docker.models.containers import Container

containers: List[Container] = docker.from_env().containers.list()

for container in containers:
    ctn_name = container.name
    ctn_id = container.id
    if ctn_name.startswith("scenoRITA_V3"):
        container.stop()
        container.remove()
        print(f"Container {ctn_name} ({ctn_id}) has been stopped and removed.")
