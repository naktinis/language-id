import os
import csv

import numpy as np
from PIL import Image


class TCData(object):
    def __init__(self, image_dir, label_filename, conf):
        self.image_dir = image_dir
        self.label_filename = label_filename
        self.batch_size = conf.batch_size
        self.language_set = []
        self.labels = []
        self.images = []

    def load_data(self):
        with open(self.label_filename) as label_file:
            csv_reader = csv.reader(label_file, delimiter=',')

            # Skip the header
            next(csv_reader)

            for audio, label in csv_reader:
                image_path = os.path.join(self.image_dir, '{}.png'.format(audio.split('.')[0]))
                self.images.append(image_path)

                # Store labels in a global
                if label not in self.language_set:
                    self.language_set.append(label)
                label_index = self.language_set.index(label)

                self.labels.append(label_index)

    def lang_index(self, lang):
        """Return the index of the given language."""
        return self.language_set.index(lang)

    def get_data(self, use_percent, tail=False):
        """Return the first (or the last) use_percent percent of data and
        its labels.
        """
        start = None
        end = int(round(len(self.images) * use_percent / 100.))
        if tail:
            start, end = -end, start
        return self.images[start:end], self.labels[start:end]
