# Interactive version using streamlit library for the amazing notebook
# https://www.kaggle.com/boliu0/visualizing-all-task-pairs-with-gridlines
 
import numpy as np
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import streamlit as st


data_path = 'input'
training_path = data_path + '/training'
evaluation_path = data_path + '/evaluation'

def plot_one(
	task,
    ax,
    i,
    train_or_test,
    input_or_output,
    ):

    cmap = colors.ListedColormap([
        '#000000',
        '#0074D9',
        '#FF4136',
        '#2ECC40',
        '#FFDC00',
        '#AAAAAA',
        '#F012BE',
        '#FF851B',
        '#7FDBFF',
        '#870C25',
        ])
    norm = colors.Normalize(vmin=0, vmax=9)

    input_matrix = task[train_or_test][i][input_or_output]
    ax.imshow(input_matrix, cmap=cmap, norm=norm)
    ax.grid(True, which='both', color='lightgrey', linewidth=0.5)
    ax.set_yticks([x - 0.5 for x in range(1 + len(input_matrix))])
    ax.set_xticks([x - 0.5 for x in range(1 + len(input_matrix[0]))])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(train_or_test + ' ' + input_or_output)


def plot_train_task(task):
    num_train = len(task['train'])
    (fig, axs) = plt.subplots(2, num_train, figsize=(3 * num_train, 3
                              * 2))
    for i in range(num_train):
        plot_one(task, axs[0, i], i, 'train', 'input')
        plot_one(task, axs[1, i], i, 'train', 'output')
    plt.tight_layout()
    return fig


def plot_test_task(task):
    num_test = len(task['test'])
    (fig, axs) = plt.subplots(2, num_test, figsize=(3 * num_test, 3
                              * 2))
    if num_test == 1:
        plot_one(task, axs[0], 0, 'test', 'input')
        plot_one(task, axs[1], 0, 'test', 'output')
    else:
        for i in range(num_test):
            plot_one(task, axs[0, i], i, 'test', 'input')
            plot_one(task, axs[1, i], i, 'test', 'output')
    plt.tight_layout()
    return fig


def main():

	st.sidebar.header('ARC tasks explorer')

	st.sidebar.subheader('Dataset')
	dataset = st.sidebar.radio('Pick dataset', ['training', 'evaluation'
	                           ])

	st.sidebar.subheader('Task')
	if dataset == 'training':
	    path = training_path
	elif dataset == 'evaluation':

	    path = evaluation_path

	tasks = sorted(os.listdir(path))
	task_id = st.sidebar.selectbox('Pick a task', tasks)
	task_file = str(path + '/' + task_id)


	with open(task_file, 'r') as f:
	    task = json.load(f)

	st.pyplot(plot_train_task(task))
	st.pyplot(plot_test_task(task))

if __name__ == '__main__':
    main()
