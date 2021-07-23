#!/usr/bin/env python3

import click
import numpy as np
import gatetools as gt
import pydicom
import os

# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-o', '--output', default='output', help='Output folder to save dicom')
@click.option('-v', '--value', default=0, help='New value')
@click.option('-N', '--sliceposition', default=0.0, help='Position of slice to erase along z')
@click.argument('input', type=str, required=True, nargs=-1)
def erasePatientFace_main(input, output, value, sliceposition):
    '''
    Set to "value" the slice >= sliceposition along z to erase patient face in the image
    '''
    erasePatientFace(input, output, value, sliceposition)

def erasePatientFace(input, output, value, sliceposition):
    #Read input
    series = gt.separate_series(input)
    key = list(series.keys())[0]
    for file in series[key]:
      slice = pydicom.read_file(file)
      if slice[0x0020, 0x0032][2] >= sliceposition:
        arr = slice.pixel_array
        arr[:] = value
        slice.PixelData = arr.tobytes()
      slice.save_as(os.path.join(output, file))

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    erasePatientFace_main()

