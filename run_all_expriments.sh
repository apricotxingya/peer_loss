filelist=`ls ../noisy_data | grep -v agnews`
for file in $filelist
do
  echo '%%%%'
  echo $file
  python runner.py noisy --noisy_file="../data/train.csv" --seeds 8 --test-size 0.15 --val-size 0.1 --dropout 0 --loss bce --activation relu --normalize --verbose --e0 0.1 --e1 0.3 --episodes 1000 --batchsize 64 --batchsize-peer 64 --hidsize 8 --lr 0.0007 --alpha 1
done

# trec


# agnews


# chn


# chngolden
