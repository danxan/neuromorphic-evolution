#!/bin/python3
import sys
import getch
import argparse
import time

class Screen():
    def __init__(self):
        self.last_lines = []

    def print(self, s):
        if len(self.last_lines) > 0:
            print("\033["+str(len(self.last_lines)+1)+"A", flush=True)

        lines = s.split('\n')
        self.last_lines = lines

        for l in lines:
            print(l)

    def get_input(self):
        return  getch.getch()
