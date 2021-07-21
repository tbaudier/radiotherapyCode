#!/usr/bin/env python3

import click
import itk


# -----------------------------------------------------------------------------
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--image', default='.', help='Input image to erase (mhd)')
@click.option('-o', '--output', default='.', help='Output image (mhd)')
@click.option('-v', '--value', default=-1024, help='New value')
@click.option('-N', '--slice', default=1, help='Number of slice to erase')
def erasePatientFace_main(image, output, value, slice):
    '''
    Set to "value" the first N slices along z to erase patient face in the image
    '''
    erasePatientFace(image, output, value, slice)

def erasePatientFace(image, output, value, slice):
  imageITK = itk.imread(image)
  imageArray = itk.array_from_image(imageITK)
  imageArray[-slice+1:, :, :] = value
  outputITK = itk.image_from_array(imageArray)
  outputITK.CopyInformation(imageITK)
  itk.imwrite(outputITK, output)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    erasePatientFace_main()
