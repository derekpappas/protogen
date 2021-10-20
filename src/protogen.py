from git import Repo
from pathlib import Path
import argparse
import os
import subprocess


# Example directory layout
#
# └── include
# |   └── googleapis
# |   |   ├── LICENSE
# |   |   └── google
# |   |   |   └── api
# |   |   |   |   ├── annotations.proto
# |   |   |   |   └── http.proto
# |   |   |   └── rpc
# |   |   |   |   ├── code.proto
# |   |   |   |   ├── error_details.proto
# |   |   |   |   └── status.proto
# |   └── grpc-gateway
# |   |   ├── LICENSE.txt
# |   |   └── protoc-gen-openapiv2
# |   |   |   └── options
# |   |   |   |   ├── annotations.proto
# |   |   |   |   └── openapiv2.proto
# └── proto
# |   └── notes
# |   |   └── v1
# |   |   |   └── api.proto
# └── v1
# |   ├── api.pb.go
# |   └── api_grpc.pb.go

class utils:
    def mkdirpath(self, p):
        """
        This function greets to
        the person passed in as
        a parameter
        """
        Path(p).mkdir(parents=True, exist_ok=True)

    def subprocessRun(self, cmd, msg):
       try:
           subprocess.run([cmd], check=True)
       except subprocess.CalledProcessError:
           print(f"{msg}")

    def cloneGitRepo(self, repo, target_dir):
        """
        Clone a repo and insert it at the target_dir locations
        """
        if not target_dir.exists():
            print(f"INFO cloning {target_dir}")
            Repo.clone_from(repo, target_dir)
        else:
            print(f"INFO dir exists can't clone {target_dir}")

    def cd(self, dir):
        try:
            os.chdir(dir)
        except:
            print(f"Error: Could not cd to {dir}")

utils = utils()

class ProtoGen:
    def __init__(self, root_dir, proto_project_name, proto_dir):
        self.root_dir = root_dir
        self.proto_project_name = proto_project_name
        self.proto_dir = proto_dir
        self.options = ""
        self.includes = ""

    def makeDirectoryStructure(self):
        self.includes = f"{self.root_dir}/include/googleapis/google"
        utils.mkdirpath(self.includes)

        self.options = f"{self.root_dir}/grpc-gateway/protoc-gen-openapiv2/options"
        utils.mkdirpath(self.options)

        self.options = f"{self.root_dir}/proto/{self.proto_project_name}/v1"
        utils.mkdirpath(self.options)

    def addGRPCRepos(self):
        grpc_tmp = "/tmp/grpc_tmp/"
        grpc_java = "/tmp/grpc_tmp/grpc_java/"
        path = Path(grpc_java)
        utils.cloneGitRepo('git@github.com:grpc/grpc-java.git', path)

        utils.cd(self.includes)


def parse():
    parser = argparse.ArgumentParser(description="Generate a protobuf directory hierarchy")
    parser.add_argument('-rd', action="store", dest="root_dir", help='Root directory')
    parser.add_argument('-ppn', action="store", dest="proto_project_name", help='Proto project name')
    parser.add_argument('-pd', action="store", dest="proto_dir", help='Proto files directory')

    args = parser.parse_args()
    print(args.root_dir)
    print(args.proto_project_name)
    return args

def main():
    args = parse()
    protogen = ProtoGen(args.root_dir, args.proto_project_name, args.proto_dir)
    protogen.makeDirectoryStructure()
    protogen.addGRPCRepos()

if __name__ == "__main__":
    main()






