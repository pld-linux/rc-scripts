#
# Conditional build:
%bcond_without	static		# link binaries with glib dynamically

Summary:	inittab and /etc/rc.d scripts
Summary(de.UTF-8):	inittab und /etc/rc.d Scripts
Summary(fr.UTF-8):	inittab et scripts /etc/rc.d
Summary(pl.UTF-8):	inittab i skrypty startowe z katalogu /etc/rc.d
Summary(tr.UTF-8):	inittab ve /etc/rc.d dosyaları
Name:		rc-scripts
Version:	0.4.4.1
Release:	7
License:	GPL v2
Group:		Base
Source0:	ftp://distfiles.pld-linux.org/src/%{name}-%{version}.tar.gz
# Source0-md5:	ff522ac3a98dc6c8c0c891f91a164ec2
Patch0:		%{name}-routes6.patch
URL:		http://svn.pld-linux.org/cgi-bin/viewsvn/rc-scripts/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
%{?with_static:BuildRequires:	glib2-static}
%{?with_static:BuildRequires:	glibc-static}
BuildRequires:	libcap-devel >= 1:2.17
BuildRequires:	linux-libc-headers >= 7:2.6.27
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	rpm >= 4.4.9-56
Requires(post):	fileutils
%ifarch sparc sparcv9 sparc64
Requires:	agetty
%endif
Requires:	/bin/awk
Requires:	/bin/basename
Requires:	/bin/gettext
Requires:	/bin/nice
Requires:	/bin/ps
Requires:	SysVinit
Requires:	blockdev
Requires:	coreutils
Requires:	ethtool
%if "%{pld_release}" == "ac"
Requires:	filesystem >= 3.0-11
%else
Requires:	filesystem >= 3.0-35
%endif
Requires:	findutils
Requires:	fsck
Requires:	gettext
Requires:	grep
Requires:	hostname
Requires:	iproute2
Requires:	iputils-arping
Requires:	mingetty
Requires:	mktemp
Requires:	module-init-tools
Requires:	mount >= 2.12
Requires:	procps >= 1:3.2.6-1.1
Requires:	psmisc >= 22.5-2
Requires:	utempter
Requires:	util-linux
Suggests:	libcgroup
Provides:	initscripts
Obsoletes:	initscripts
Obsoletes:	vserver-rc-scripts
Conflicts:	LPRng < 3.8.0-2
Conflicts:	dev < 2.9.0-22
Conflicts:	iputils-arping < 2:s20070202-1
Conflicts:	openssh-server < 2:3.6.1p2-6
Conflicts:	psacct < 6.3.5-10
Conflicts:	tzdata < 2007b-1.1
%if "%{pld_release}" == "th"
Conflicts:	udev-core < 1:135-2
%else
Conflicts:	udev-core < 1:124-3
%endif
Conflicts:	upstart-SysVinit < 2.86-25
Conflicts:	wpa_supplicant < 0.6.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define		localedir	/etc/sysconfig/locale
%define 	_bindir		/bin
%define		_sbindir	/sbin

%description
This package contains the scripts use to boot a system, change run
levels, and shut the system down cleanly.

%description -l de.UTF-8
Dieses Paket enthält die Scripts, die zum Hochfahren des Systems,
Ändern der Betriebsebene und sauberem Herunterfahren des Systems
erforderlich sind. Außerdem enthält es die Scripts, die
Netzwerkschnittstellen aktivieren und deaktivieren.

%description -l fr.UTF-8
Ce package contient les scripts utilisés pour démarrer le systéme,
changer les niveaux d'exécution, et arréter le systéme proprement. Il
contient aussi les scripts qui activent et désactivent la plupart des
inetrfaces réseau.

%description -l pl.UTF-8
Pakiet zawiera skrypty uruchamiane przy starcie i zamykaniu systemu, a
także przy zmianie jego poziomu pracy.

%description -l tr.UTF-8
Bu paket, sistem açmak, çalışma düzeylerini değiştirmek ve sistemi
düzgün bir şekilde kapatmak için gereken dosyaları içerir. Ayrıca pek
çok bilgisayar ağı arayüzlerini etkinleştiren ya da edilginleştiren
programcıklar içerir.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--with-localedir=%{localedir}
%{__make} \
	%{!?with_static:ppp_watch_LDADD="$(pkg-config --libs glib-2.0)" ppp_watch_DEPENDENCIES=}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/{run/netreport,log}
install -d $RPM_BUILD_ROOT/etc/sysconfig/hwprofiles

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	%{!?with_static:ppp_watch_LDADD="$(pkg-config --libs glib-2.0)" ppp_watch_DEPENDENCIES=}

for i in 0 1 2 3 4 5 6; do
	install -d $RPM_BUILD_ROOT/etc/rc.d/rc$i.d
done

for i in 2 3 4 5; do
	ln -s ../init.d/local $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S99local
	ln -s ../init.d/netfs $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S25netfs
	ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S10network
	ln -s ../init.d/allowlogin $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S99allowlogin
	ln -s ../init.d/sys-chroots $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S99sys-chroots
done

for i in 1 2 3 4 5; do
	ln -s ../init.d/killall $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S00killall
	ln -s ../init.d/cpusets $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S01cpusets
	ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/S20random
done

for i in 0 2 3 4 5 6; do
	ln -s ../init.d/single $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K00single
done

ln -s ../init.d/single $RPM_BUILD_ROOT/etc/rc.d/rc1.d/S00single

for i in 0 6; do
	ln -s ../init.d/cpusets $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K99cpusets
	ln -s ../init.d/killall $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K90killall
	ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K80random
done

for i in 0 1 6; do
	ln -s ../init.d/netfs $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K75netfs
	ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K90network
	ln -s ../init.d/allowlogin $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K01allowlogin
	ln -s ../init.d/sys-chroots $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K01sys-chroots
	ln -s ../init.d/local $RPM_BUILD_ROOT/etc/rc.d/rc$i.d/K01local
done

> $RPM_BUILD_ROOT/var/log/dmesg

# make /etc/init.d symlink relative
ln -nfs rc.d/init.d $RPM_BUILD_ROOT/etc/init.d

%if "%{pld_release}" == "ac"
rm -rf $RPM_BUILD_ROOT/etc/init
%endif

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
chown root:root /var/log/dmesg
chmod 640 /var/log/dmesg
touch /var/cache/rc-scripts/msg.cache
chmod 644 /var/cache/rc-scripts/msg.cache
chown root:root /var/cache/rc-scripts/msg.cache

# move network interfaces description files to new location
%triggerpostun -- initscripts
mv -f /etc/sysconfig/network-scripts/ifcfg-* /etc/sysconfig/interfaces

%files
%defattr(644,root,root,755)
%doc ChangeLog
%doc doc/*.txt rc.d/init.d/template.init
%doc sysconfig/interfaces/data/chat-ppp*
%doc sysconfig/interfaces/ifc*
%doc sysconfig/interfaces/tnl*
%doc sysconfig/init-colors*
%doc doc/sysvinitfiles

%dir /etc/rc.d
%dir /etc/rc.d/init.d
%dir /etc/rc.d/rc?.d
/etc/init.d

%if "%{pld_release}" != "ac"
%config(noreplace) %verify(not md5 mtime size) /etc/init/random.conf
%config(noreplace) %verify(not md5 mtime size) /etc/init/rc.conf
%config(noreplace) %verify(not md5 mtime size) /etc/init/rcS-sulogin.conf
%config(noreplace) %verify(not md5 mtime size) /etc/init/rcS.conf
%endif

/etc/rc.d/init.d/functions
%attr(754,root,root) /etc/rc.d/init.d/allowlogin
%attr(754,root,root) /etc/rc.d/init.d/cpusets
%attr(754,root,root) /etc/rc.d/init.d/cryptsetup
%attr(754,root,root) /etc/rc.d/init.d/killall
%attr(754,root,root) /etc/rc.d/init.d/local
%attr(754,root,root) /etc/rc.d/init.d/netfs
%attr(754,root,root) /etc/rc.d/init.d/network
%attr(754,root,root) /etc/rc.d/init.d/random
%attr(754,root,root) /etc/rc.d/init.d/single
%attr(754,root,root) /etc/rc.d/init.d/sys-chroots

%attr(754,root,root) /etc/rc.d/rc
%config(noreplace) %verify(not md5 mtime size) /etc/rc.d/rc.local
%attr(754,root,root) /etc/rc.d/rc.init
%attr(754,root,root) /etc/rc.d/rc.sysinit
%attr(754,root,root) /etc/rc.d/rc.shutdown
%attr(754,root,root) /etc/rc.d/rc?.d/K??allowlogin
%attr(754,root,root) /etc/rc.d/rc?.d/K??cpusets
%attr(754,root,root) /etc/rc.d/rc?.d/K??killall
%attr(754,root,root) /etc/rc.d/rc?.d/K??local
%attr(754,root,root) /etc/rc.d/rc?.d/K??netfs
%attr(754,root,root) /etc/rc.d/rc?.d/K??network
%attr(754,root,root) /etc/rc.d/rc?.d/K??random
%attr(754,root,root) /etc/rc.d/rc?.d/K??single
%attr(754,root,root) /etc/rc.d/rc?.d/K??sys-chroots
%attr(754,root,root) /etc/rc.d/rc?.d/S??allowlogin
%attr(754,root,root) /etc/rc.d/rc?.d/S??cpusets
%attr(754,root,root) /etc/rc.d/rc?.d/S??killall
%attr(754,root,root) /etc/rc.d/rc?.d/S??local
%attr(754,root,root) /etc/rc.d/rc?.d/S??netfs
%attr(754,root,root) /etc/rc.d/rc?.d/S??network
%attr(754,root,root) /etc/rc.d/rc?.d/S??random
%attr(754,root,root) /etc/rc.d/rc?.d/S??single
%attr(754,root,root) /etc/rc.d/rc?.d/S??sys-chroots

%dir /var/cache/rc-scripts
%ghost /var/cache/rc-scripts/msg.cache

%attr(755,root,root) /etc/profile.d/lang.*sh

%attr(755,root,root) %{_bindir}/doexec
%attr(755,root,root) %{_bindir}/ipcalc
%attr(755,root,root) %{_bindir}/resolvesymlink
%attr(755,root,root) %{_bindir}/run-parts
%attr(755,root,root) %{_bindir}/usleep

%attr(755,root,root) %{_sbindir}/consoletype
%attr(755,root,root) %{_sbindir}/fstab-decode
%attr(755,root,root) %{_sbindir}/genhostid
%attr(755,root,root) %{_sbindir}/getkey
%attr(755,root,root) %{_sbindir}/hwprofile
%attr(755,root,root) %{_sbindir}/if*
%attr(755,root,root) %{_sbindir}/initlog
%attr(755,root,root) %{_sbindir}/loglevel
%attr(755,root,root) %{_sbindir}/minilogd
%attr(755,root,root) %{_sbindir}/netreport
%attr(755,root,root) %{_sbindir}/ppp-watch
%attr(755,root,root) %{_sbindir}/service
%attr(755,root,root) %{_sbindir}/setsysfont
%attr(755,root,root) %{_sbindir}/setuidgid
%attr(755,root,root) %{_sbindir}/start-stop-daemon
%attr(755,root,root) %{_sbindir}/tnl*
%attr(4755,root,root) %{_sbindir}/usernetctl
%attr(755,root,root) /lib/firmware/firmware-loader.sh

%dir %{_sysconfdir}/ppp
%attr(754,root,root) %{_sysconfdir}/ppp/*
%dir /etc/sysconfig/cpusets
%dir /etc/sysconfig/hwprofiles
%dir /etc/sysconfig/interfaces
%dir /etc/sysconfig/interfaces/data
%dir /etc/sysconfig/isapnp

%dir /etc/sysconfig/network-scripts
%attr(755,root,root) /etc/sysconfig/network-scripts/ifdown-br
%attr(755,root,root) /etc/sysconfig/network-scripts/ifdown-irda
%attr(755,root,root) /etc/sysconfig/network-scripts/ifdown-post
%attr(755,root,root) /etc/sysconfig/network-scripts/ifdown-ppp
%attr(755,root,root) /etc/sysconfig/network-scripts/ifdown-sl
%attr(755,root,root) /etc/sysconfig/network-scripts/ifdown-vlan
/etc/sysconfig/network-scripts/ifup-aliases
%attr(755,root,root) /etc/sysconfig/network-scripts/ifup-br
%attr(755,root,root) /etc/sysconfig/network-scripts/ifup-ipx
%attr(755,root,root) /etc/sysconfig/network-scripts/ifup-irda
%attr(755,root,root) /etc/sysconfig/network-scripts/ifup-iucv
/etc/sysconfig/network-scripts/ifup-neigh
%attr(755,root,root) /etc/sysconfig/network-scripts/ifup-plip
%attr(755,root,root) /etc/sysconfig/network-scripts/ifup-plusb
%attr(755,root,root) /etc/sysconfig/network-scripts/ifup-post
%attr(755,root,root) /etc/sysconfig/network-scripts/ifup-ppp
/etc/sysconfig/network-scripts/ifup-routes
%attr(755,root,root) /etc/sysconfig/network-scripts/ifup-sl
%attr(755,root,root) /etc/sysconfig/network-scripts/ifup-vlan

/etc/sysconfig/network-scripts/functions.network
%dir /etc/sysconfig/interfaces/down.d
%dir /etc/sysconfig/interfaces/down.d/*
%dir /etc/sysconfig/interfaces/up.d
%dir /etc/sysconfig/interfaces/up.d/*
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/interfaces/down.d/ppp/logger
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/interfaces/up.d/ppp/logger
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/isapnp/isapnp-kernel.conf
%attr(640,root,root) %ghost /var/log/dmesg
%attr(750,root,root) %dir /var/run/netreport

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adjtime
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/crypttab
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/initlog.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/inittab
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysctl.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/cpusets/cpuset-test
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/hwprof
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/i18n
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/init-colors
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/interfaces/ifcfg-eth0
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/network
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/static-arp
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/static-nat
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/static-routes
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/static-routes6
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/system

%{_mandir}/man?/*
%lang(de) %{_mandir}/de/man?/*
%lang(es) %{_mandir}/es/man?/*
%lang(fr) %{_mandir}/fr/man?/*
%lang(ja) %{_mandir}/ja/man?/*
%lang(ru) %{_mandir}/ru/man?/*
%lang(sv) %{_mandir}/sv/man?/*

%dir %{localedir}
%lang(de) %{localedir}/de
%lang(pl) %{localedir}/pl
