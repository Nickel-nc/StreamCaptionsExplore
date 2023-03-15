# Video captions module (In testing WIP)


### Usage task commands
___

```
conda create -n video-bert python=3.9
conda activate video-bert

git clone git@github.com:ammesatyajit/VideoBERT.git

pip install -r requirements
pip install --upgrade tensorflow_hub

pip install spacy
pip install transformers

conda install -c anaconda tensorflow
conda install -c anaconda keras

conda install -c pytorch torchvision
# conda install -c pytorch torchtext
pip install torch==1.8.0 torchtext==0.9.0

python -m spacy download en_core_web_sm

```

If case of conflicts, delete caffe dlls from path lib

### 1. Feature extraction with I3D model

```
$FILE_LIST_PATH = ".\data\video_filepaths.txt"
$ROOT_VIDEO_PATH = ".\data\raw_videos"
$FEATURES_SAVE_PATH = ".\data\features"
$IMGS_SAVE_PATH = ".\data\images"


python .\VideoBERT\I3D\batch_extract.py `
-f $FILE_LIST_PATH `
-r $ROOT_VIDEO_PATH `
-s $FEATURES_SAVE_PATH `
-i $IMGS_SAVE_PATH
```

### 2. Hierarchical Minibatch K-means

```
$ROOT_FEATURE_PATH = ".\data\features"
$FEATURES_PREFIX = "features"
$BATCH_SIZE = 2048
$SAVE_DIR = ".\data\kmeans_vectors"
$CENTROID_DIR = ".\data\centroids"

python .\VideoBERT\I3D\minibatch_hkmeans.py `
-r $ROOT_FEATURE_PATH `
-p $FEATURES_PREFIX `
-b $BATCH_SIZE `
-s $SAVE_DIR `
-c $CENTROID_DIR
```

### 3. Concatenate centroids

### 4. Centroid to images

```
$ROOT_FEATURES = "./data/features"
$ROOT_IMGS = "./data/images"
$CENTROID_FILE = "./data/centroids_prepared/centroids.npy"
$SAVE_FILE = "./data/images_dict/images_dict.json"

python .\VideoBERT\data\centroid_to_img.py `
-f $ROOT_FEATURES `
-i $ROOT_IMGS `
-c $CENTROID_FILE `
-s $SAVE_FILE
```

### 5. Label data

```
$ROOT_FEATURES = "./data/features"
$CENTROID_FILE = "./data/centroids_prepared/centroids.npy"
$SAVE_FILE = "./data/labelled_data/labelled_data.json"

python ./VideoBERT/data/label_data.py `
-f $ROOT_FEATURES `
-c $CENTROID_FILE `
-s $SAVE_FILE
```

### Punctuate data

```
$CAPTIONS_PATH = "./data/captions/captions.json"
$PUNCTUATOR_MODEL = "./data/punctuator_model/Demo-Europarl-EN.pcl"
$LABELLED_DATA = "./data/labelled_data/labelled_data.json"
$ROOT_FEATURES = "./data/features"
$SAVE_PATH = "./data/train/train.json"

python VideoBERT/data/punctuate_text.py `
-c $CAPTIONS_PATH `
-p $PUNCTUATOR_MODEL `
-l $LABELLED_DATA `
-f $ROOT_FEATURES `
-s $SAVE_PATH
```

### Training

```
$OUTPUT_DIR = "./data/pred_checkpoints"
$TRAIN_DATA_PATH = "./data/train/train.json"
$EVAL_DATA_PATH = "./data/train/train.json"
$PER_GPU_TRAIN_BATCH_SIZE = 4
$GRADIENT_ACCUMULATION_STEPS = 2
$LEARNING_RATE = 1e-5
$ADAM_EPSILON = 1e-8
$MAX_GRAD_NORM = 1.0
$NUM_TRAIN_EPOCHS = 10
$LOG_DIR = "./data/logs"
$LOCAL_RANK = -1
$WARMUP_STEPS = 2
$LOGGING_STEPS = 1
$SAVE_STEPS = 1
$SAVE_TOTAL_LIMIT = 5
$SEED = 42

python -m VideoBERT.train.train `
--output_dir $OUTPUT_DIR `
--train_data_path $TRAIN_DATA_PATH `
--eval_data_path $EVAL_DATA_PATH `
--per_gpu_train_batch_size $PER_GPU_TRAIN_BATCH_SIZE `
--gradient_accumulation_steps $GRADIENT_ACCUMULATION_STEPS `
--learning_rate $LEARNING_RATE `
--adam_epsilon $ADAM_EPSILON `
--max_grad_norm $MAX_GRAD_NORM `
--num_train_epochs $NUM_TRAIN_EPOCHS `
--log_dir $LOG_DIR `
--local_rank $LOCAL_RANK `
--warmup_steps $WARMUP_STEPS `
--logging_steps $LOGGING_STEPS `
--save_steps $SAVE_STEPS `
--save_total_limit $SAVE_TOTAL_LIMIT `
--seed $SEED
```

### Run inference

```
$MODEL_NAME_OR_PATH = "./data/pred_checkpoints"
$OUTPUT_DIR = "./data/pred_checkpoints"
$EXAMPLE_ID = 0
$SEED = 42

python -m VideoBERT.evaluation.inference `
--model_name_or_path $MODEL_NAME_OR_PATH `
--output_dir $OUTPUT_DIR `
--example_id $EXAMPLE_ID `
--seed $SEED
```


### Relevant Links
___

[Souce repo Video prediction](https://github.com/MDSKUL/MasterProject)

[Souce repo Howto100m](https://github.com/antoine77340/howto100m)

[Souce repo VideoBert](https://github.com/ammesatyajit/VideoBERT)

[Souce repo UniVl model](https://github.com/microsoft/UniVL)

[Source dataset](https://www.di.ens.fr/willow/research/howto100m/)


[Punctuator models source](https://drive.google.com/drive/folders/0B7BsN5f2F1fZQnFsbzJ3TWxxMms?resourcekey=0-6yhuY9FOeITBBWWNdyG2aw)