%global _hardened_build 1
%global commit_long     8d188fa0e00bb8c6ff6eddd07bf92857e9bd533a
%global commit_short    %(c=%{commit_long}; echo ${c:0:7})

Name:       wiringpi
Version:    2.46
Release:    1%{?dist}
Summary:    PIN based GPIO access library for BCM283x SoC devices
License:    LGPLv3
URL:        http://wiringpi.com
Source0:    https://git.drogon.net/?p=wiringPi;a=snapshot;h=%{commit_long};sf=tgz#/wiringPi-%{commit_short}.tar.gz
Patch0:     0001-Makefiles.patch
ExclusiveArch: %{arm}

BuildRequires: gcc


%description
WiringPi is a PIN based GPIO access library for the BCM2835, BCM2836 and
BCM2837 SoC devices (Raspberry Pi devices). It is usable from C,
C++ and RTB (BASIC) as well as many other languages with suitable
wrappers.


%package tools
Summary:    Utility tools for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description tools
The wiringPi gpio utility is used for command line GPIO access. It be used in
scripts to manipulate the GPIO pins, set outputs and read inputs.


%package devel
Summary:    Development libraries for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
WiringPi development libraries to allow GPIO access on a Raspberry Pi from C
and C++ programs.


%prep
%autosetup -p1 -n wiringPi-%{commit_short}


%build
# Build libraries
for i in wiringPi devLib; do
    pushd $i
    make %{?_smp_mflags} DEBUG="%{optflags}" LDFLAGS="%{__global_ldflags}"
    popd
done

# Build GPIO utility
pushd gpio
make %{?_smp_mflags} DEBUG="%{optflags}" \
LDFLAGS="-L../wiringPi -L../devLib %{__global_ldflags}"
popd

# Create pkgconfig files
%{__cat} << EOF > wiringPi.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: wiringPi
Description: wiringPi library
Version: %{version}
Libs: -L%{_libdir} -lwiringPi -lpthread
Cflags: -I%{_includedir}/wiringPi
EOF

%{__cat} << EOF > wiringPiDev.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: wiringPiDev
Description: wiringPi device library
Version: %{version}
Libs: -L%{_libdir} -lwiringPi -lwiringPiDev -lpthread
Cflags: -I%{_includedir}/wiringPi
EOF

# Fix spurious executable perm
chmod -x examples/PiFace/ladder.c


%install
# Install libraries & GPIO utility
for i in wiringPi devLib gpio; do
    pushd $i
    make install-fedora DESTDIR=%{buildroot} PREFIX=%{_prefix} LIBDIR=%{_libdir}
    popd
done

# Install pkgconfig files
%{__mkdir} -p %{buildroot}%{_libdir}/pkgconfig
%{__install} -p -m 0644 *.pc %{buildroot}%{_libdir}/pkgconfig/


%ldconfig_scriptlets


%files devel
%defattr(-,root,root)
%doc examples
%dir %{_includedir}/wiringPi
%{_libdir}/pkgconfig/*.pc
%{_includedir}/wiringPi/*.h


%files tools
%defattr(-,root,root)
%{_bindir}/gpio
%{_mandir}/man1/*.1.*


%files
%defattr(-,root,root)
%doc People README.TXT pins/pins.pdf
%license COPYING.LESSER
%{_libdir}/libwiringPi.so.*
%{_libdir}/libwiringPiDev.so.*


%changelog
* Mon May 14 2018 Vaughan Agrez <devel@agrez.net> - 2.46-1
- Import into Fedora
