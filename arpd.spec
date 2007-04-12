%define	name	arpd
%define	version	0.2
%define	release	%mkrel 5

Summary:	ARP reply daemon
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Servers
License:	BSD
URL:		http://niels.xtdnet.nl/honeyd/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}.init.bz2
Source2:	%{name}.sysconfig.bz2
Patch0:		arpd-0.2-gcc34.diff
PreReq:		rpm-helper
BuildRequires:	libevent0.9-devel
BuildRequires:	libdnet-devel
BuildRequires:	libpcap-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
arpd replies to any ARP request for an IP address matching the
specified destination net with the hardware MAC address of the
specified interface, but only after determining if another host
already claims it.

%prep

%setup -q -n %{name}
%patch0 -p0

# libevent0.9 fix
perl -pi -e "s|event\.h|libevent0\.9\.h|g" *
perl -pi -e "s|libevent\.a|libevent0\.9\.a|g" *

# lib64 fix
perl -pi -e "s|\\\$withval/lib/|\\\${libdir}/|g" configure*
perl -pi -e "s|\\\$withval/lib |\\\${libdir} |g" configure*
perl -pi -e "s|\-L\\\${prefix}/lib|\-L\\\${libdir}|g" configure*
perl -pi -e "s|\\\${prefix}/lib/|\\\${libdir}/|g" configure*
perl -pi -e "s|\-levent|\-levent0.9|g" configure*

bzcat %{SOURCE1} > %{name}.init
bzcat %{SOURCE2} > %{name}.sysconfig

%build

export CFLAGS="%{optflags} -fPIC"

./configure \
    --enable-shared \
    --enable-static \
    --prefix=%{_prefix} \
    --exec-prefix=%{_exec_prefix} \
    --bindir=%{_sbindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8

install -m755 %{name} %{buildroot}%{_sbindir}/%{name}
install -m644 %{name}.8 %{buildroot}%{_mandir}/man8/%{name}.8

install -m755 %{name}.init %{buildroot}%{_initrddir}/%{name}
install -m644 %{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE
%config(noreplace) %attr(0755,root,root) %{_initrddir}/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0644,root,root) %{_mandir}/man8/%{name}.8*


