Multilingual Acoustic Word Embeddings on GlobalPhone
====================================================

Overview
--------
Multilingual acoustic word embedding (AWE) approaches are implemented and
evaluated on the GlobalPhhone corpus.


Disclaimer
----------
The code provided here is not pretty. But I believe that research should be
reproducible. I provide no guarantees with the code, but please let me know if
you have any problems, find bugs or have general comments.


Download datasets
-----------------
The [GlobalPhone](https://csl.anthropomatik.kit.edu/english/globalphone.php)
corpus and forced alignments of the data needs to be obtained. GlobalPhone
needs to be paid for. If you have proof of payment, we can give you access to
the forced alignments. Save the data and forced alignments in a separate
directory and update the `paths.py` file to point to the data directories.


Create and run Docker image
---------------------------
*To-do*


If not using Docker: Install dependencies
-----------------------------------------
If you are not using Docker, install the following dependencies:

- [Python 3](https://www.python.org/downloads/)
- [TensorFlow 1.13.1](https://www.tensorflow.org/)
- [LibROSA](http://librosa.github.io/librosa/)
- [Cython](https://cython.org/)
- [tqdm](https://tqdm.github.io/)
- [speech_dtw](https://github.com/kamperh/speech_dtw/)
- [shorten](http://etree.org/shnutils/shorten/dist/src/shorten-3.6.1.tar.gz)

To install `speech_dtw` (required for same-different evaluation) and `shorten`
(required for processing audio), run `./install_local.sh`.


Extract speech features
-----------------------
Update the paths in `paths.py` to point to the data directories. If you are
using docker, `paths.py` will already point to the mounted directories. Extract
MFCC features in the `features/` directory as follows:

    cd features
    ./extract_features.py SP

You need to run `extract_features.py` for all languages; run it without any
parameters to see all 16 language codes.


Evaluate frame-level features using the same-different task
-----------------------------------------------------------
This is optional. To perform frame-level same-different evaluation based on
dynamic time warping (DTW), follow [samediff/readme.md](samediff/readme.md).



