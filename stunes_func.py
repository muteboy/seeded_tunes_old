#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
#import sys
import os


def cs(cso, s):
	""" shorthand for writing to the CS file with a line feed """
	cso.write(s + "\n")
	return;


def rand_int_list(n, l, u):
	return [random.randint(l, u) for i in range(1, n + 1)];


def rand_biased_bin_list(n, p):
	return [(1 if random.random() < p else 0) for i in range(1, n + 1)];


def write_csound_score_for_instrument(
		fn, inum=1, iname='bass', note_dur=.5, p_length=16,
		freq_list=(1, 2, 3, 4, 5, 6, 7, 8), mask_list=(1, 0, 1, 0, 1, 0, 1, 0),
		amp=20000, octave=5, p6=.02, p7=.01):
	cs = lambda s: [fn.write(s + "\n")]
	inum_str = 'i' + str(inum)
	cs(inum_str + ' ;' + iname)
	cs(';p1	p2	p3	p4	p5	p6	p7')
	cs(';inum	start	dur	iamp	ifrq')
	for i in range(0, p_length):
		p2 = '0' if i == 0 else '+'
		cs(inum_str + '	' + p2 + '	' + str(note_dur) + '	' + '{:05}'.format(amp * mask_list[i]) + '	' + str(
			octave) + '.0' + str(freq_list[i]) + '	' + str(p6) + '	' + str(p7) + ' ; ' + str(i))
	cs(';end of score for i' + str(inum) + ': ' + iname + '\n')
	return;


def file_len(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1;

'''
def random_line_from_file(fname, seed):
	random.seed(seed)
	f = open(fname)
	lines = f.readlines()
	return lines[random.randint(1, file_len(fname))].rstrip("\n\r");
'''

def select_names_from_pool(pool_list, nn=5):
	random.shuffle(pool_list)
	return pool_list[:nn];

'''
def generate_person_name(seed='123', first_name_file='words_names/names_first.txt', surname_file='words_names/names_surnames.txt'):
	return random_line_from_file(first_name_file, seed).title() + ' ' + random_line_from_file(surname_file, seed).title()
'''


'''
def generate_list_of_people(seed, np=3, first_name_file='words_names/names_first.txt', surname_file='words_names/names_surnames.txt'):
	first_name_file_len = file_len(first_name_file)
	surname_file_len = file_len(surname_file)
	fnf = open(first_name_file)
	fnflines = fnf.readlines()
	random.seed(seed)
	snf = open(surname_file)
	snflines = snf.readlines()
	people_list = []
	for i in range(1, np + 1):
		first_name = fnflines[random.randint(1, first_name_file_len)].rstrip("\n\r").title()
		surname = snflines[random.randint(1, surname_file_len)].rstrip("\n\r").title()
		full_name = first_name + " " + surname
		people_list.append(full_name)
	return people_list;
'''

'''
   def generate_nonsense_word_list(nw=5000, seed=1):
	   fn = 'words_names/random_nonsense_words-' + str(nw) + '_seed-' + str(seed) + '.txt'
	   if os.path.exists(fn):
		   print 'Skipping word list creation'
	   else:
		   os.system('touch ' + fn)
		   os.system('./generate_nonsense_word_list.pl ' + str(nw) + ' ' + str(seed) + ' >> ' + fn)
	   f = open(fn)
	   return f.readlines();
'''


def generate_note_lengths(pl=16, scale=4, seed=1):
	""" generates note lengths """
	# returns a random list of floats, always divisible by 0.25
	# number of values 1 > pl
	pl_hi = pl * scale
	random.seed(seed)
	nn = random.randint((pl / 4), pl)
	dividers = sorted(random.sample(xrange(1, pl_hi), nn - 1))
	l1 = [a - b for a, b in zip(dividers + [pl_hi], [0] + dividers)]
	suml1 = sum(l1)
	l2 = [float(x) / float(scale) for x in l1]
	suml2 = sum(l2)
	return l1, suml1, l2, suml2;


def pick_n_words_Titlecase(nw, wlist):
	s = ''
	for i in range(1, nw + 1):
		# s = s + str(nonsense_words[random.randint(1,len(wlist))].rstrip("\n\r").title()) + ' '
		s = s + str(wlist[random.randint(1, len(wlist))].rstrip("\n\r").title()) + ' '
	return s.strip();


def set_settings():
	"set all the setting and variables"
	text_size_artist_name = "x20"
	text_color_artist_name = "black"
	text_size_album_name = "x20"
	text_color_album_name = "black"
	text_size_cat_no = "x15"
	text_color_cat_no = "black"
	text_size_tracklist = "x16"
	text_color_tracklist = "black"
	position_artist_name = "+80+10"
	position_album_name = "111"
	position_cat_no = "111"
	position_tracklist = "111"
	# echo -ne '1/10\r'
	return;
