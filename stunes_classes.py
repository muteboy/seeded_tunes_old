#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" main module for defining classes """

import random
import datetime
import os
import stunes_func
import sys


class Label(object):
	""" a record label """

	def __init__(self, label_year_start):
		self.label_seed = 1006721
		random.seed(self.label_seed)
		self.label_name = 'Seed ' + str(self.label_seed) + ' Recordings'
		self.label_year_start = label_year_start
		self.label_year_end = random.randint(self.label_year_start + 1, datetime.datetime.now().year)
		# self.num_artists = random.randint(1, 10) - Force number for debugging
		self.num_artists = 1
		self.label_path = self.label_name.replace(" ", "_")
		return

	@staticmethod
	def folders(path):
		""" delete and create folders """
		os.system('rm -r {}/'.format(path))
		os.system('mkdir {}'.format(path))
		return


class WordsAndNames(object):
	""" word and name lists """

	@staticmethod
	def nonsense_word_list(seed, nw=5000):
		""" generate word list """
		fn = 'words_names/random_nonsense_words-' + str(nw) + '_seed-' + str(seed) + '.txt'
		if os.path.exists(fn):
			print 'Skipping word list creation'
		else:
			os.system('touch ' + fn)
			os.system('./generate_nonsense_word_list.pl ' + str(nw) + ' ' + str(seed) + ' >> ' + fn)
		f = open(fn)
		return f.readlines();

	@staticmethod
	def label_people_list(seed, num_artists,
	                      first_name_file='words_names/names_first.txt',
	                      surname_file='words_names/names_surnames.txt'):
		""" generate people list """
		first_name_file_len = stunes_func.file_len(first_name_file)
		surname_file_len = stunes_func.file_len(surname_file)
		fnf = open(first_name_file)
		fnflines = fnf.readlines()
		random.seed(seed)
		snf = open(surname_file)
		snflines = snf.readlines()
		people_list = []
		for i in range(1, num_artists + 1):
			people_list.append(fnflines[random.randint(1, first_name_file_len)].rstrip("\n\r").title() +
			                   " " +
			                   snflines[random.randint(1, surname_file_len)].rstrip("\n\r").title())
		return people_list

	@staticmethod
	def list_of_artist_members(pool_list, nn=5):
		""" select a few names from the pool to be the band members """
		random.shuffle(pool_list)
		return pool_list[:nn]

