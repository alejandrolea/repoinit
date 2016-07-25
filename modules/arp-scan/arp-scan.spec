# $Id$
# Authority: dag
# Upstream: Roy Hills

%{!?dtag:%define _with_libpcapdevel 1}
%{?el6:%define _with_libpcapdevel 1}
%{?el5:%define _with_libpcapdevel 1}

Summary: ARP scanning and fingerprinting tool
Name: arp-scan
Version: %{__version}
Release: %{__release}%{?dist}
License: GPL
Group: Applications/Internet
URL: http://www.nta-monitor.com/tools-resources/security-tools/arp-scan

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

#Source: http://www.nta-monitor.com/files/arp-scan/arp-scan-%{version}.tar.gz
Source: https://github.com/royhills/arp-scan/releases/download/%{version}/arp-scan-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

#BuildRequires: libdnet-devel
BuildRequires: libpcap
%{?_with_libpcapdevel:BuildRequires:libpcap-devel}

%description
arp-scan sends ARP (Address Resolution Protocol) queries to the specified
targets, and displays any responses that are received. It allows any part
of the outgoing ARP packets to be changed, allowing the behavior of targets
to non-standard ARP packets to be examined. The IP address and hardware
address of received packets are displayed, together with the vendor details.

These details are obtained from the IEEE OUI and IAB listings, plus a few
manual entries. It includes arp-fingerprint, which allows a system to be
fingerprinted based on how it responds to non-standard ARP packets.

%prep
%setup

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO
%doc %{_mandir}/man1/arp-fingerprint.1*
%doc %{_mandir}/man1/arp-scan.1*
%doc %{_mandir}/man1/get-iab.1*
%doc %{_mandir}/man1/get-oui.1*
%doc %{_mandir}/man5/mac-vendor.5*
%{_bindir}/arp-fingerprint
%{_bindir}/arp-scan
%{_bindir}/get-iab
%{_bindir}/get-oui
%{_datadir}/arp-scan/

%changelog
* Tue Sep 24 2013 Dag Wieers <dag@wieers.com> - 1.9-1
- Updated to release 1.9.

* Mon Aug 01 2011 Dag Wieers <dag@wieers.com> - 1.8.1-1
- Updated to release 1.8.1.

* Wed Mar 09 2011 Dag Wieers <dag@wieers.com> - 1.8-1
- Updated to release 1.8.

* Wed Oct 15 2008 Dag Wieers <dag@wieers.com> - 1.7-1
- Updated to release 1.7.

* Sun Apr 15 2007 Dag Wieers <dag@wieers.com> - 1.6-1
- Updated to release 1.6.

* Thu Jul 27 2006 Dag Wieers <dag@wieers.com> - 1.5-1
- Initial package. (using DAR)
