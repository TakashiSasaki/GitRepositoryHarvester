# -*- coding: utf-8 -*-

import os
import atexit
import json

__author__ = 'Takashi SASAKI'
globalState = None


def initGlobalState():
    global globalState
    globalState = {
        "foundGitRepositories": [],
        "foundBzrRepositories": [],
        "foundSvnRepositories": [],
        "directoryStack": ["C:\\"],
        "nVisitedDirectories": 0
    }


def saveGlobalState():
    global globalState
    f = open("globalState", "w", encoding="utf_8")
    json.dump(globalState, f, ensure_ascii=False)
    print("SAVE: " + json.dumps(globalState))


def loadGlobalState():
    global globalState
    try:
        f = open("globalState", "r", encoding="utf_8")
    except IOError as e:
        return
    globalState.update(json.load(f))
    print("LOAD: " + json.dumps(globalState))


def popDirectory(directory_path):
    # print(directory_stack)
    for root, dirs, files in os.walk(directory_path):
        new_directories = []
        for d in dirs:
            if d == "$Recycled.Bin": continue
            new_directories.append(os.path.join(directory_path, d))
        return directory_path, dirs, files, new_directories
    raise IOError("Can't get directories for %s" % directory_path)


def main():
    global globalState
    directory_stack = globalState["directoryStack"]
    found_git_repositories = globalState["foundGitRepositories"]
    found_svn_repositories = globalState["foundSvnRepositories"]
    found_bzr_repositories = globalState["foundBzrRepositories"]
    n_visited_directories = globalState["nVisitedDirectories"]
    count = 0
    while len(directory_stack) > 0:
        if directory_stack[0] == "C:\\Windows":
            directory_stack = directory_stack[1:]
            continue
        if directory_stack[0] == "C:\\WindowsESD":
            directory_stack = directory_stack[1:]
            continue
        if directory_stack[0] == "C:\\Program Files":
            directory_stack = directory_stack[1:]
            continue
        if directory_stack[0] == "C:\\Program Files (x86)":
            directory_stack = directory_stack[1:]
            continue
        if directory_stack[0] == "C:\\w32tex":
            directory_stack = directory_stack[1:]
            continue

        try:
            root, dirs, files, new_directories = popDirectory(directory_stack[0])
        except IOError as e:
            directory_stack = directory_stack[1:]
            continue
        n_visited_directories += 1
        if ".git" in dirs:
            found_git_repositories.append(root)
            directory_stack = directory_stack[1:]
        elif ".svn" in dirs:
            found_svn_repositories.append(root)
            directory_stack = directory_stack[1:]
        elif ".bzr" in dirs:
            found_bzr_repositories.append(root)
            directory_stack = directory_stack[1:]
        else:
            directory_stack = new_directories + directory_stack[1:]
        count += 1
        if count >= 5000:
            count = 0
            globalState["directoryStack"] = directory_stack
            globalState["foundGitRepositories"] = found_git_repositories
            globalState["foundBzrRepositories"] = found_bzr_repositories
            globalState["foundSvnRepositories"] = found_svn_repositories
            globalState["nVisitedDirectories"] = n_visited_directories
            saveGlobalState()
    saveGlobalState()


def printResult():
    f = open("foundGitRepositories.txt", "w", encoding="utf_8")
    global globalState
    for x in globalState["foundGitRepositories"]:
        f.write(x + "\n")
    f = open("foundBzrRepositories.txt", "w", encoding="utf_8")
    global globalState
    for x in globalState["foundBzrRepositories"]:
        f.write(x + "\n")
    f = open("foundSvnRepositories.txt", "w", encoding="utf_8")
    global globalState
    for x in globalState["foundSvnRepositories"]:
        f.write(x + "\n")


def aborted1():
    print("中断しちゃいましたよ")


if __name__ == "__main__":
    atexit.register(saveGlobalState)
    initGlobalState()
    loadGlobalState()
    main()
    printResult()
    saveGlobalState()