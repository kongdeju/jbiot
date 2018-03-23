
Usage
=====

lsub
----

use lsub to subject jbobs ,type lsub -h to check the detail usage::

    lsub -h

    Usage:
        lsub <cmdfile> [--with-docker|--with-singularity][--dry][-e <email>][-w <wexin_name>][-n <job_nam>]

    Options:
        -h --help                print this screen
        --dry                    all done but run script
        --with-docker            prefer to use docker when run cmd
        --with-singularity       prefer to user singularity when run cmd
        -e,--email=<email>       email of you want to remind of
        -w,--wechat=<name>       wechat name you want to send to
        -n,--name=<job_name>     the name of this task.

csub
----

use csub to subject jobs to cluster, type csub -h to check detail usage


.. Note::

    documents will updated in time...


