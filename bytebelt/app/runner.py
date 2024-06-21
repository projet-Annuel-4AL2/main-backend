
class Runner:

    def __init__(self, implementation):
        self.implementation = implementation

    def copy_source_files(self, container_name, source, dest):
        self.implementation.copy(container_name, source, dest)

    def run(self, language):
        self.implementation.run(language)

