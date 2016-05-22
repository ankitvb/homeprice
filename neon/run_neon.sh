#!/bin/bash

#source load_modules.sh

export BATCH_SIZE=1000
export EVAL_FREQ=10

for NUM_EPOCHS in 500 
do
    python train_mlp.py -o homeapp_neon.hd5 -e $NUM_EPOCHS --batch_size $BATCH_SIZE --eval_freq $EVAL_FREQ
done 
