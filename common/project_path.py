from os.path import dirname, abspath, join
from os import getcwd


class ProjectPath:

    @staticmethod
    def get_project_path():
        return dirname(dirname(abspath(__file__)))

    @staticmethod
    def get_resource_path():
        return join(project_path.get_project_path(), "./resource/")

    @staticmethod
    def add_abs_path(r_path):
        return ProjectPath.get_project_path()  + r_path


project_path = ProjectPath()
print(join(project_path.get_project_path(), "resource/"))
if __name__ == '__main__':

    print( join(project_path.get_project_path(),"resource/"))