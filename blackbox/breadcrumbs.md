./extract_analysis_features.py --analyse GE
cd ../downsample
./downsample.py --technique resample --frame_dims 13 ../blackbox/mfcc/GE/ge.dev.filter1_gt.npz 
 exp/GE/mfcc.dev.filter1_gt.downsample_10.npz  10
cd -
./npz_to_tsv.py ../downsample/exp/GE/mfcc.dev.filter1_gt.downsample_10.npz auto
cd ../embeddings



./extract_analysis_features.py --analyse GE

./npz_to_tsv.py ../downsample/exp/RU/mfcc.dev.gt_words.downsample_10.npz auto
./npz_to_tsv.py ../downsample/exp/GE/mfcc.dev.gt_words.downsample_10.npz auto
./npz_to_tsv.py ../embeddings/models/GE.gt/train_cae_rnn/15b3ecce63/cae.best_val.GE.val.npz auto
./npz_to_tsv.py ../embeddings/models/RU.gt/train_cae_rnn/0bab597d5a/cae.best_val.RU.val.npz auto
