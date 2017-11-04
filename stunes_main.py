#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" main module for generating a label's worth of artists, albums and tracks in CSound format """

import datetime
import os
import random
import logging

from graphviz import Digraph

import stunes_func
import stunes_instr
import stunes_gfx
import stunes_dot
import stunes_classes


def cs(s):
	""" simpler writing to file """
	cso.write(s + "\n")
	return


label = stunes_classes.Label(1972)
label.folders(label.label_path)

# CREATE WORDS AND NAMES

wordsandnames = stunes_classes.WordsAndNames()
nonsense_words = wordsandnames.nonsense_word_list(seed=label_data['label_seed'], nw=5000)
label_people = stunes_func.generate_list_of_people(seed=label_data['label_seed'],
                                                   np=label_data['num_artists'] * 3)

# CREATE LABEL GRAPHICS
stunes_gfx.im_text_label(rot=270, ps=20, font='FreeSans-Bold',
                         text=label_data['label_name'], folder=label_data['label_path'],
                         fn='label_name.png')

# label logo
# TODO change cover sidebar width?
stunes_gfx.im_seed_logo(label_data['label_path'], text=label_data['label_seed'])

# start dot for GraphViz
dotfile = Digraph(comment=label_data['label_name'])
stunes_dot.dot_write_label(label_data, dotfile)

# initialise data
label_discography = []

# LOOP THROUGH ARTISTS #
for artist_id in range(1, label_data['num_artists'] + 1):
	# TODO create the data structures, then go through and create the files.
	logging.debug('Artist %s of %s', artist_id, label_data['num_artists'] + 1)
	artist_seed = int(str(label_data['label_seed']) + '{:02}'.format(artist_id))
	random.seed(artist_seed)
	artist_data = {
		'artist_seed':       artist_seed,
		'artist_id':         artist_id,
		'num_albums':        random.randint(1, 10),
		'num_members':       random.randint(1, 5),
		'artist_name':       stunes_func.pick_n_words_Titlecase(wlist=nonsense_words,
		                                                        nw=random.randint(1, 2)),
		'artist_year_start': random.randint(label_data['label_year_start'], label_data['label_year_end']),
	}
	artist_data['artist_year_end'] = random.randint(artist_data['artist_year_start'], label_data['label_year_end'])
	artist_data['artist_path'] = '{:02}_{}'.format(artist_data['artist_id'], artist_data['artist_name']).replace(" ", "_")
	artist_data['artist_people'] = WordsAndNames.list_of_artist_members(label_people, nn=artist_data['num_members'])

	# FORCE FOR DEBUGGING
	artist_data['num_albums'] = 1

	# set progress
	artist_progress = '{}/{}'.format(artist_data['artist_id'], label_data['num_artists'])
	print 'Artist', artist_progress

	# create artist folder
	os.system('mkdir {0}/{1}'.format(label_data['label_path'], artist_data['artist_path']))

	# write artist data to dot file
	stunes_dot.dot_write_artist(artist_data, label_data, dotfile)

	# artist graphics
	stunes_gfx.im_text_label(rot=0, font='FreeSans-Bold', text=artist_data['artist_name'],
	                         folder='{}/{}'.format(label_data['label_path'], artist_data['artist_path']),
	                         fn='artist_name.png')

	# add artist data to label discography
	label_discography.append(artist_data)

	# LOOP THROUGH ALBUMS FOR THIS ARTIST
	for album_id in range(1, artist_data['num_albums'] + 1):
		album_seed = int(str(artist_seed) + '{:02}'.format(album_id))
		random.seed(album_seed)
		# num_tracks = random.randint(3, 10)
		album_data = {
			'artist_seed': artist_data['artist_seed'],
			'album_seed':             album_seed,
			'album_id':               album_id,
			'num_tracks':             random.randint(3, 10),
			'album_name':             stunes_func.pick_n_words_Titlecase(wlist=nonsense_words,
			                                                             nw=random.randint(1, 2)),
			'tracklist':              []
		}

		# FORCE FOR DEBUGGING
		album_data['num_tracks'] = 2

		if album_data['num_tracks'] < 5:
			album_data['album_name'] += ' EP'

		album_data['album_cat_no'] = 'SR{0}{1}'.format(str(artist_data['artist_seed']), str(album_data['album_id']))
		album_data['album_path'] = '{:02}_{}'.format(album_data['album_id'], album_data['album_name']).replace(" ", "_")
		album_data['album_path_full'] = '{}/{}/{}/'.format(label_data['label_path'],
		                                                   artist_data['artist_path'],
		                                                   album_data['album_path'])

		# set progress
		album_progress = '{}/{}'.format(album_data['album_id'], artist_data['num_albums'])
		print 'Artist {} Album {}'.format(artist_progress, album_progress)

		# create album folder
		os.system('mkdir {0}/{1}/{2}'.format(label_data['label_path'], artist_data['artist_path'], album_data['album_path']))

		# write album data to dot file
		stunes_dot.dot_write_album(album_data, artist_data, dotfile)

		# CREATE ALBUM ARTWORK
		# album name
		stunes_gfx.im_text_label(rot=0, text=album_data['album_name'],
		                         folder=album_data['album_path_full'],
		                         fn='album_name.png')

		# album catalog number
		stunes_gfx.im_text_label(rot=270, ps=14, text=album_data['album_cat_no'],
		                         folder=album_data['album_path_full'],
		                         fn='album_cat_no.png')

		# album sidebar
		# TODO generate random colour using old algorithm - per artist
		os.system('convert -size 200x1000 canvas:{0} '
		          '{1}album_sidebar.png'.format('snow1', album_data['album_path_full']))

		# random artwork
		# TODO pull in art generator from tapeworm
		stunes_gfx.im_artwork(folder=album_data['album_path_full'])

		# track list
		# TODO proper tracklist
		os.system('convert -background transparent -fill black '
		          '-font FreeSans -pointsize 18 -size 300x '
		          'caption:"{0}" {1}album_tracklist.png'
		          .format('1. Track A  2. Track B  3. Track C  4. Track D  '
		                  '2. Track B  3. Track C  4. Track D  2. Track B  '
		                  '3. Track C  4. Track D', album_data['album_path_full']))

		# combine all artwork into final
		os.system('convert -size 1000x1000 xc:snow1 '
		          '-page +0+0 {0}album_sidebar.png -page +200+300 {0}album_artwork.png '
		          '-page +200+50 {1}/{2}/artist_name.png -page +75+425 {1}/label_name.png '
		          '-page +100+425 {0}album_cat_no.png -page +50+300 {1}/seed_logo_labelled.png '
		          '-page +200+100 {0}album_name.png -page +650+50 {0}album_tracklist.png '
		          '-layers flatten {0}album_art_final.png'
		          .format(album_data['album_path_full'],
		                  label_data['label_path'],
		                  artist_data['artist_path']))

		os.system('convert {0}album_art_final.png -colorspace gray '
		          '\( +clone -blur 0x1 \) +swap -compose divide '
		          '-composite -linear-stretch 5%x0% -rotate 0.2 '
		          '{0}album_art_final.png'.format(album_data['album_path_full']))

		# TODO make list of tracks to be added to the album
		# TODO - make changes in band members for each album?

		# LOOP THROUGH TRACKS
		for track_id in range(1, int(album_data['num_tracks']) + 1):
			track_seed = int(str(album_seed) + '{:02}'.format(track_id))
			random.seed(track_seed)
			track_data = {
				'track_id':    track_id,
				'track_seed':  track_seed,
				'track_title': '{:02}'.format(track_id) + ' ' + stunes_func.pick_n_words_Titlecase(
						wlist=nonsense_words, nw=random.randint(1, 2)),
				'track_tempo': random.randint(120, 220),
			}

			# set progress
			track_progress = '{}/{}'.format(track_data['track_id'], album_data['num_tracks'])
			print 'Artist {} album {} track {}'.format(artist_progress, album_progress, track_progress)

			album_data['tracklist'].append(track_data['track_title'])

			os.system('mkdir -p ' + album_data['album_path_full'])
			track_sco_fn = '{0}{1}.sco'.format(album_data['album_path_full'], track_data['track_title']).replace(" ", "_")
			pattern_list_length = 4

			# write score file
			# TODO print status throughout to find image error
			with open(track_sco_fn, 'w+') as cso:
				# PUT THE FORMATTED STUFF HERE
				cs(';Label:  ' + label_data['label_name'])
				cs(';Artist: ' + artist_data['artist_name'])
				cs(
						';Years active: ' +
						str(artist_data['artist_year_start']) +
						'-' +
						str(artist_data['artist_year_end'])
				)
				cs(';Album: ' + album_data['album_name'])
				cs(';Track: ' + track_data['track_title'])
				cs(';')
				cs(';note lengths: ' + str(stunes_func.generate_note_lengths()))
				# print '\n\n', seeded_tunes_functions.generate_note_lengths(), '\n\n'
				# TODO - WHAT TO DO WITH NOTE LENGTHS? STILL NEED MASK
				cs(';')
				cs(';function table definition')
				cs(';p1	p2	p3	p4	p5	p6	p7')
				cs(';ftnum	acttim	size	gen	gen specific')
				cs('f1	0	2048	10	1	1	1	1	.7	.5	.3	.1	;pulse')
				cs('f2	0	1024	10	1')
				cs('')
				cs(';tempo')
				cs('t	0	' + str(track_data['track_tempo']))
				cs('')
				cs(';instrument score')
				for i in range(0, len(stunes_instr.instruments_dict)):
					steps_in_pattern = int(pattern_list_length / stunes_instr.instruments_dict[i]['dur'])
					note_list = stunes_func.rand_int_list(steps_in_pattern, 1, 9)
					# note lengths
					note_mask = (stunes_func.rand_biased_bin_list(steps_in_pattern,
					                                              stunes_instr.
					                                              instruments_dict[i]['density'])
					             )
					stunes_func.write_csound_score_for_instrument(
							fn=cso,
							inum=stunes_instr.instruments_dict[i]['inum'],
							iname=stunes_instr.instruments_dict[i]['iname'],
							note_dur=stunes_instr.instruments_dict[i]['dur'],
							p_length=steps_in_pattern,
							freq_list=note_list,
							mask_list=note_mask,
							octave=stunes_instr.instruments_dict[i]['octave'],
							amp=stunes_instr.instruments_dict[i]['amp'],
					)
				cs(';Raw generated data')
				cs(';------------------')
				cs(';label data: ' + str(label_data))
				cs(';artist data: ' + str(artist_data))
				cs(';album data: ' + str(album_data))
				cs(';track data: ' + str(track_data))
				cs(';------------------')
				cs(';end of file writing loop')


# print label_discography, "yay"

# RENDER LABEL GRAPH
# TODO - get dot looking right
dotfile.render('gv_output.gv', view=False)

# TODO - ANALYZE ARTIST PRODUCTIVITY
# TODO generate release ads for albums - like klf - use IM to make old looking


# TODO - RENDER AND PLAY CSOUND
# os.system('csound -H2 -o' + file_stem + '.wav ' + file_stem + '.orc ' + file_stem + '.sco')
# os.system('play ' + file_stem + '.wav')
