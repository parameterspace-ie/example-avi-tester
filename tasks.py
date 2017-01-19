"""
GAVIP Example AVIS: Alerts AVI

AVI pipeline
"""

import os
import json
from django.conf import settings

# Class used for creating pipeline tasks
from pipeline.classes import (
    AviTask,
    AviParameter, AviLocalTarget,
)

import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import mpld3
import json
import pandas


class PlotData(AviTask):

    outputFile = AviParameter()

    def output(self):
        return AviLocalTarget(os.path.join(
            settings.OUTPUT_PATH, '%s' % self.outputFile
        ))

    def run(self):

        x=np.linspace(1,10,10)
        y=np.random.randint(10000, size=10)

        fig = plt.figure()
        plt.plot(x, y, 'r')
        plt.xlabel('Random x')
        plt.ylabel('Random y')

        with open(self.output().path, 'w') as out:
            json.dump(mpld3.fig_to_dict(fig), out)