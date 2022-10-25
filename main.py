
# Copyright (c) 2021 brainlife.io
#
# This file is a MNE python-based brainlife.io App
#


# set up environment
import os
import json
import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image

#workaround for -- _tkinter.TclError: invalid command name ".!canvas"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Current path
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Load brainlife config.json
with open(__location__+'/config.json') as config_json:
    config = json.load(config_json)

# == LOAD DATA ==
fname = config['fif']
raw = mne.io.read_raw_fif(fname, verbose=False)
proj=mne.read_proj(config['projection'])
raw.add_proj(proj)
raw_cleaned = raw.copy().apply_proj()
raw_cleaned.save(os.path.join('out_dir','meg.fif'))

ecg_evoked = mne.preprocessing.create_ecg_epochs(raw).average()
ecg_evoked.apply_baseline((None, None))

projs = projs[3:]
# # # == FIGURES ==
plt.figure(1)
fig = mne.viz.plot_projs_joint(proj, ecg_evoked, picks_trace='MEG 0111')
fig.suptitle('ECG projectors')
fig.savefig(os.path.join('out_figs','joint-plot.png'))
