#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" module for generating graphic components for album artwork """
import os

# TODO pull in various art styles, randomly choose
# TODO random color for sidebar?


def im_text_label(ps=32, font='FreeSans', rot=0, text='No text provided', folder='.', fn='text'):
	""" use ImageMagick to create a text label image """
	os.system('convert -background transparent -fill black -font {} -pointsize {} '
	          '-rotate {} label:"{}" {}/{}'.format(font, ps, rot, text, folder, fn))
	return


def im_seed_logo(path='.', text='ABCDEFGH'):
	""" generate label logo image"""
	os.system('convert -size 100x100 xc:transparent -antialias -fill none '
	          '-stroke black -strokewidth 6 -draw "circle 50,50 22,22 '
	          'path \'M 56,20 C 48,43 45,62 47,77 M 56,20 C 66,25 77,79 47,77 17,75 26,35 56,20\'" '
	          '{0}/seed_logo.png'.format(path))
	os.system('convert {0}/seed_logo.png -font FreeSans -gravity South -background transparent '
	          '-splice 0x18 -annotate +0+2 "{1}" {0}/seed_logo_labelled.png'.format(path, text))
	return


def im_artwork(size='800x700',
               imcmd='-channel G +noise Random '
                     '-virtual-pixel Tile -blur 0x8 '
                     '-auto-level -separate +channel '
                     '-ordered-dither threshold,3 ', folder='.'):
	""" use ImageMagick to create abstract artwork """
	os.system('convert -size {} xc: {} {}/album_artwork.png'.format(size, imcmd, folder))
	return
