# -*- coding: utf-8 -*-

import logging
import os, atexit, json

__author__ = 'Takashi SASAKI'
globalState = None


def initGlobalState():
    global globalState
    globalState = {
        "foundGitRepositories": [],
        "directoryStack": ["C:\\"],
        "nVisitedDirectories": 0
    }


def saveGlobalState():
    f = open("globalState", "w")
    json.dump(globalState, f)
    print("SAVE: " + json.dumps(globalState))


def loadGlobalState():
    try:
        f = open("globalState", "r")
    except IOError as e:
        return
    globalState = json.load(f)
    print("LOAD: " + json.dumps(globalState))

def popDirectory(directory_stack):
    # print(directory_stack)
    for root, dirs, files in os.walk(directory_stack[0]):
        new_directories = []
        for d in dirs:
            if d == "$Recycled.Bin": continue
            new_directories.append(os.path.join(directory_stack[0], d))
        return directory_stack[0], dirs, files, new_directories
    raise IOError("Can't get directories for %s" % directory_stack[0])

def main():
    directory_stack = globalState["directoryStack"]
    found_git_repositories = globalState["foundGitRepositories"]
    n_visited_directories = globalState["nVisitedDirectories"]
    count = 0
    while len(directory_stack) > 0:
        try:
            root, dirs, files, new_directories = popDirectory(directory_stack)
        except IOError as e:
            directory_stack = directory_stack[1:]
            continue
        n_visited_directories += 1
        if ".git" in dirs:
            found_git_repositories.append(root)
            directory_stack = directory_stack[1:]
        else:
            directory_stack = new_directories + directory_stack[1:]
        count += 1
        if count >= 5000:
            count = 0
            globalState["directoryStack"] = directory_stack
            globalState["foundGitRepositories"] = found_git_repositories
            globalState["nVisitedDirectories"] = n_visited_directories
            saveGlobalState()
    saveGlobalState()


def printResult():
    global globalState
    for x in globalState["foundGitRepositories"]:
        print(x)


def aborted1():
    print("中断しちゃいましたよ")


if __name__ == "__main__":
    atexit.register(saveGlobalState)
    initGlobalState()
    loadGlobalState()
    main()
    printResult()
    saveGlobalState()