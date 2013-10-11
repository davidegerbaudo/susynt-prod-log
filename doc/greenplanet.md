# Disk space

The space in `/home` is network mounted. Avoid hammering it. The same
is true for `/gdata/atlas`.

The space in `/tmp` is local, but limited (also you can freeze the
machine if you fill it up).  

Each one of the atlas machines has a `/local` area that can be used as
scratch. Cleanup after yourself (is auto-cleanup implemented?)

# Batch

Use the `atlas` queue. Write your output locally (`/local/${jobid}`?)
and copy it back to the network-mounted area at the end of the job.

Depending on whether you use all of the available input branches, it
might be advantageous to copy the input file locally at the beginning
of the job.

# Fairshare

No need to worry about clogging the `atlas` queue with many jobs. Chad
says that the fairshare is already implemented in maui, so if you have
many jobs your priority will go down. You can check your fairshare
score with the commands in
[greenplanet_fairshare.sh](../bash/greenplanet_fairshare.sh).
Snapshot as of 2013-01-11:

```
FSInterval        %     Target       0       1       2       3       4       5       6
FSWeight       ------- -------  1.0000  0.5000  0.2500  0.1250  0.0625  0.0312  0.0156
TotalUsage      100.00 ------- 78286.4 83712.0 77701.9 79319.1 70435.3 64973.4 63181.9
rpatrick          0.00   2.00  ------- ------- -------    0.00 ------- ------- -------
sfarrell          0.01   2.00  ------- ------- ------- ------- -------    0.09    1.54
krao              0.00   2.00  ------- ------- ------- ------- ------- ------- -------
anelson           0.06   2.00     0.06    0.06    0.06    0.02 -------    0.08    0.16
jedman            0.00   2.00  ------- ------- ------- ------- ------- ------- -------
cshimmin          0.15   2.00     0.29 ------- ------- -------    0.13 ------- -------
gerbaudo          0.04   2.00     0.02    0.06    0.07    0.02 ------- -------    0.12
suneetu           0.26   2.00     0.32    0.21    0.26    0.00    0.29    0.02    0.07
amete             0.09   2.00     0.08    0.07    0.23    0.08 ------- ------- -------
ataffard          0.00   2.00  ------- ------- ------- ------- ------- ------- -------
mrelich           0.21   2.00     0.17    0.28    0.21    0.15    0.32 ------- -------
mfrate            0.06   2.00  -------    0.03    0.15    0.23    0.36    0.56    0.61
atlas*            0.87   7.00     0.94    0.71    0.98    0.50    1.11    0.76    2.49
atlas*            0.87   7.00     0.94    0.71    0.98    0.50    1.11    0.76    2.49
```
