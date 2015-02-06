Summary:	ARP reply daemon
Name:		arpd
Version:	0.2
Release:	13
Group:		System/Servers
License:	BSD
URL:		http://niels.xtdnet.nl/honeyd/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}.init.bz2
Source2:	%{name}.sysconfig.bz2
Patch0:		arpd-0.2-gcc34.diff
Requires(preun): rpm-helper
Requires(post): rpm-helper
BuildRequires:	libevent0.9-devel
BuildRequires:	dnet-devel
BuildRequires:	pcap-devel = 1.3.0-2
BuildRequires:	flex
BuildRequires:	bison

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
    --localstatedir=%{_localstatedir}/lib \
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


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2-11mdv2011.0
+ Revision: 616604
- the mass rebuild of 2010.0 packages

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.2-10mdv2010.0
+ Revision: 436671
- rebuild

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-9mdv2009.1
+ Revision: 298232
- rebuilt against libpcap-1.0.0

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2-8mdv2009.0
+ Revision: 238993
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2-7mdv2008.0
+ Revision: 83891
- bump release
- fix deps
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - fix prereq


* Fri Dec 22 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-5mdv2007.0
+ Revision: 101561
- Import arpd

* Mon Jun 19 2006 Emmanuel Andry <eandry@mandriva.org> 0.2-5mdv2007.0
- rebuild
- %%mkrel

* Thu Jul 14 2005 Oden Eriksson <oeriksson@mandriva.com> 0.2-4mdk
- rebuilt against new libpcap-0.9.1 (aka. a "play safe" rebuild)

* Mon Jan 17 2005 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.2-3mdk
- fix deps and build

* Mon Dec 22 2003 Michael Scherer <misc@mandrake.org> 0.2-2mdk
- correct initscript
- remove explicit lib Requires

