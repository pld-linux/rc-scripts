# $Id: rc-scripts.spec,v 1.13 1999-07-28 00:06:19 kloczek Exp $
Summary:	inittab and /etc/rc.d scripts
Summary(de):	inittab und /etc/rc.d Scripts
Summary(fr):	inittab et scripts /etc/rc.d
Summary(pl):	inittab i skrypty startowe z katalogu /etc/rc.d
Summary(tr):	inittab ve /etc/rc.d dosyalar�
Name:		rc-scripts
Version:	0.0.7
Release:	1
Copyright:	GPL
Group:		Base
Group(pl):	Bazowe	
Source:		%{name}-%{version}.tar.gz
BuildPrereq:	popt-devel
Requires:	mingetty
Requires:	mktemp
Requires:	modutils >= 2.1.121
Requires:	textutils
Requires:	sh-utils
Requires:	/bin/nice
Requires:	/bin/basename
Requires:	/bin/awk
Requires:	procps
Requires:	/bin/ps
Requires:	SysVinit
Requires:	sed
Requires:	net-tools
Requires:	iproute2
Prereq:		/sbin/chkconfig
Obsoletes:	initscripts
Provides:	initscripts
Buildroot:	/tmp/%{name}-%{version}-root

%define		_prefix		/usr
%define		_exec_prefix	/
%define		_sysconfdir	/etc

%description
This package contains the scripts use to boot a system, change run
levels, and shut the system down cleanly.

%description -l de
Dieses Paket enth�lt die Scripts, die zum Hochfahren des Systems, �ndern
der Betriebsebene und sauberem Herunterfahren des Systems erforderlich sind.
Au�erdem enth�lt es die Scripts, die Netzwerkschnittstellen aktivieren und
deaktivieren.

%description -l fr
Ce package contient les scripts utilis�s pour d�marrer le syst�me,
changer les niveaux d'ex�cution, et arr�ter le syst�me proprement.
Il contient aussi les scripts qui activent et d�sactivent la plupart
des inetrfaces r�seau.

%description -l pl
Pakiet zawiera skrypty uruchamiane przy starcie i zamykaniu systemu, a
tak�e przy zmianie poziomu uruchomienia. 

%description -l tr
Bu paket, sistem a�mak, �al��ma d�zeylerini de�i�tirmek ve sistemi d�zg�n bir
�ekilde kapatmak i�in gereken dosyalar� i�erir. Ayr�ca pek �ok bilgisayar a��
aray�zlerini etkinle�tiren ya da edilginle�tiren programc�klar i�erir.

%prep
%setup -q

%build
LDFLAGS="-s"; export LDFLAGS
%configure 
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/run/netreport

make install  \
	DESTDIR=$RPM_BUILD_ROOT 
	
	
gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	doc/*.txt 

%post
for i in  halt random reboot single  network nfsfs allowlogin
	do /sbin/chkconfig --add $i
done 
if [ -f /etc/inittab.rpmsave ]; then
	echo "**** Found old /etc/inittab.rpmsave ****"
	echo "/etc/inittab renamed to /etc/inittab.rpmnew"
	mv /etc/inittab /etc/inittab.rpmnew
	echo "/etc/inittab.rpmsave renamed to /etc/inittab."
	mv /etc/inittab.rpmsave /etc/inittab
fi
for l in /etc/sysconfig/network-scripts/ifcfg-* ; do 
  if [ -f "$l" ] ; then
    NEWNAME=`basename $l | sed -e 's/^ifcfg-//'`
    [ -f /etc/sysconfig/interfaces/$NEWNAME ] || cp $l /etc/sysconfig/interfaces/$NEWNAME
  fi
done

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del random
	/sbin/chkconfig --del nfsfs
	/sbin/chkconfig --del network
fi

%files
%defattr(644,root,root,754)
%doc doc/sysconfig.txt.gz
%doc sysconfig/interfaces/ifc*
%doc sysconfig/interfaces/tnl*
%doc sysconfig/interfaces/data/chat-ppp*
%doc doc/net-scripts.txt.gz

%{_sysconfdir}/rc.d/init.d/functions
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/allowlogin
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/halt
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/killall
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/random
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/reboot
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/shutdwn
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/single

%attr(754,root,root) %{_sysconfdir}/rc.d/rc.sysinit
%attr(754,root,root) %{_sysconfdir}/rc.d/rc
%attr(754,root,root) %{_sysconfdir}/rc.d/rc.local

%attr(755,root,root) %{_sysconfdir}/profile.d/lang.sh

%attr(755,root,root) %{_bindir}/doexec
%attr(755,root,root) %{_bindir}/usleep
%attr(755,root,root) %{_sbindir}/setsysfont
%attr(755,root,root) %{_sbindir}/initlog
%attr(755,root,root) %{_sbindir}/loglevel
%attr(755,root,root) %{_bindir}/ipcalc
%attr(755,root,root) %{_sbindir}/usernetctl
%attr(755,root,root) %{_sbindir}/netreport

%attr(755,root,root) %{_sbindir}/if*
%attr(755,root,root) %{_sbindir}/tnl*

%{_sysconfdir}/rc.d/init.d/functions.network
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/network
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/nfsfs
%attr(750,root,root) %dir /var/run/netreport
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig/interfaces
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig/interfaces/data
%attr(755,root,root) %dir %{_sysconfdir}/ppp
%attr(755,root,root) %{_sysconfdir}/ppp/*
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig/network-scripts
%attr(755,root,root) %{_sysconfdir}/sysconfig/network-scripts/if*

%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/network
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/static-routes
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/static-nat
%config            %verify(not size mtime md5) %{_sysconfdir}/sysconfig/interfaces/ifcfg-lo
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adjtime
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/inittab
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/system

%{_mandir}/man1/*

$Log: rc-scripts.spec,v $
Revision 1.13  1999-07-28 00:06:19  kloczek
- updated spec.

Revision 1.12  1999/07/27 23:59:51  kloczek
- update to 0.0.7 first working release,
- main chanes is configuring network interfaces with using iproute2 tools
  instead net-tools,
- many other changes and fixes (look at Changelog),
- removed ipchains-setup (we have firewall-init scripts).

Revision 1.11  1999/07/12 23:06:14  kloczek
- added using CVS keywords in %changelog (for automating them).

* Thu Apr 29 1999 PLD Team <bugs@pld.org.pl>
  [0.0.5-1]
- automake/autoconf support

* Wed Apr 28 1999 PLD Team <bugs@pld.org.pl>
  [0.0.4-1]
- added ipchains-setup  

* Thu Apr 22 1999 PLD Team <bugs@pld.org.pl>
  [0.0.3-1]
- split into two packages: rc-scripts & net-scripts  
- directory structure changed - only config in /etc

* Tue Mar 23 1999 PLD Team <bugs@pld.org.pl>
  [0.0.2-1]
- be more verbose while upgrading when /etc/inittab.rpmsave is found,
- added seting NETWORK="no" variable to when /etc/sysconfig/network is not present
  or when NETWORK in this file is not defined.

* Sun Mar 21 1999 PLD Team <bugs@pld.org.pl>
  [0.0.1-1]
- added /etc/sysconfig/system,
- removed man group from man pages,
- added in %post not replacing /etc/inittab on upgrade from initscripts,
- removed %config from scripts.

* Fri Mar 19 1999 PLD Team <bugs@pld.org.pl>
- Modified handling ppp links. Added new features to ifcfg-ppp
  and changed syntax of chat scripts for ppp.
- First Release.
- Package based on RedHat's initscripts-3.78.
