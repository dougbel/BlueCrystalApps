# hello_mpi.py:
# usage: python hello_mpi.py

from mpi4py import MPI
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--argument', required=True)

opt = parser.parse_args()

def print_hello(rank, size, name, arg):
  msg = "Hello World! I am FIRST process {0} of {1} on {2}. Argument {3}.\n"
  sys.stdout.write(msg.format(rank, size, name, arg))

if __name__ == "__main__":
  size = MPI.COMM_WORLD.Get_size()
  rank = MPI.COMM_WORLD.Get_rank()
  name = MPI.Get_processor_name()

  print_hello(rank, size, name, opt.argument)
