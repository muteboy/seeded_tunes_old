#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" main module for outputting to dot """


class DotOutput(object):
	""" GraphViz Output """

	@staticmethod
	def dot_write_label(ld, dotfile):
		""" write dot file header for label """
		dotfile.body.append('// Label: {}'.format(ld['label_name']))
		dotfile.attr('graph', splines='ortho')
		dotfile.attr('graph', rankdir='LR')
		dotfile.attr('node', shape='record', height='2', width='2')
		dotfile.node('test_record', r'hello\nworld |{ <there> b |{c|<here> d|e}| f}| g | h')
		dotfile.edge('test_record:here', 'test_record:there')
		dotfile.attr('node', fixedsize='true', width='1.5', height='1.5', shape='box',
		             style='filled', color='lightgrey', fontname='FreeSans')
		dotfile.node(str(ld['label_seed']), str(ld['label_name']).replace(' ', '\n'))
		return

	@staticmethod
	def dot_write_artist(ad, ld, dotfile):
		""" write dot for artist """
		dotfile.body.append('// Artist {}/{}: {}'.
		                    format(ad['artist_id'], ld['num_artists'], ad['artist_name']))
		dotfile.node(str(ad['artist_seed']), str(ad['artist_name']).replace(' ', '\n'))
		dotfile.edge(str(ld['label_seed']), str(ad['artist_seed']))
		return

	@staticmethod
	def dot_write_album(ald, ad, dotfile):
		""" write dot for album """
		dotfile.body.append('// Album {}/{}: {}'.
		                    format(ald['album_id'], ad['num_albums'], ald['album_name']))
		dotfile.node(str(ald['album_seed']), str(ald['album_name']).replace(' ', '\n'))
		# TODO MAKE START OF TABLE NODE WITH TRACKS
		dotfile.edge(str(ad['artist_seed']), str(ald['album_seed']))
		return
