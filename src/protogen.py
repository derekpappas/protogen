from git import Repo
from pathlib import Path
import argparse
import os
import shutil
import subprocess

import json
# from google.protobuf.json_format import Parse

# https://github.com/json-to-proto/json-to-proto.github.io

# message = Parse(json.dumps({
#     "first": "a string",
#     "second": True,
#     "third": 123456789
# }), Thing())

# print(message.first)  # "a string"
# print(message.second) # True
# print(message.third)  # 123456789

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
        if target_dir.exists():
            utils.rmtree(target_dir)

        utils.mkdirpath(target_dir)

        print(f"INFO start cloning {repo} to {target_dir}")
        Repo.clone_from(repo, target_dir)
        print(f"INFO done cloning {repo} to {target_dir}")

    def cd(self, dir):
        try:
            os.chdir(dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            print(f"Error: Could not cd to {dir}")

    def rmtree(self, path):
        try:
            shutil.rmtree(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def cptree(self, path):
        try:
            shutil.cptree(path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


utils = utils()

class ProtoGen:
    def __init__(self, root_dir, proto_project_name, proto_dir):
        self.root_dir = root_dir
        self.proto_project_name = proto_project_name
        self.proto_dir = proto_dir
        self.options = ""
        self.includes = ""
        self.grpc_tmp = "/tmp/grpc_tmp"
        self.grpc_tmp_path = Path(self.grpc_tmp)

    def makeDirectoryStructure(self):
        self.includes = f"{self.root_dir}/include/googleapis/google"
        utils.mkdirpath(self.includes)

        self.options = f"{self.root_dir}/grpc-gateway/protoc-gen-openapiv2/options"
        utils.mkdirpath(self.options)

        self.options = f"{self.root_dir}/proto/{self.proto_project_name}/v1"
        utils.mkdirpath(self.options)

    def addGRPCRepo(self, repo, subdir):
        path = Path(os.path.join(self.grpc_tmp, subdir))
        utils.cloneGitRepo(repo, path)
        utils.cd(self.includes)


    def addGRPCJavaRepo(self):
        self.addGRPCRepo('git@github.com:grpc/grpc-java.git', "grpc_java")
        utils.cd(self.includes)
        src = Path(f"{self.grpc_tmp}/grpc_java/xds/third_party/googleapis")
        utils.cptree(src)

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
    protogen.addGRPCJavaRepo()

if __name__ == "__main__":
    main()






