input_file=$1

../bin/word2vec -train $input_file -output ../data/item_vec.txt -size 128 -window 5 -sample 1e-3 -negative 5 -hs 0 -binary 0 -cbow 0 -iter 100
