sbatch  --export=ALL --cpus-per-task 24  -o ~/slurmout/t1.%a.out  \
  --array=0-29  /mnt/cluster/data/Hawco_M3RI_Travel/src/slurm/01_job_id_subscript.sh
