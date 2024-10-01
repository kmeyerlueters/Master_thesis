#!/bin/sh


# check python version
python --version

# to surpress annoyingly verbose warning
export TOKENIZERS_PARALLELISM=true
export CUDA_VISIBLE_DEVICES=1

# set params
PROVIDER="microsoft"

for MODEL_NAME in "Phi-3-medium-4k-instruct"; do 
 

    for EXPERIMENT in "/work/bba5344/data/Phi_arguments_biggest_difference"; do

        python get_temporal_completions.py \
            --model_name_or_path $PROVIDER/$MODEL_NAME \
            --test_data_input_path $EXPERIMENT.csv \
            --n_test_samples 0 \
            --batch_size 8 \
            --input_col "prompt" \
            --argument_col "argument" \
            --topic_col "topic" \
            --stance_col "stance" \
            --test_data_output_path /work/bba5344/model_completions/$EXPERIMENT/$MODEL_NAME.csv \
            --load_in_8bit False \
            --log_level "debug" \
            --cache_dir "/work/bba5344/cache_dir" \
            --prompt_template_path "/work/bba5344/code/prompt_template.txt"

    done;

done;
