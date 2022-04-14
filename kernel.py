#! /usr/bin/env python3
import os
import sys
import subprocess

ENV = {
    "url": "https://github.com/analogdevicesinc/linux",
    "tag": "master",
    "repo": None,
}

def command (cmd):
    ret = os.system(cmd)
    if ret > 0:
        raise RuntimeError("failed to exec {}".format(cmd))
def exists (path):
    return os.path.exists(path)
def git_clone (url, branch):
    command("git clone {} --branch {}".format(url, branch))
def mkdir (path):
    command("mkdir -p {}".format(path))
def rmf (path):
    command("rm -f {}".format(path))

def file_suffix (path):
    """ truncates x/y/path into "path" """
    return path.split("/")[-1]
def file_prefix (path):
    """ truncates x/y/path into "path" """
    return "/".join(path.split("/")[:-1])
def strip_prefix (path):
    """ truncates x/y/path.z into "path" """
    return path.split("/")[-1].split(".")[0]
def strip_extension (path):
    """ truncates x/y/path.z into "z" """
    return path.split("/")[-1].split(".")[-1]

def main (argv):
    global ENV

    for i in range (0, len(argv)):
        key = argv[i].strip("--")
        if key in ENV:
            ENV[key] = argv[i+1]
    
    # env
    repo = ENV["repo"]
    url  = ENV["url"]
    tag  = ENV["tag"]

    # download custom content 
    clone_target = url.split("/")[-1]
    if not(exists(clone_target)):
        git_clone(url, tag)

    # build products
    rmf("patches/*.patch")
    mkdir("patches")
    # parse products
    with open("files.txt", "r") as fd:
        files = fd.read().strip().split("\n")
 
    # run diff for all selected files
    count = 1
    for f in files:
        prefix = file_prefix(f).replace("/", "-")
        prefix = prefix.replace("_","-")
        name = strip_prefix(f).replace("_","-")
        patch = "{:04d}-{}-{}.patch".format(count, prefix, name)
        # two options
        # [1] either this file exists 
        #     --> custom modification
        # [2] or this file does not exist in local repo
        #     --> brand new
        if exists(repo +"/" +f):
            # patch to generate
            print("modification patch : \"{}\"".format(patch))
            cmd = [
                "diff", 
                "-ruN", 
                "{}/{}".format(repo, f),
                "{}/{}".format(clone_target, f),
            ]
            # run `diff`
            ret = subprocess.run(cmd, capture_output=True)
            stdout = ret.stdout.decode("utf-8")
            # need to replace, in generated patch
            # the /x/y/z prefix of the local repo,
            # so this patch can apply in tree
            # produce patch  
            stdout = stdout.replace("{}/{}".format(repo, f), "")
            with open("patches/{}".format(patch), "w") as fd:
                fd.write(stdout)

        else:
            # patch to generate
            print("new patch : {}".format(patch))
            cmd = [
                "diff", 
                "-ruN", 
                "{}/{}".format(repo, f),
                "{}/{}".format(clone_target, f),
            ]
            # run `diff`
            ret = subprocess.run(cmd, capture_output=True)
            stdout = ret.stdout.decode("utf-8")
            # need to replace, in generated patch
            # the /x/y/z prefix of the local repo,
            # so this patch can apply in tree
            stdout = stdout.replace("{}/{}".format(repo, f), "")
            # produce patch  
            with open("patches/{}".format(patch), "w") as fd:
                fd.write(stdout)
        count += 1

if __name__ == "__main__":
    main(sys.argv[1:])
