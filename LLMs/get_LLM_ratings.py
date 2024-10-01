import pandas as pd
import time 
import fire
import logging
import torch
import os
import re

from huggingface_hub import login
from simple_generation import SimpleGenerator

def extract_number_from_completion(completion):
    """Extracts the first number from the completion."""
    match = re.search(r'\b[1-5]\b', completion)
    if match:
        return match.group(0)
    else:
        return "0"  # Default to "0" if no valid number is found

def load_prompt_template(template_path):
    """Load the prompt template from an external file."""
    with open(template_path, 'r') as file:
        return file.read()

def process_chunk(chunk, argument_col, topic_col, stance_col, prompt_template):
    """Process a chunk of data and construct prompts."""
    def map_stance(stance):
        return "for" if stance == 1 else "against"

    def construct_prompt(row):
        return prompt_template.replace("Argument:", f"Argument: {row[argument_col]}") \
                              .replace("Topic:", f"Topic: {row[topic_col]}") \
                              .replace("Stance:", f"Stance: {map_stance(row[stance_col])}")

    chunk['input_text'] = chunk.apply(construct_prompt, axis=1)
    return chunk

def main(
        # data parameters
        test_data_input_path: str,
        n_test_samples: int,
        input_col: str,
        argument_col: str,
        topic_col: str,
        stance_col: str,
        test_data_output_path: str,
        prompt_template_path: str,  # New parameter for the prompt template path

        # model parameters
        model_name_or_path: str,
        cache_dir: str,

        # inference parameters
        batch_size, # can be int or "auto"
          
        # quantization parameters
        load_in_8bit: bool,
           
        # misc parameters
        log_level: str,
        ):

    ###########################################################
    # SET UP
    ###########################################################

    # set up logging
    logging.basicConfig(level=getattr(logging, log_level.upper()), format='%(asctime)s %(levelname)s %(message)s')

    # set up device
    login("insert_key")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logging.info(f"Running on device: {device}")
    if device == "cuda":
        logging.info(f"CUDA memory: {round(torch.cuda.mem_get_info()[0]/1024**3,2)}GB")
        
    ###########################################################
    # LOAD DATA
    ###########################################################

    # Load the prompt template
    prompt_template = load_prompt_template(prompt_template_path)

    # Load and process TEST data in chunks
    chunksize = 10000  # Adjust this based on your memory capacity
    chunk_list = []

    with pd.read_csv(test_data_input_path, encoding='ISO-8859-1', delimiter=';', chunksize=chunksize) as reader:
        for chunk in reader:
            if n_test_samples > 0:
                chunk = chunk.sample(n_test_samples, random_state=123)
            processed_chunk = process_chunk(chunk, argument_col, topic_col, stance_col, prompt_template)
            chunk_list.append(processed_chunk)

    test_df = pd.concat(chunk_list)
    input_texts = test_df['input_text'].tolist()

    # print 3 random prompts
    logging.info(f"3 random prompts from TEST data:\n{test_df.sample(3, random_state=123)['input_text'].tolist()}\n")

    ###########################################################
    # LOAD GENERATOR
    ###########################################################

    logging.info(f"Loading model {model_name_or_path}")

    generator = SimpleGenerator(
        model_name_or_path,
        load_in_8bit=load_in_8bit,
        torch_dtype=torch.bfloat16,
        cache_dir=cache_dir,
        device_map="auto"
    )

    ###########################################################
    # GET COMPLETIONS
    ###########################################################

    logging.info(f"Generating completions for {len(input_texts)} prompts")

    completions = generator(
        texts=input_texts,
        temperature=0.001,
        max_new_tokens=500,
        top_p=1.0,
        do_sample=True,
        skip_prompt=True,
        batch_size=batch_size,
        starting_batch_size=8,
        apply_chat_template=True,
    )

    logging.info(f"Generated {len(completions)} completions")
    processed_completions = [extract_number_from_completion(completion) for completion in completions]

    # write new model completions to new column
    test_df["model_completion"] = completions
    test_df["extracted_number"] = processed_completions
    test_df["model_name"] = model_name_or_path

    # check if output path exists, otherwise create it
    if not os.path.exists(test_data_output_path.rsplit("/", 1)[0]):
        logging.info(f"Creating new path {test_data_output_path.rsplit('/', 1)[0]}")
        os.makedirs(test_data_output_path.rsplit("/", 1)[0])

    logging.info(f"Saving completions to {test_data_output_path}")
    test_df.to_csv(test_data_output_path, index=False, sep=';')

if __name__ == "__main__":
    st = time.time()
    fire.Fire(main)
    logging.info(f'Total execution time: {time.time() - st:.2f} seconds')
