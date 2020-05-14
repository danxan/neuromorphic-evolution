#!/bin/python3
import sys
import getch
import argparse
import time

class Screen2():
    def __init__(self):
        self.last_lines = []

    def clear(self):
        if len(self.last_lines) > 0:
            print("\033["+str(len(self.last_lines)+1)+"A", flush=True)

    def print(self, s):

        lines = str(s).split('\n')
        self.last_lines += lines

        for l in lines:
            print(l.replace("0.", "++").replace("1.", "##"))


    def get_input(self):
        return  getch.getch()

class Screen():
    def __init__(self):
        self.last_lines = []

    def print(self, s):
        if len(self.last_lines) > 0:
            print("\033["+str(len(self.last_lines)+1)+"A", flush=True)

        lines = str(s).split('\n')

        self.last_lines = lines

        for l in lines:
            print(l.replace("0.", "++").replace("1.", "##"))


    def get_input(self):
        return  getch.getch()
