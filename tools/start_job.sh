#!/usr/bin/env bash
#SBATCH --job-name=generate_questions
#SBATCH --mail-type=END,INVALID_DEPEND
#SBATCH --mail-user=steffen.kleinle@uni-a.de
#SBATCH --output=logs/%x_%j.log
#SBATCH --time=1-0

#SBATCH --partition=epyc-gpu
#SBATCH --mem-per-cpu=50G
#SBATCH --cpus-per-task=2
#SBATCH --gpus=a100:1
python3 classifier.py
