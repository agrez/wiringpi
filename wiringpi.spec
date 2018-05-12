%global _hardened_build 1
%global commit_long     8d188fa0e00bb8c6ff6eddd07bf92857e9bd533a
%global commit_short    %(c=%{commit_long}; echo ${c:0:7})

Name:       wiringpi
Version:    2.46
Summary:    WiringPi is a PIN based GPIO access library for BCM283x SoC devices
Release:    1.git%{commit_short}%{?dist}
License:    LGPLv3
URL:        http://wiringpi.com
Source0:    https://git.drogon.net/?p=wiringPi;a=snapshot;h=%{commit_long};sf=tgz#/wiringPi-%{commit_short}.tar.gz
Patch0:     0001-Makefiles.patch
ExclusiveArch:  armv7hl

%description
WiringPi is a PIN based GPIO access library for the BCM2835, BCM2836 and
BCM2837 SoC devices (Raspberry Pi devices). It is usable from C,
C++ and RTB (BASIC) as well as many other languages with suitable
wrappers. The wiringPi gpio utility is used for command line GPIO access.


%package libs
Summary: Shared libraries for %{name}

%description libs
WiringPi is a PIN based GPIO access library for the BCM2835, BCM2836 and
BCM2837 SoC devices used in all Raspberry Pi devices. It is usable from C,
C++ and RTB (BASIC) as well as many other languages with suitable
wrappers.


%package devel
Summary: Development libraries for %{name}
Requires: %{name}-libs = %{version}-%{release}

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


%install
# Install libraries & GPIO utility
for i in wiringPi devLib gpio; do
    pushd $i
    make install-fedora DESTDIR=%{buildroot} PREFIX=%{_prefix}
    popd
done


%if 0%{?fedora} < 28
%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig
%endif


%files libs
%defattr(-,root,root)
%license COPYING.LESSER
%{_libdir}/libwiringPi.so.*
%{_libdir}/libwiringPiDev.so.*


%files devel
%defattr(-,root,root)
%license COPYING.LESSER
%dir %{_includedir}/wiringPi
%{_includedir}/wiringPi/*.h
%{_libdir}/libwiringPi.so
%{_libdir}/libwiringPiDev.so


%files
%defattr(-,root,root)
%license COPYING.LESSER
%doc People README.TXT VERSION pins/pins.pdf
%attr(4755,root,root) %{_bindir}/gpio
%{_mandir}/man1/*.1.*


%changelog
* Tue May 08 2018 Vaughan Agrez <devel@agrez.net> - 2.46-1.git8d188fa
- Import into Fedora
