import os
import sys
from ete3 import Tree
import traceback
from collections import defaultdict
import logging 
from operator import itemgetter
import subprocess
import random

def createLoggerObject(log_file):
	"""
	Description:
	This function creates a logging object.
	********************************************************************************************************************
	Parameters:
	- log_file: Path to file to which to write logging.
	********************************************************************************************************************
	Returns:
	- logger: A logging object.
	********************************************************************************************************************
	"""

	logger = logging.getLogger('task_logger')
	logger.setLevel(logging.DEBUG)
	# create file handler which logs even debug messages
	fh = logging.FileHandler(log_file)
	fh.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M")
	fh.setFormatter(formatter)
	logger.addHandler(fh)
	return logger

def runCmd(cmd, logObject, check_files=[], check_directories=[], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL):
	if logObject != None:
		logObject.info('Running %s' % ' '.join(cmd))
	try:
		subprocess.call(' '.join(cmd), shell=True, stdout=stdout, stderr=stderr,
						executable='/bin/bash')
		for cf in check_files:
			assert (os.path.isfile(cf))
		for cd in check_directories:
			assert (os.path.isdir(cd))
		if logObject != None:
			logObject.info('Successfully ran: %s' % ' '.join(cmd))
	except:
		if logObject != None:
			logObject.error('Had an issue running: %s' % ' '.join(cmd))
			logObject.error(traceback.format_exc())
		raise RuntimeError('Had an issue running: %s' % ' '.join(cmd))

def closeLoggerObject(logObject):
	"""
	Description:
	This function closes a logging object.
	********************************************************************************************************************
	Parameters:
	- logObject: A logging object.
	********************************************************************************************************************
	"""

	handlers = logObject.handlers[:]
	for handler in handlers:
		handler.close()
		logObject.removeHandler(handler)

def determineBranchSumForGroup(species_tree_file, group_genomes):
	try:
		t = Tree(species_tree_file) 
		t.prune(group_genomes)
		phylo_breadth = 0.0
		for n in t.traverse('postorder'):
			phylo_breadth += n.dist
		return(phylo_breadth)
	except:
		sys.stderr.write(traceback.format_exc() + '\n')
		sys.exit(1)

def determineOgCount(genome_ogs, group_genomes, core_genome=80.0):
	try:
		og_counts = defaultdict(int)
		for g in group_genomes:
			for og in genome_ogs[g]:
				og_counts[og] += 1
		tot_genomes = len(group_genomes)
		
		core_ogs = set([])
		for og in og_counts:
			og_prop = og_counts[og]/float(tot_genomes)
			if (og_prop*100.0) >= core_genome:
				core_ogs.add(og)

		all_ogs = set([])
		aux_ogs = set([])
		for g in group_genomes:
			all_ogs = all_ogs.union(genome_ogs[g])
			aux_ogs = aux_ogs.union(genome_ogs[g].difference(core_ogs))
		
		tot_ogs = len(all_ogs)
		tot_aux_ogs = len(aux_ogs)

		return([tot_aux_ogs, tot_ogs])
		
	except:
		sys.stderr.write(traceback.format_exc() + '\n')
		sys.exit(1)

def determineClosestRep(species_tree_file, rep_listing_file):
	try:
		reps = set([])
		with open(rep_listing_file) as orlf:
			for line in orlf:
				line = line.strip()
				reps.add(line)
				
		ltl_dists = defaultdict(lambda: defaultdict(lambda: None))
		t = Tree(species_tree_file) 
		leaves = []
		for n in t.traverse('postorder'):
			if n.is_leaf():
				leaves.append(n.name)

		for i, l1 in enumerate(sorted(leaves)):
			for j, l2 in enumerate(sorted(leaves)):
				if i != j and l2 in reps:
					ltl_dists[l1][l2] = t.get_distance(l1,l2)
		
		genome_to_group = {}
		for l in leaves:
			cr = None	
			for i, r in enumerate(sorted(ltl_dists[l].items(), key=itemgetter(1), reverse=False)):
				if i == 0: 
					cr = r[0]
			assert(cr != None)
			genome_to_group[l] = cr
		return(genome_to_group)
	except:
		sys.stderr.write(traceback.format_exc() + '\n')
		sys.exit(1)
	
