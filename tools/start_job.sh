#!/usr/bin/env bash
#SBATCH --job-name=generate_questions
#SBATCH --mail-type=END,INVALID_DEPEND
#SBATCH --mail-user=steffen.kleinle@uni-a.de
#SBATCH --output=logs/%x.%j.log
#SBATCH --time=1-0

#SBATCH --partition=epyc
#SBATCH --mem-per-cpu=50G
#SBATCH --cpus-per-task=8
python3 generate_questions_with_evidence.py
