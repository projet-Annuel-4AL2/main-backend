import io
import tarfile
import docker
import os


class DockerImplementation:

    def __init__(self):
        self.client = docker.from_env()
        self.containers = []

    def copy(self, container_name: str, source_path: str, dest_path='/temp_code') -> None:
        if not os.path.exists(source_path):
            raise ValueError(f'Path {source_path} does not exist')

        container = list(filter(lambda cont: cont.name == container_name, self.containers))[0]
        # Creating a buffer to read tar binary data into memory
        with io.BytesIO() as buffer:
            with tarfile.open('temp.tar', mode='w') as tar:
                tar.fileobj = buffer
                tar.add(source_path)
                folder_data = buffer.getvalue()

        container.exec_run(['mkdir', dest_path])
        container.put_archive(dest_path, folder_data)

    def run(self, language: str, container_name: str) -> str:
        container = None
        # Command to keep the containers running
        initial_command = 'tail -f /dev/null'

        if language == 'php':
            container = self.client.containers.run(
                image='php',
                command=initial_command,
                detach=True,
                name=container_name
            )
        elif language == 'python':
            container = self.client.containers.run(
                image='python',
                command=initial_command,
                detach=True,
                name=container_name
            )

        if container is not None:
            self.containers.append(container)

        return container.name