import re
from environment import Environment
from lstm_for_meta import Lstm, LstmFastBatchGenerator as BatchGenerator
from res_net_opt import ResNet4Lstm
from useful_functions import create_vocabulary, get_positions_in_vocabulary

with open('datasets/scipop_v3.0/scipop_train.txt', 'r') as f:
    train_text = re.sub('<[^>]*>', '', f.read( ))

with open('datasets/scipop_v3.0/scipop_valid.txt', 'r') as f:
    valid_text = re.sub('<[^>]*>', '', ''.join(f.readlines()[:10]))

vocabulary = create_vocabulary(train_text + valid_text)
vocabulary_size = len(vocabulary)

env = Environment(
    pupil_class=Lstm,
    meta_optimizer_class=ResNet4Lstm,
    batch_generator_classes=BatchGenerator,
    vocabulary=vocabulary)

env.build_pupil(
    batch_size=64,
    num_layers=1,
    num_nodes=[400],
    num_output_layers=1,
    num_output_nodes=[],
    vocabulary_size=vocabulary_size,
    embedding_size=150,
    num_unrollings=10,
    init_parameter=3.,
    num_gpus=1,
    regime='training_with_meta_optimizer'
)

env.build_optimizer(
    regime='inference'
)


add_feed = [{'placeholder': 'dropout', 'value': 0.9}]
valid_add_feed = [{'placeholder': 'dropout', 'value': 1.}]

env.train(
    with_meta_optimizer=True,
    save_path='debug_empty_meta_optimizer/not_changing_variables_issue',
    batch_size=64,
    num_unrollings=10,
    vocabulary=vocabulary,
    checkpoint_steps=2000,
    result_types=['loss'],
    printed_result_types=['loss'],
    stop=40000,
    train_dataset_text=train_text,
    validation_dataset_texts=[valid_text],
    results_collect_interval=100,
    additions_to_feed_dict=add_feed,
    validation_additions_to_feed_dict=valid_add_feed,
    summary=True,
    add_graph_to_summary=True
)
