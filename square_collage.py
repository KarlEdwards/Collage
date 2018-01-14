#!/usr/bin/env python3

# Example Usage:
# python3 square_collage.py image_file_specs

# TODO
# [] Make add_title() more robust and useful in terms of font, size, color, and placement

# Adapted from https://gist.github.com/npenzin/f884aa0258db6cc76639
from PIL import Image, ImageOps, ImageDraw, ImageFont

import os
import sys
import glob
import zlib
import math
import argparse
import numpy as np

# Configuration
FONT_PATH = '~/tensorflow/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf/DejaVuSans-Bold.ttf'
DEFAULT_SIZE = 600
DEFAULT_PADDING = 60
DEFAULT_BACKGOUND_COLOR = '#fafafa'
    
class Collage( object ):
  
    def __init__(self, image_file_specs):
        """initialize"""
        self.images       = image_file_specs
        self.cols         = math.ceil( len( image_file_specs )**0.5 ) 
        self.rows         = self.cols
        self.def_size     = DEFAULT_SIZE
        self.def_pad      = DEFAULT_PADDING
        self.def_bg_color = DEFAULT_BACKGOUND_COLOR
        self.canvas_size  = (
            self.def_size*self.cols + (( self.cols + 1 ) * self.def_pad ),
            self.def_size*self.rows + (( self.rows + 1 ) * self.def_pad ))
        self._create()

    def _create( self ):
        """Build a collage"""
        self.canvas = Image.new( 'RGB', self.canvas_size, self.def_bg_color )
        for img_n, img_fn in enumerate( self.images ):
            # open img
            temp_img = Image.open( img_fn )
            # crop if not square
            temp_img = self._crop_img( temp_img )
            # resize to default size square
            temp_img = temp_img.resize(( DEFAULT_SIZE, DEFAULT_SIZE ), Image.ANTIALIAS )
            # arrange items on the page
            left_margin = img_n % self.cols * ( self.def_size + self.def_pad ) + self.def_pad
            top_margin = img_n // self.cols * ( self.def_size + self.def_pad ) + self.def_pad
            box = ( left_margin, top_margin )
            self.canvas.paste( temp_img, box )
      
    def add_title( self, title ):
        draw = ImageDraw.Draw(self.canvas)
        font = ImageFont.truetype( font = FONT_PATH, size = 40 )
        draw.text(( 1200,10 ), title, 'blue', font = font )

    def _crop_img( self, image_to_crop ):
        """Crop the given image"""
        temp_img = image_to_crop

        # if image is not square, then crop center
        if temp_img.width != temp_img.height:
            if temp_img.width > temp_img.height:
                left = temp_img.width/2 - temp_img.height/2
                upper = 0
                right = temp_img.width/2 + temp_img.height/2
                lower = temp_img.height
                box = ( left, upper, right, lower )
                temp_img = temp_img.crop( box )
            else:
                left = 0
                upper = temp_img.height/2 - temp_img.width/2
                right = temp_img.width
                lower = temp_img.height/2 + temp_img.width/2
                box = ( left, upper, right, lower )
                temp_img = temp_img.crop( box )

        return temp_img

    def show( self ):
        """Show the collage"""
        self.canvas.show()
        return

    def save_to_file( self, file_name ):
        """Save the collage to a file"""
        img = self.canvas
        img.save( file_name )
        img.close()
        return
