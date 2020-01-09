%global DATE 20120507
%global SVNREV 187244
%global gcc_version 4.7.0
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 5
%global gmp_version 4.3.1
%global mpfr_version 2.4.1
%global mpc_version 0.8.1
%global ppl_version 0.10.1
%global cloog_version 0.15.7
%global _unpackaged_files_terminate_build 0
%global multilib_64_archs sparc64 ppc64 s390x x86_64
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%if 0%{?rhel} >= 6
%global multilib_32_arch i686
%else
%global multilib_32_arch i386
%endif
%endif
Summary: The GNU Transactional Memory library
Name: libitm

Version: %{gcc_version}
Release: %{gcc_release}.1.1%{?dist}
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: System Environment/Libraries
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-4_7-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: http://www.mpfr.org/mpfr-%{mpfr_version}/mpfr-%{mpfr_version}.tar.bz2
Source4: http://www.multiprecision.org/mpc/download/mpc-%{mpc_version}.tar.gz
Source5: ftp://ftp.gnu.org/pub/gnu/gmp/gmp-%{gmp_version}.tar.bz2
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
%if 0%{?rhel} >= 6
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
BuildRequires: binutils >= 2.19.51.0.14-33
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
%else
# Don't have binutils which support --build-id >= 2.17.50.0.17-3
# Don't have binutils which support %gnu_unique_object >= 2.19.51.0.14
# Don't have binutils which  support .cfi_sections >= 2.19.51.0.14-33
BuildRequires: binutils >= 2.17.50.0.2-8
%endif
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
#BuildRequires: systemtap-sdt-devel >= 1.3
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
%if 0%{?rhel} >= 6
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%else
BuildRequires: elfutils-devel >= 0.72
%endif
%ifarch ppc ppc64 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
BuildRequires: gmp-devel >= 4.1.2-8
%if 0%{?rhel} >= 6
BuildRequires: mpfr-devel >= 2.2.1
%endif
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
ExclusiveArch: %{ix86} x86_64 %{arm} alpha ppc ppc64

%global oformat %{nil}
%ifarch %{ix86}
%global oformat OUTPUT_FORMAT(elf32-i386)
%endif
%ifarch x86_64
%global oformat OUTPUT_FORMAT(elf64-x86-64)
%endif
%ifarch ppc
%global oformat OUTPUT_FORMAT(elf32-powerpc)
%endif
%ifarch ppc64
%global oformat OUTPUT_FORMAT(elf64-powerpc)
%endif
%ifarch s390
%global oformat OUTPUT_FORMAT(elf32-s390)
%endif
%ifarch s390x
%global oformat OUTPUT_FORMAT(elf64-s390)
%endif
%ifarch ia64
%global oformat OUTPUT_FORMAT(elf64-ia64-little)
%endif

Patch0: gcc47-hack.patch
Patch1: gcc47-c++-builtin-redecl.patch
Patch2: gcc47-java-nomulti.patch
Patch3: gcc47-ppc32-retaddr.patch
Patch4: gcc47-pr33763.patch
Patch5: gcc47-rh330771.patch
Patch6: gcc47-i386-libgomp.patch
Patch7: gcc47-sparc-config-detection.patch
Patch8: gcc47-libgomp-omp_h-multilib.patch
Patch9: gcc47-libtool-no-rpath.patch
Patch10: gcc47-cloog-dl.patch
Patch11: gcc47-pr38757.patch
Patch12: gcc47-libstdc++-docs.patch
Patch13: gcc47-no-add-needed.patch
Patch14: gcc47-ppl-0.10.patch
Patch15: gcc47-libitm-fno-exceptions.patch

Patch1000: gcc47-libstdc++-compat.patch
Patch1001: gcc47-gnu89-inline-dflt.patch
Patch1002: gcc47-ppc64-ld-workaround.patch
Patch1003: gcc47-cloog-gmp-41-workaround.patch
Patch1004: gcc47-ppl-convenience.patch
Patch1005: gcc47-cloog-dl2.patch
Patch1006: gcc47-gmp-4.0.1-s390.patch
Patch1007: gcc47-libgfortran-compat.patch
Patch1008: gcc47-alt-compat-test.patch
Patch1009: gcc47-libquadmath-compat.patch
Patch1010: gcc47-libstdc++44-xfail.patch

%if 0%{?rhel} >= 6
%global nonsharedver 44
%else
%global nonsharedver 41
%endif

%global _gnu %{nil}
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif
%ifarch ppc
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif
%ifnarch sparcv9 ppc
%global gcc_target_platform %{_target_platform}
%endif

%description
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%prep
%if 0%{?rhel} >= 6
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 4
%else
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 4 -a 5
%endif
%patch0 -p0 -b .hack~
%patch1 -p0 -b .c++-builtin-redecl~
%patch2 -p0 -b .java-nomulti~
%patch3 -p0 -b .ppc32-retaddr~
%patch4 -p0 -b .pr33763~
%patch5 -p0 -b .rh330771~
%patch6 -p0 -b .i386-libgomp~
%patch7 -p0 -b .sparc-config-detection~
%patch8 -p0 -b .libgomp-omp_h-multilib~
%patch9 -p0 -b .libtool-no-rpath~
%patch11 -p0 -b .pr38757~
%patch13 -p0 -b .no-add-needed~
%patch15 -p0 -b .libitm-fno-exceptions~

%patch1000 -p0 -b .libstdc++-compat~
%if 0%{?rhel} < 6
%patch1001 -p0 -b .gnu89-inline-dflt~
%patch1002 -p0 -b .ppc64-ld-workaround~
%endif
%patch1007 -p0 -b .libgfortran-compat~
%ifarch %{ix86} x86_64
# On i?86/x86_64 there are some incompatibilities in _Decimal* as well as
# aggregates containing larger vector passing.
%patch1008 -p0 -b .alt-compat-test~
%endif
%patch1009 -p0 -b .libquadmath-compat~
%if 0%{?rhel} == 6
%patch1010 -p0 -b .libstdc++44-xfail~
%endif

sed -i -e 's/4\.7\.1/4.7.0/' gcc/BASE-VER
echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

%if 0%{?rhel} >= 6
# Default to -gdwarf-3 rather than -gdwarf-2
sed -i '/UInteger Var(dwarf_version)/s/Init(2)/Init(3)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)2\./\13./' gcc/doc/invoke.texi
%endif
# Default to -fno-debug-types-section -grecord-gcc-switches
sed -i '/flag_debug_types_section/s/Init(1)/Init(0)/' gcc/common.opt
sed -i '/dwarf_record_gcc_switches/s/Init(0)/Init(1)/' gcc/common.opt

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

%build

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if 0%{?rhel} < 6
mkdir gmp gmp-install
cd gmp
../../gmp-%{gmp_version}/configure --disable-shared \
  --enable-cxx --enable-mpbsd --build=%{_build} --host=%{_host} \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
  --prefix=`cd ..; pwd`/gmp-install
make %{?_smp_mflags}
make install
cd ..

mkdir mpfr mpfr-install
cd mpfr
../../mpfr-%{mpfr_version}/configure --disable-shared \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
  --prefix=`cd ..; pwd`/mpfr-install --with-gmp=`cd ..; pwd`/gmp-install
make %{?_smp_mflags}
make install
cd ..
%endif

mkdir mpc mpc-install
cd mpc
../../mpc-%{mpc_version}/configure --disable-shared \
  CFLAGS="${CFLAGS:-%optflags}" CXXFLAGS="${CXXFLAGS:-%optflags}" \
%if 0%{?rhel} < 6
  --with-gmp=`cd ..; pwd`/gmp-install --with-mpfr=`cd ..; pwd`/mpfr-install \
%endif
  --prefix=`cd ..; pwd`/mpc-install
make %{?_smp_mflags}
make install
cd ..

CC=gcc
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
%endif
%ifarch ppc64
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
fi
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables/' \
      ../gcc/Makefile.in
    ;;
esac
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="`echo $OPT_FLAGS | sed 's/ -Wall / /g'`" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla --disable-bootstrap \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--disable-build-with-cxx --disable-build-poststage1-with-cxx \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
%if 0%{?rhel} >= 6
	--enable-gnu-unique-object \
%else
	--disable-gnu-unique-object \
%endif
%if 0%{?rhel} >= 6
	--enable-linker-build-id \
%else
	--disable-linker-build-id \
%endif
	--enable-languages=c,c++,lto \
	--enable-plugin --with-linker-hash-style=gnu \
	--disable-libgcj \
	--without-ppl --without-cloog \
%if 0%{?rhel} == 5
	--with-gmp=`pwd`/gmp-install --with-mpfr=`pwd`/mpfr-install \
%endif
	--with-mpc=`pwd`/mpc-install \
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%if 0%{?rhel} >= 6
%ifarch ppc ppc64
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch %{ix86}
%if 0%{?rhel} >= 6
	--with-arch=i686 \
%else
	--with-arch=i586 \
%endif
%endif
%ifarch x86_64
%if 0%{?rhel} >= 6
	--with-arch_32=i686 \
%else
	--with-arch_32=i586 \
%endif
%endif
%ifarch s390 s390x
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform}
%endif

GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS"

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/libitm

(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -fr %{buildroot}

cd obj-%{gcc_target_platform}

mkdir -p %{buildroot}%{_prefix}/%{_lib}
mkdir -p %{buildroot}%{_infodir}
cp -a %{gcc_target_platform}/libitm/.libs/libitm.so.1* %{buildroot}%{_prefix}/%{_lib}/
cp -a %{gcc_target_platform}/libitm/libitm.info %{buildroot}%{_infodir}/

%check
cd obj-%{gcc_target_platform}

# Test against the system libstdc++.so.6 + libstdc++_nonshared.a combo
mv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6{,.not_here}
mv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so{,.not_here}
ln -f %{_prefix}/%{_lib}/libstdc++.so.6 \
  %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{_prefix}/%{_lib}/libstdc++.so.6 -lstdc++_nonshared )' \
  > %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so
cp -a %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a \
  %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared.a

# run the tests.
make %{?_smp_mflags} -k check-target-libitm RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
( LC_ALL=C ../contrib/test_summary -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults
echo ====================TESTING=========================
cat testresults
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
if [ -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%preun
if [ $1 = 0 -a -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*
%doc gcc/COPYING3 COPYING.RUNTIME rpm.doc/libitm/*

%changelog
* Tue May 29 2012 Jakub Jelinek <jakub@redhat.com> 4.7.0-5.1.1
- new package
