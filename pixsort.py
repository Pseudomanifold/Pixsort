#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFilter

import numpy
import sys

def get_row_or_column(image, index, get_row=True):
  pixels        = image.load()
  width, height = image.size

  data = list()
  if get_row:
    for x in range(width):
      data.append( pixels[x,index] )
  else:
    for y in range(height):
      data.append( pixels[index,y] )

  return data

def set_row_or_column(image, index, data, set_row=True):
  pixels        = image.load()
  width, height = image.size

  if set_row:
    for x in range(width):
      pixels[x,index] = data[x]
  else:
    for y in range(height):
      pixels[index,y] = data[y]

  return image

def calculate_variabilities(image, per_row=True):
  width, height = image.size
  n             = height if per_row else width
  result        = list()

  for i in range(n):
    data = numpy.array(get_row_or_column(image, i, per_row))
    mean = numpy.mean(data)
    data = data - mean
    data = abs(data)

    result.append( -numpy.sum(data) )

  return result

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

def sort(image, index, per_row=True):
  edges         = image.filter(ImageFilter.FIND_EDGES)
  pixels        = image.load()
  width, height = image.size

  data = get_row_or_column(image, index, per_row)
  data.sort(reverse=True)

  image = set_row_or_column(image, index, data, per_row)
  return image

if __name__ == "__main__":
  image         = Image.open(sys.argv[1])
  ranges        = calculate_ranges(image)
  variabilities = calculate_variabilities(image)
  indices       = numpy.argsort(variabilities)

  # TODO: make configurable
  n = 50

  for i in range(n):
    image = sort(image, int(indices[i]))

  image.show()
