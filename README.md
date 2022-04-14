# Kernel diffpatch

Scripts to generate patch series between two Kernel forks.

Sometimes you want to retrieve custom features from a given fork
and apply them to another. This patch generator helps you
extract custom content and generate a patch serie that can be
directly applied and built `in tree`.

I personnaly use this script with Analog Devices's fork,
which is usually merged into Xilinx's kernel.

As an example, the makefile is set to 
Analog Devices's repo and we generate a couple of patches to embed some of their custom drivers.  

This assumes you have a local linux kernel `diff` with, specificed with `--repo /foo/bar`.   
You can control the source repo, containing custom content with `--url https://foo/bar`.   
You can use a specific remote branc with `--branch custom`.   
Control the custom content to extract from the remote branch, with the `files.txt` listing.

```shell
# list of custom ADI's work
# we would like to enhance our local repo with:
╰─$ cat files.txt 
drivers/clk/adi/Kconfig
drivers/clk/adi/Makefile
drivers/clk/adi/clk-ad9545-i2c.c
drivers/clk/adi/clk-ad9545-spi.c
drivers/clk/adi/clk-ad9545.c
drivers/clk/adi/clk-ad9545.h

# let's generate a patch serie for those files
╰─$ ./kernel.py --repo /tmp/linux-custom
new patch : 0001-drivers-clk-adi-Kconfig.patch
new patch : 0002-drivers-clk-adi-Makefile.patch
new patch : 0003-drivers-clk-adi-clk-ad9545-i2c.patch
new patch : 0004-drivers-clk-adi-clk-ad9545-spi.patch
new patch : 0005-drivers-clk-adi-clk-ad9545.patch
new patch : 0006-drivers-clk-adi-clk-ad9545.patch
```

Now apply custom features to enhance our local repo:
```shell
╰─$ cd /tmp/linux-custom
╰─$ patch -p1 < $kernel-diffpatch/patches/*.patch
```

Obviously, this package does not garantee the patch serie will apply correctly.
It is up to the user to:
* provide all custom dependencies, needed by all new custom features
* fix patch that would not apply

You don't have to `diff` with Analog Devices's fork, 
you can use any remote linux kernel :
```shell
╰─$ ./kernel.py --repo /tmp/linux-custom \
    --url https://github.com/xilinx/linux-xlnx
```

You can specify a non default branch to work with:  
```shell
╰─$ ./kernel.py --repo /tmp/linux-custom \
    --url https://github.com/xilinx/linux-xlnx \
        --tag 2020.01
```
