#!/bin/bash

source build_common.sh

VERSION=${VERSION:="3.4.8"}
RELEASE=${RELEASE:="1"}
PACKNAME=${PACKNAME:="zookeeper"}
CACHEDIR=${CACHEDIR:="/isos/redBorder"}
REPODIR=${REPODIR:="/repos/redBorder"}

list_of_packages="${REPODIR}/${PACKNAME}-${VERSION}-${RELEASE}.el7.centos.src.rpm 
                ${REPODIR}/${PACKNAME}-${VERSION}-${RELEASE}.el7.centos.x86_64.rpm 
                ${REPODIR}/${PACKNAME}-debuginfo-${VERSION}-${RELEASE}.el7.centos.x86_64.rpm
                ${CACHEDIR}/${PACKNAME}-${VERSION}-${RELEASE}.el7.centos.x86_64.rpm"

if [ "x$1" != "xforce" ]; then
        f_check "${list_of_packages}"
        if [ $? -eq 0 ]; then
                # the rpms exist and we don't need to create again
                exit 0
        fi
fi

# First we need to download source
mkdir SOURCES
URL=$(curl -s https://www.apache.org/dyn/closer.cgi/zookeeper/zookeeper-${VERSION}/zookeeper-${VERSION}.tar.gz?asjson=1 | python -c 'import sys,json; data=json.load(sys.stdin); print data["preferred"] + data["path_info"]')
wget ${URL} -O SOURCES/${PACKNAME}-${VERSION}.tar.gz
wget https://github.com/id/zookeeper-el7-rpm/archive/master.tar.gz -O SOURCES/zookeeper-el7-rpm.tar.gz
pushd SOURCES &>/dev/null
tar xzf zookeeper-el7-rpm.tar.gz
mv ${PACKNAME}-${VERSION}.tar.gz zookeeper-el7-rpm-master
popd &>/dev/null

# Now it is time to create the source rpm
/usr/bin/mock -r default \
        --define "__version ${VERSION}" \
        --define "__release ${RELEASE}" \
	--resultdir=pkgs --buildsrpm --spec=${PACKNAME}.spec --sources=SOURCES/zookeeper-el7-rpm-master

# with it, we can create rest of packages
/usr/bin/mock -r default \
        --define "__version ${VERSION}" \
        --define "__release ${RELEASE}" \
	--resultdir=pkgs --rebuild pkgs/${PACKNAME}*.src.rpm

ret=$?

# cleaning
rm -rf SOURCES

if [ $ret -ne 0 ]; then
        echo "Error in mock stage ... exiting"
        exit 1
fi

# sync to cache and repo
#rsync -a pkgs/${PACKNAME}${LIBVER}-${VERSION}-${RELEASE}.el7.centos.x86_64.rpm ${CACHEDIR}
#rsync -a pkgs/${PACKNAME}*.rpm ${REPODIR}
f_rsync_iso pkgs/${PACKNAME}${LIBVER}-${VERSION}-${RELEASE}.el7.centos.x86_64.rpm
f_rsync_repo pkgs/${PACKNAME}*.rpm  
#rm -rf pkgs

# Update sdk7 repo
f_rupdaterepo

