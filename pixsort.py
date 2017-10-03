#!/usr/bin/env python3

from PIL import Image

import numpy
import sys

def calculate_ranges(image, per_column=False):
  pixels        = image.load()
  width, height = image.size
  result        = list()

  if per_column:
    for x in range(width):
      data = list()

      for y in range(height):
        data.append( pixels[x,y] )

      result.append( max(data) - min(data) )
  else:
    for y in range(height):
      data = list()

      for x in range(width):
        data.append( pixels[x,y] )

      result.append( max(data) - min(data) )

  return result

def sort(image, index, per_column=False):
  pixels        = image.load()
  width, height = image.size

  relevant_pixels = list()
  if per_column:
    for y in range(height):
      relevant_pixels.append( pixels[index,y] )
  else:
    for x in range(width):
      relevant_pixels.append( pixels[x,index] )

  relevant_pixels.sort(reverse=True)

  if per_column:
    for (y,p) in zip(range(height), relevant_pixels):
      pixels[index,y] = p
  else:
    for (x,p) in zip(range(width), relevant_pixels):
      pixels[x,index] = p

  return image

if __name__ == "__main__":
  image   = Image.open(sys.argv[1])
  ranges  = calculate_ranges(image)
  indices = numpy.argsort(ranges)

  # TODO: make configurable
  n = 500

  for i in range(n):
    image = sort(image, int(indices[i]))

  image.show()
