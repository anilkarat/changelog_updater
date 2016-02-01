#! /usr/bin/env python

import os,sys
import subprocess
import datetime
import optparse
#version = __init__.get_version("patch")

def get_version(build, result):
    if result == None:
        version = [0, 0, 0]
    else:
        version = (result.get("version")).split(".")
    if build == "patch":
        version[2] =str(int(version[2])+1)
    elif build == "minor":
        version[1] = str(int(version[1])+1)
    elif build == "major":
        version[0] = str(int(version[0])+1)
    __version__ = '.'.join(map(str, version))
    return __version__


def get_version_and_timestamp():
    time_flag = 0
    version_flag = 0
    #if not os.path.exists("/home/ankit/thinktank_project_main/thinktank_project/login_validation/CHANGELOG.txt"):
    if not os.path.isfile("CHANGELOG.txt"):
        return None
    else:
        prev = False
        for line in (open("CHANGELOG.txt").readlines()):
            #if "--" in line:
            #    prev = True
            #    continue
            if prev:
                formatted_timestamp = line.split("\n")[0]
                timestamp = datetime.datetime.strptime(formatted_timestamp, "%Y-%m-%d %H:%M:%S.%f")
                time_flag = 1
                #prev = False
                break
            if  "VERSION" in line:
                splitted_line = line.split(" ",1)
                version = (splitted_line[1]).split("\n")[0]
                version_flag = 1
                prev = True
                #break
        if time_flag == 1 and version_flag == 1:
            return {'version': version, 'timestamp':timestamp}
        else:
            return None

def get_commit_info(timestamp):
    user_list = []
    records = []
    git_dict = {}
    commit_list = []
    if timestamp != None:
        test=subprocess.Popen(["git", "log", "--after="+str(timestamp), "--pretty=format:%H,%an,%ad,%B"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        (out, error) = test.communicate()
        if out:
            for commit in out.split("\n\n"):
                commit_list.append(commit)
                if len(commit.split(","))==4:
                    test1=subprocess.Popen(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit.split(",")[0]], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                    (out1, error) = test1.communicate()
                    file_string = ""
                    for files in out1.split("\n"):
                        if files != "":
                            file_string += files+","
                    git_dict = {"comit_id": commit.split(",")[0], "user": commit.split(",")[1], "timestamp": commit.split(",")[2], "message": commit.split(",")[3], "files_changed": file_string}
                    records.append(git_dict)    

    else:
        test=subprocess.Popen(["git", "log", "--pretty=format:%H,%an,%ad,%B"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        (out, error) = test.communicate()
        if out:
            for commit in out.split("\n\n"):
                commit_list.append(commit)
                if len(commit.split(","))==4:
                    test1=subprocess.Popen(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit.split(",")[0]], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                    (out1, error) = test1.communicate()
                    file_string = ""
                    for files in out1.split("\n"):
                        if files != "":
                            file_string += files+","
                    git_dict = {"comit_id": commit.split(",")[0], "user": commit.split(",")[1], "timestamp": commit.split(",")[2], "message": commit.split(",")[3], "files_changed": file_string}
                    records.append(git_dict)
    return records

def write_data_to_file(returned_data, version):
    flag = 0
    data = ""
    if returned_data != None:
        timestamp = returned_data.get("timestamp")
        with file('CHANGELOG.txt', 'r') as original: data = original.read()
    else:
        timestamp = returned_data
    with open("CHANGELOG.txt", "w") as f:
        out = get_commit_info(timestamp)
        if out:
            f.write("VERSION: " + version+"\n"+ str(datetime.datetime.now()))
            f.write("\n"+"--------------------------")
            f.write("\n\n")
        else:
            f.write("VERSION: " + version+"\n" + str(datetime.datetime.now()))
            f.write("\n"+"--------------------------")
            f.write("\n\n")
            f.write("No commits after "+str(timestamp)+"\n\n"+data)
            sys.exit()
        if out != None:
            row_list=[]
            #import pdb;pdb.set_trace()
            for record in out:
                if "," not in record.get("files_changed"):
                    row=record.get("timestamp") +"("+record.get("user")+"): "+record.get("message")+"\n"+"                                  files_changed: "+record.get("files_changed")+"\n\n"
                    row_list.append(row)
                else:
                    row=record.get("timestamp") +"("+record.get("user")+"): "+record.get("message")+"\n"
                    count = 0
                    for files in record.get("files_changed").split(","):
                        if files != "":
                            if count == 0:
                                row += "                                  files_changed: "+files+"\n"
                                count+=1
                            else:
                                row += "                                                 "+files+"\n"
                            row_list.append(row)    
            for i in row_list:
                f.write(str(i)+"\n"+data)

def get_version_info():
    parser=optparse.OptionParser()
    parser.add_option('--build',action="store",default="none",dest="build")
    (options, args) = parser.parse_args()
    args_list = ["patch", "minor", "major"]
    if "--build" not in sys.argv:
      print ("Please provide build parameter")
      sys.exit()
    elif not any(arg in sys.argv for arg in args_list):
        print("Please provide correct build parameter(patch or minor or major)")
        sys.exit()
    else:
        return options.build

if __name__ == "__main__":
    build = get_version_info()
    returned_data = get_version_and_timestamp()
    version = get_version(build, returned_data)
    write_data_to_file(returned_data, version)
