#
# Conditional build:
%bcond_without	static	# link binaries with glib dynamically
#
Summary:	inittab and /etc/rc.d scripts
Summary(de):	inittab und /etc/rc.d Scripts
Summary(fr):	inittab et scripts /etc/rc.d
Summary(pl):	inittab i skrypty startowe z katalogu /etc/rc.d
Summary(tr):	inittab ve /etc/rc.d dosyalar�
Name:		rc-scripts
Version:	0.4.0.6
Release:	0.2
License:	GPL
Vendor:		PLD rc-scripts Team <pld-rc-scripts@pld-linux.org>
Group:		Base
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	23f3c0e5194a75d3717d9d22c38446e4
Patch0:		%{name}-quotation-marks.patch
URL:		http://svn.pld-linux.org/cgi-bin/svnview/rc-scripts/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib-devel
%{?with_static:BuildRequires:	glib-static}
BuildRequires:	popt-devel
BuildRequires:	pkgconfig
Requires(post):	fileutils
Requires:	/bin/awk
Requires:	/bin/basename
Requires:	/bin/gettext
Requires:	/bin/nice
Requires:	/bin/ps
Requires:	FHS >= 2.2-6
Requires:	SysVinit
Requires:	e2fsprogs >= 1.15
Requires:	fileutils
Requires:	findutils
Requires:	gettext
Requires:	grep
Requires:	iproute2
Requires:	mingetty
Requires:	mktemp
Requires:	module-init-tools
Requires:	mount >= 2.10
Requires:	net-tools
Requires:	procps
Requires:	sh-utils
Requires:	textutils
Requires:	utempter
Requires:	util-linux
Provides:	initscripts
Obsoletes:	initscripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	LPRng < 3.8.0-2
Conflicts:	psacct < 6.3.5-10
Conflicts:	openssh-server < 2:3.6.1p2-6

%define		_exec_prefix	/
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
tak�e przy zmianie jego poziomu pracy.

%description -l tr
Bu paket, sistem a�mak, �al��ma d�zeylerini de�i�tirmek ve sistemi
d�zg�n bir �ekilde kapatmak i�in gereken dosyalar� i�erir. Ayr�ca pek
�ok bilgisayar a�� aray�zlerini etkinle�tiren ya da edilginle�tiren
programc�klar i�erir.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--with-localedir=%{localedir}
%{__make} \
	%{!?with_static:ppp_watch_LDADD="-lglib" ppp_watch_DEPENDENCIES=}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/{run/netreport,log}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	%{!?with_static:ppp_watch_LDADD="-lglib" ppp_watch_DEPENDENCIES=}

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

install sysconfig/interfaces/ifcfg-eth0 $RPM_BUILD_ROOT/etc/sysconfig/interfaces
> $RPM_BUILD_ROOT/var/log/dmesg

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
touch /var/log/dmesg
chmod 000 /var/log/dmesg
chown root:root /var/log/dmesg
chmod 640 /var/log/dmesg

# move network interfaces description files to new location
%triggerpostun -- initscripts
mv -f /etc/sysconfig/network-scripts/ifcfg-* /etc/sysconfig/interfaces

%files
%defattr(644,root,root,755)
%doc doc/*.txt rc.d/init.d/template.init
%doc sysconfig/interfaces/data/chat-ppp*
%doc sysconfig/interfaces/ifc*
%doc sysconfig/interfaces/tnl*

%attr(755,root,root) %dir /etc/rc.d
%attr(755,root,root) %dir /etc/rc.d/init.d
%attr(755,root,root) %dir /etc/rc.d/rc?.d

/etc/rc.d/init.d/functions
%attr(754,root,root) /etc/rc.d/init.d/allowlogin
%attr(754,root,root) /etc/rc.d/init.d/killall
%attr(754,root,root) /etc/rc.d/init.d/network
%attr(754,root,root) /etc/rc.d/init.d/random
%attr(754,root,root) /etc/rc.d/init.d/single
%attr(754,root,root) /etc/rc.d/init.d/timezone

%attr(754,root,root) /etc/rc.d/rc
%attr(754,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/rc.d/rc.local
%attr(754,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/rc.d/rc.modules
%attr(754,root,root) /etc/rc.d/rc.init
%attr(754,root,root) /etc/rc.d/rc.sysinit
%attr(754,root,root) /etc/rc.d/rc.shutdown
%attr(754,root,root) /etc/rc.d/rc?.d/S??allowlogin
%attr(754,root,root) /etc/rc.d/rc?.d/S??killall
%attr(754,root,root) /etc/rc.d/rc?.d/S??local
%attr(754,root,root) /etc/rc.d/rc?.d/S??network
%attr(754,root,root) /etc/rc.d/rc?.d/S??random
%attr(754,root,root) /etc/rc.d/rc?.d/S??single
%attr(754,root,root) /etc/rc.d/rc?.d/S??timezone
%attr(754,root,root) /etc/rc.d/rc?.d/K??allowlogin
%attr(754,root,root) /etc/rc.d/rc?.d/K??killall
%attr(754,root,root) /etc/rc.d/rc?.d/K??network
%attr(754,root,root) /etc/rc.d/rc?.d/K??random
%attr(754,root,root) /etc/rc.d/rc?.d/K??single

%attr(755,root,root) /etc/profile.d/lang.*sh

%attr(755,root,root) %{_bindir}/doexec
%attr(755,root,root) %{_bindir}/ipcalc
%attr(755,root,root) %{_bindir}/resolvesymlink
%attr(755,root,root) %{_bindir}/run-parts
%attr(755,root,root) %{_bindir}/usleep

%attr(755,root,root) %{_sbindir}/genhostid
%attr(755,root,root) %{_sbindir}/hwprofile
%attr(755,root,root) %{_sbindir}/service
%attr(755,root,root) %{_sbindir}/consoletype
%attr(755,root,root) %{_sbindir}/initlog
%attr(755,root,root) %{_sbindir}/loglevel
%attr(755,root,root) %{_sbindir}/ppp-watch
%attr(755,root,root) %{_sbindir}/netreport
%attr(755,root,root) %{_sbindir}/setsysfont
%attr(4755,root,root) %{_sbindir}/usernetctl

%attr(755,root,root) %{_sbindir}/if*
%attr(755,root,root) %{_sbindir}/tnl*

%attr(755,root,root) %{_sbindir}/getkey

%attr(755,root,root) %dir %{_sysconfdir}/ppp
%attr(754,root,root) %{_sysconfdir}/ppp/*
%attr(755,root,root) %dir /etc/sysconfig
%attr(755,root,root) %dir /etc/sysconfig/interfaces
%attr(755,root,root) %dir /etc/sysconfig/interfaces/data
%attr(755,root,root) %dir /etc/sysconfig/isapnp
%attr(755,root,root) %dir /etc/sysconfig/network-scripts
%attr(755,root,root) /etc/sysconfig/network-scripts/if*
/etc/sysconfig/network-scripts/functions.network
%dir /etc/sysconfig/interfaces/down.d
%dir /etc/sysconfig/interfaces/down.d/*
%dir /etc/sysconfig/interfaces/up.d
%dir /etc/sysconfig/interfaces/up.d/*
%attr(755,root,root) /etc/sysconfig/interfaces/down.d/ppp/logger
%attr(755,root,root) /etc/sysconfig/interfaces/up.d/ppp/logger
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/isapnp/isapnp-kernel.conf
%attr(640,root,root) %ghost /var/log/dmesg
%attr(750,root,root) %dir /var/run/netreport

%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/adjtime
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/inittab
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/modules
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/initlog.conf
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysctl.conf
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/clock
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/hwprof
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/i18n
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/network
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/static-arp
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/static-nat
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/static-routes
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/timezone
%config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/interfaces/ifcfg-eth0
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/system

%{_mandir}/man1/*

%dir %{localedir}
%lang(de) %{localedir}/de
%lang(pl) %{localedir}/pl
