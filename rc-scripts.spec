# $Id: rc-scripts.spec,v 1.63 2001-02-23 20:52:49 aflinta Exp $
Summary:	inittab and /etc/rc.d scripts
Summary(de):	inittab und /etc/rc.d Scripts
Summary(fr):	inittab et scripts /etc/rc.d
Summary(pl):	inittab i skrypty startowe z katalogu /etc/rc.d
Summary(tr):	inittab ve /etc/rc.d dosyalar�
Name:		rc-scripts
Version:	0.2.10
Release:	2
License:	GPL
Group:		Base
Group(de):	Gr�nds�tzlich
Group(pl):	Podstawowe
Source0:	%{name}-%{version}.tar.gz
Patch0:		%{name}-shared.patch
Patch1:		%{name}-typo.patch
URL:		http://cvs.pld.org.pl/index.cgi/rc-scripts/
Vendor:		PLD rc-scripts Team <pld-rc-scripts@pld.org.pl>
BuildRequires:	popt-devel
BuildRequires:	glib-devel
%{!?bcond_off_static:BuildRequires:	glib-static}
BuildRequires:	gettext-devel
Requires:	grep
Requires:	mingetty
Requires:	mktemp
Requires:	modutils >= 2.1.121
Requires:	fileutils
Requires:	textutils
Requires:	sh-utils
Requires:	/bin/nice
Requires:	/bin/basename
Requires:	/bin/awk
Requires:	procps
Requires:	/bin/ps
Requires:	SysVinit
Requires:	iproute2
Requires:	/bin/gettext
Requires:	gettext
Requires:	e2fsprogs >= 1.15
Requires:	mount >= 2.10
Requires:	bdflush
Requires:	utempter
Requires:	net-tools
Obsoletes:	initscripts
Provides:	initscripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr
%define		_exec_prefix	/
%define		_sysconfdir	/etc
%define		localedir	/etc/sysconfig/locale

%description
This package contains the scripts use to boot a system, change run
levels, and shut the system down cleanly.

%description -l de
Dieses Paket enth�lt die Scripts, die zum Hochfahren des Systems,
�ndern der Betriebsebene und sauberem Herunterfahren des Systems
erforderlich sind. Au�erdem enth�lt es die Scripts, die
Netzwerkschnittstellen aktivieren und deaktivieren.

%description -l fr
Ce package contient les scripts utilis�s pour d�marrer le syst�me,
changer les niveaux d'ex�cution, et arr�ter le syst�me proprement. Il
contient aussi les scripts qui activent et d�sactivent la plupart des
inetrfaces r�seau.

%description -l pl
Pakiet zawiera skrypty uruchamiane przy starcie i zamykaniu systemu, a
tak�e przy zmianie poziomu uruchomienia.

%description -l tr
Bu paket, sistem a�mak, �al��ma d�zeylerini de�i�tirmek ve sistemi
d�zg�n bir �ekilde kapatmak i�in gereken dosyalar� i�erir. Ayr�ca pek
�ok bilgisayar a�� aray�zlerini etkinle�tiren ya da edilginle�tiren
programc�klar i�erir.

%prep
%setup -q
%{!?bcond_off_static:#}
%patch0 -p1
%patch1 -p1

%build
%configure \
	--with-localedir=%{localedir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/run/netreport

%{__make} install  \
	DESTDIR=$RPM_BUILD_ROOT 

for i in 0 1 2 3 4 5 6; do
	install -d $RPM_BUILD_ROOT/etc/rc.d/rc$i.d
done

for i in 2 3 4 5; do
	ln -s ../rc.local $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S99local
	ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S10network
	ln -s ../init.d/allowlogin $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S99allowlogin
	ln -s ../init.d/timezone $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S10timezone
done

for i in 1 2 3 4 5; do
	ln -s ../init.d/killall $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S00killall
	ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S20random
done

for i in 0 2 3 4 5 6; do
	ln -s ../init.d/single $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K00single
done

ln -s ../init.d/single $RPM_BUILD_ROOT/etc/rc.d/rc1.d/S00single

for i in 0 6; do
	ln -s ../init.d/killall $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K90killall
	ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K80random
done

for i in 0 1 6; do
	ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K90network
	ln -s ../init.d/allowlogin $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K01allowlogin
done

gzip -9nf doc/*.txt rc.d/init.d/template.init

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/inittab.rpmsave ]; then
	echo "**** Found old /etc/inittab.rpmsave ****"
	echo "/etc/inittab renamed to /etc/inittab.rpmnew"
	mv -f /etc/inittab /etc/inittab.rpmnew
	echo "/etc/inittab.rpmsave renamed to /etc/inittab."
	mv -f /etc/inittab.rpmsave /etc/inittab
fi

%files
%defattr(644,root,root,755)
%doc doc/sysconfig.txt.gz
%doc sysconfig/interfaces/ifc*
%doc sysconfig/interfaces/tnl*
%doc sysconfig/interfaces/data/chat-ppp*
%doc doc/net-scripts.txt.gz
%doc rc.d/init.d/template.init.gz

%attr(755,root,root) %dir %{_sysconfdir}/rc.d
%attr(755,root,root) %dir %{_sysconfdir}/rc.d/rc?.d
%attr(755,root,root) %dir %{_sysconfdir}/rc.d/init.d

%{_sysconfdir}/rc.d/init.d/functions
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/allowlogin
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/killall
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/random
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/single
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/timezone
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/network

%attr(754,root,root) %{_sysconfdir}/rc.d/rc.sysinit
%attr(754,root,root) %{_sysconfdir}/rc.d/rc
%attr(754,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/rc.d/rc.local
%attr(754,root,root) %{_sysconfdir}/rc.d/rc.shutdown
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/S??local
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/S??allowlogin
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/S??killall
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/S??network
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/S??random
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/S??single
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/S??timezone
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/K??allowlogin
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/K??killall
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/K??network
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/K??random
%attr(754,root,root) %{_sysconfdir}/rc.d/rc?.d/K??single

%attr(755,root,root) %{_sysconfdir}/profile.d/lang.sh

%attr(755,root,root) %{_bindir}/doexec
%attr(755,root,root) %{_bindir}/usleep
%attr(755,root,root) %{_bindir}/ipcalc
%attr(755,root,root) %{_bindir}/resolvesymlink
%attr(755,root,root) %{_bindir}/run-parts

%attr(755,root,root) %{_sbindir}/setsysfont
%attr(755,root,root) %{_sbindir}/initlog
%attr(755,root,root) %{_sbindir}/loglevel
%attr(755,root,root) %{_sbindir}/usernetctl
%attr(755,root,root) %{_sbindir}/netreport

%attr(755,root,root) %{_sbindir}/if*
%attr(755,root,root) %{_sbindir}/tnl*

%attr(755,root,root) %{_sbindir}/getkey

%attr(750,root,root) %dir /var/run/netreport
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig/interfaces
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig/interfaces/data
%attr(755,root,root) %dir %{_sysconfdir}/ppp
%attr(755,root,root) %{_sysconfdir}/ppp/*
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig/network-scripts
%attr(755,root,root) %{_sysconfdir}/sysconfig/network-scripts/if*
%{_sysconfdir}/sysconfig/network-scripts/.functions
%dir %{_sysconfdir}/sysconfig/interfaces/up.d
%dir %{_sysconfdir}/sysconfig/interfaces/down.d
%dir %{_sysconfdir}/sysconfig/interfaces/up.d/*
%dir %{_sysconfdir}/sysconfig/interfaces/down.d/*
%attr(755,root,root) %{_sysconfdir}/sysconfig/interfaces/up.d/ppp/logger
%attr(755,root,root) %{_sysconfdir}/sysconfig/interfaces/down.d/ppp/logger

%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/i18n
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/network
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/static-routes
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/static-nat
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/timezone
#%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/clock
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adjtime
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/inittab
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/system

%{_mandir}/man1/*

%dir %{localedir}
%lang(pl) %{localedir}/pl
%lang(de) %{localedir}/de
