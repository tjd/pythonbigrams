# bigrams.py

#
# This code demonstrates how bigrams, pairs of consecutive words, can be used
# to create auto-complete suggestions for the next word to type.
#
# The idea is to take some text (lots and lots of it!) and count how many
# times each bigram occurs. Then, for instance, if someone types the word 'I',
# we can suggest as the next word the second word in the most frequent bigram
# starting with 'I'.
#
# THis program was written to be as easy to understand as possible. It's *not*
# particularly efficient, and could be sped up and improved in many ways.
#

# Returns a list of all the words in the given file.
def get_words(fname):
	words = open(fname, 'r').read().lower().split()
	return words

# Converts a list of words into a list of bigrams
# e.g. ['once', 'upon', 'a', 'time'] gives the bigrams
# [('once', 'upon'), ('upon', 'a'), ('a', 'time')]
def make_bigrams(words):
	result = []
	for i in range(1, len(words)):
		result.append((words[i-1], words[i]))
	return result

# Given a list of bigrams, returns a dictionary of bigrams and their counts.
def count_bigrams(bigrams):
	result = {}
	for bg in bigrams:
		if bg in result:
			result[bg] += 1
		else:
			result[bg] = 1
	return result

# Given a dictionary of bigram counts, returns a list of (count, bigram) pairs
# in order from highest count to lowest count.
def sort_bigram_counts(bg_count):
	result = [(bg_count[w], w) for w in bg_count]
	result.sort()
	result.reverse()
	return result

# Returns the total number of bigrams in the given sorted list of (count,
# bigram) pairs where w is the first word of the bigram.
def num_start_with(w, counts):
	return sum(cp[0] for cp in counts if cp[1][0] == w)

# Given a words and a sorted list of (count, bigram) pairs, returns a list of
# the words that most frequently follow word.
def suggest_next(word, counts, num_suggestions=5):
	# get first num_suggestions (count, bigram) pairs that start with word
	result = [(c, bg) for (c, bg) in counts if bg[0] == word]
	return result[:num_suggestions]


# The function below is a slightly more efficient version of suggest_next that
# stops searching the list as soon as it finds num_suggestions matches.
#
# def suggest_next(word, counts, num_suggestions=5):
# 	# get first num_suggestions (count, bigram) pairs that start with word
# 	result = []
# 	for (c, bg) in counts:
# 		if bg[0] == word:
# 			result.append((c,bg))
# 			if len(result) == num_suggestions:
# 				break
# 	return result

# Shows most popular suggestions (and their counts) for word w.
# counts is a sorted list of (count, bigram) pairs
def report_info(w, counts):
	# get all the bigrams that start with w
	w_total = num_start_with(w, counts)
	w_pairs = suggest_next(w, counts)
	print(f'\n{w_total} bigrams start with "{w}"')

	# show bigrams that start with w, most frequent first
	for (c, bg) in w_pairs:
		print(f'{bg[0]} {bg[1]} ({100*c/w_total:.1f}%, {c})')

# Returns the word that appears most frequently after w.
# counts is a sorted list of (count, bigram) pairs
def get_most_freq_after(w, counts):
	for (c, bg) in counts:
		if bg[0] == w:
			return bg[1]
	return ''

# Returns sequence of most likely words beginning with start_word.
# counts is a sorted list of (count, bigram) pairs
def word_sequence(start_word, counts, length=5):
	result = [start_word]
	w = start_word
	for i in range(length):
		next_word = get_most_freq_after(w, counts)
		result.append(next_word)
		w = next_word
	return result

# counts is a sorted list of (count, bigram) pairs
def interact(counts):
	print()
	print('Commands:')
	print('   info <word>  # show most frequent next words')
	print('   seq <word>   # sequence of 5 most frequent words')
	print('   quit         # end the session')
	print()
	while True:
		terms = input('--> ').strip().lower().split(' ')
		n = len(terms)
		if n == 0 or n > 2:
			print(f'invalid command: {terms}')
		elif n == 1:
			if terms[0] == 'quit':
				return
			else:
				print(f'unknown command: {terms[0]}')
		else: # n == 2
			if terms[0] == 'info':
				report_info(terms[1], counts)
			elif terms[0] == 'seq':
				print(' '.join(word_sequence(terms[1], sorted_counts)))
			else:
				print(f'unknown command: {terms[0]}')

if __name__ == '__main__':
	fname = 'bill_complete.txt'
	words = get_words(fname)
	print(f'... {len(words)} total words read from {fname}')

	bigrams = make_bigrams(words)
	print(f'... {len(bigrams)} bigrams')
	
	bg_count = count_bigrams(bigrams)
	print(f'... {len(bg_count)} distinct words')

	print('sorting ...')
	sorted_counts = sort_bigram_counts(bg_count)
	print('... done sorting')

	interact(sorted_counts)

	# # # look at suggestions for a few words
	# test_words = 'i why who good happy love hate sad bad evil king queen god man woman romeo juliet'.split()
	# for w in test_words:
	# 	print(word_sequence(w, sorted_counts))
	# 	# report_info(w, sorted_counts)
