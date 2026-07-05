%global source_name linuxigd

Name: linux-igd
Summary: The Linux UPNP Internet GATEWAY DEVICE
Version: 1.0
Release: 24%{?dist}
License: GPL-2.0-or-later
# Upstream is abandoned (last release 2007); SourceForge downloads return 404; no local tarball available
URL: https://linux-igd.sourceforge.net/index.php
ExclusiveArch: x86_64 aarch64
Source0: https://downloads.sourceforge.net/project/%{name}/%{source_name}-%{version}.tar.gz
Source1: upnpd.service
Patch1: %{source_name}-%{version}.patch
Patch0: %{name}-%{version}-to-cvs20070630.patch
Patch2: %{source_name}-%{version}-restrict-internal-interface.patch
Patch3: linux-igd-includes.patch

BuildRequires: systemd-rpm-macros
BuildRequires: libupnp-devel

%{?systemd_requires}


%description
This is a daemon that emulates Microsoft's Internet Connection Service (ICS).
It implements the UPnP Internet Gateway Device specification (IGD) and allows
UPnP aware clients, such as MSN Messenger to work properly from behind
a Linux NAT firewall.


%prep
%setup -q -c -n %{name}
%patch0
%patch1
%patch2
%patch3 -p1


%build
pushd %{source_name}-%{version}
%make_build CFLAGS="$RPM_OPT_FLAGS"
popd


%install
pushd %{source_name}-%{version}
%make_install
iconv -f latin1 -t utf8 CHANGES > ../CHANGES
iconv -f latin1 -t utf8 TODO > ../TODO
cp LICENSE ../
popd

rm -rf %{buildroot}%{_initrddir}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/upnpd.service


%files
%license LICENSE
%doc CHANGES TODO
%dir %{_sysconfdir}/linuxigd/
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/linuxigd/*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/upnpd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/upnpd
%attr(0644,root,root) %{_mandir}/man8/upnpd.8.gz
%{_sbindir}/upnpd
%{_unitdir}/upnpd.service


%post
%systemd_post upnpd.service


%preun
%systemd_preun upnpd.service


%postun
%systemd_postun_with_restart upnpd.service


%changelog
* Sat Jul 04 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.0-24
- Source0: http→https; dead upstream (2007), SourceForge 404, no local tarball
- URL: http→https; drop RHEL8 conditional; always BuildRequires: systemd-rpm-macros
- SPDX: GPL+ → GPL-2.0-or-later; add ExclusiveArch: x86_64 aarch64
- %%make_build, %%make_install

* Fri Apr 24 2026 CasjaysDev <rpm-devel@casjaysdev.pro> - 1.0-24
- Modernize spec for AlmaLinux 10; remove %clean section

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Sep 10 2014 Michael Cronenworth <mike@cchtml.com> - 1.0-19
- Many packaging fixes (BZ# 850189, 903740)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 10 2012 Jon Ciesla <limburgher@gmail.com> - 1.0-13
- Migrate to systemd, BZ 789751.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 4 2008 Masahiro Hasegawa <masahase@gmail.com> - 1.0-7
- Fix Bug #457730

* Sat May 17 2008 Masahiro Hasegawa <masahase@gmail.com> - 1.0-6
- Fix dependencies

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-5
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Masahiro Hasegawa <masahase@gmail.com> - 1.0-4
- Merge CVS 20070630

* Tue Dec 25 2007 Masahiro Hasegawa <masahase@gmail.com> - 1.0-3
- more rewritten by Fedora's rule

* Tue Dec 25 2007 Masahiro Hasegawa <masahase@gmail.com> - 1.0-2
- more rewritten by Fedora's rule

* Mon Dec 24 2007 Masahiro Hasegawa <masahase@gmail.com>
- Rewritten by Fedora's rule

* Wed Oct 31 2007 Masahiro Hasegawa <masahase@gmail.com>
- Version 1.0 release
- first build for version 1.0 (Release)

* Mon Aug 14 2006 Tim Brody <tdb01r@ecs.soton.ac.uk>
- Version 0.95 Release 1
- first build for version 0.95 (Release)

* Sun Sep 26 2004 Watanabe Keiji <k@elt.ne.jp>
- Version 0.99 Release ELT1
- first build for version 0.92 (CVS Version on Sep 25, 2004.)
