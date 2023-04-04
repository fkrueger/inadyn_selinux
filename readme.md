This git-repo contains the files needed to create accompanying RPM files for CentOS/RHEL8 (el8), but they should work for Fedora, Alma Linux, Rocky Linux, etc. also.

Based on the inadyn version provided on https://github.com/troglobit/inadyn


# INSTALLATION via repository
The compiled SElinux policy module should also work on Fedora, and maybe even earlier versions of CentOS.

A complete version of the resulting RPM file can be found in my technoholics-repo.
It can be found here: https://dev.techno.holics.at/technoholics-repo/

## Easy installation with technoholics-repo
* Download technoholics-repo-release-20210620-1.el8.noarch.rpm
* Install access to the techno.holics.at repository via
yum install https://dev.techno.holics.at/technoholics-repo/el8/technoholics-repo-release-20210620-1.el8.noarch.rpm
* If needed, the gpg key used for signing the RPM packages can be found here: https://dev.techno.holics.at/holics-repo/RPM-GPG-KEY-holicsrepo
* Now install the inadyn_selinux and preferrably also the inadyn-utils packages.
yum install inadyn_selinux inadyn

# Cheers!


