#!/usr/bin/env python

"""
Encode the given NumPy archive using the specified model.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2018, 2019
"""

from datetime import datetime
from os import path
import argparse
import pickle
import numpy as np
import os
import sys
import tensorflow as tf

sys.path.append(path.join("..", "src"))

from apply_model import build_model
from link_mfcc import sixteen_languages
from tflego import NP_DTYPE, TF_DTYPE, NP_ITYPE, TF_ITYPE
import batching
import data_io


#-----------------------------------------------------------------------------#
#                            APPLY MODEL FUNCTIONS                            #
#-----------------------------------------------------------------------------#


def apply_model(model_fn, npz_fn):

    # Load the model options
    model_dir = path.split(model_fn)[0]
    options_dict_fn = path.join(model_dir, "options_dict.pkl")
    print("Reading:", options_dict_fn)
    with open(options_dict_fn, "rb") as f:
        options_dict = pickle.load(f)

    # Load data
    x_data, labels, lengths, keys, speakers = data_io.load_data_from_npz(
        npz_fn
        )

    if "cnn" in options_dict["script"]:

        # Pad and flatten data
        x_data, _ = data_io.pad_sequences(
            x_data, options_dict["max_length"], True
            )
        x_data = np.transpose(x_data, (0, 2, 1))
        x_data = x_data.reshape((-1, options_dict["d_in"]))

        # Build model
        x = tf.placeholder(TF_DTYPE, [None, options_dict["d_in"]])
        model = build_model(x, None, options_dict)

        # Embed data
        batch_iterator = batching.LabelledIterator(
            x_data, None, x_data.shape[0], False
            )
        saver = tf.train.Saver()
        with tf.Session() as session:
            saver.restore(session, model_fn)
            for batch_x in batch_iterator:
                np_z = session.run(
                    [model["encoding"]], feed_dict={x: batch_x})[0]
                break  # single batch

    else:  # rnn
        
        # Truncate and limit dimensionality
        data_io.trunc_and_limit_dim(
            x_data, lengths, options_dict["n_input"],
            options_dict["max_length"]
            )

        # Build model
        x = tf.placeholder(TF_DTYPE, [None, None, options_dict["n_input"]])
        x_lengths = tf.placeholder(TF_ITYPE, [None])
        model = build_model(x, x_lengths, options_dict)

        # Embed data
        batch_iterator = batching.SimpleIterator(x_data, len(x_data), False)
        saver = tf.train.Saver()
        with tf.Session() as session:
            saver.restore(session, model_fn)
            for batch_x_padded, batch_x_lengths in batch_iterator:
                np_x = batch_x_padded
                np_x_lengths = batch_x_lengths
                np_z = session.run(
                    [model["encoding"]], feed_dict={x: np_x, x_lengths:
                    np_x_lengths}
                    )[0]
                break  # single batch

    embed_dict = {}
    for i, utt_key in enumerate([keys[i] for i in batch_iterator.indices]):
        embed_dict[utt_key] = np_z[i]

    return embed_dict


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__.strip().split("\n")[0], add_help=False
        )
    parser.add_argument("model_fn", type=str, help="model checkpoint filename")
    parser.add_argument("npz_fn", type=str, help="the NumPy archive to encode")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    # Do not output TensorFlow info and warning messages
    import warnings
    warnings.filterwarnings("ignore")
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    tf.logging.set_verbosity(tf.logging.ERROR)
    if type(tf.contrib) != type(tf):
        tf.contrib._warning = None

    # Embed data
    embed_dict = apply_model(args.model_fn, args.npz_fn)

    # Save embeddings
    model_dir, model_fn = path.split(args.model_fn)
    npz_fn = path.join(
        model_dir, path.splitext(model_fn)[0] + "." +
        path.split(args.npz_fn)[-1]
        )
    print("Writing:", npz_fn)
    np.savez_compressed(npz_fn, **embed_dict)
    print(datetime.now())


if __name__ == "__main__":
    main()
