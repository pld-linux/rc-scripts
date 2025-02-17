#
# TODO: move inittab file to SysVinit
#
# Conditional build:
%bcond_without	static		# link binaries with glib dynamically

Summary:	inittab and /etc/rc.d scripts
Summary(de.UTF-8):	inittab und /etc/rc.d Scripts
Summary(fr.UTF-8):	inittab et scripts /etc/rc.d
Summary(pl.UTF-8):	inittab i skrypty startowe z katalogu /etc/rc.d
Summary(tr.UTF-8):	inittab ve /etc/rc.d dosyaları
Name:		rc-scripts
Version:	0.4.20
Release:	4
License:	GPL v2
Group:		Base
#Source0:	ftp://distfiles.pld-linux.org/src/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	cde72affb846648781f8f8540a39037b
Source1:	rc-local.service
Source2:	sys-chroots.service
Source3:	%{name}.tmpfiles
Patch100:	git.patch
URL:		http://svn.pld-linux.org/trac/svn/wiki/packages/rc-scripts
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel
%{?with_static:BuildRequires:	glib2-static}
%{?with_static:BuildRequires:	glibc-static}
BuildRequires:	libcap-devel >= 1:2.17
BuildRequires:	linux-libc-headers >= 7:2.6.27
BuildRequires:	pkgconfig
BuildRequires:	pcre-devel
%{?with_static:BuildRequires:	pcre-static}
BuildRequires:	popt-devel
BuildRequires:	rpm >= 4.4.9-56
Requires(post):	fileutils
%ifarch sparc sparcv9 sparc64
Requires:	agetty
%endif
Requires:	/bin/awk
Requires:	/bin/basename
Requires:	/bin/gettext
Requires:	/bin/ipcalc
Requires:	/bin/nice
Requires:	/bin/ps
Requires:	SysVinit-tools >= 2.88-1
Requires:	blockdev
Requires:	coreutils
Requires:	ethtool
Requires:	run-parts = %{version}-%{release}
Requires:	virtual-init-daemon
%if "%{pld_release}" == "ac"
Requires:	filesystem >= 3.0-11
%else
Requires:	filesystem >= 4.0-1
%endif
Requires:	findutils
Requires:	fsck
Requires:	gettext
Requires:	grep
Requires:	hostname
Requires:	ipcalc >= 1.0.1-2
Requires:	iproute2
Requires:	iproute2-tc
Requires:	iputils-arping
Requires:	libutempter >= 1.1.6-2
Requires:	mktemp
Requires:	mount >= 2.12
Requires:	procps >= 1:3.2.6-1.1
Requires:	psmisc >= 22.5-2
Requires:	util-linux >= 2.22.1
Requires:	virtual(module-tools)
Suggests:	libcgroup
Obsoletes:	initscripts
Obsoletes:	vserver-rc-scripts
Conflicts:	LPRng < 3.8.0-2
Conflicts:	dev < 2.9.0-22
Conflicts:	iputils-arping < 2:s20070202-1
# character classes support required
Conflicts:	mawk < 1.3.4-0.20090727
Conflicts:	openssh-server < 2:3.6.1p2-6
Conflicts:	psacct < 6.3.5-10
Conflicts:	tzdata < 2007b-1.1
%if "%{pld_release}" == "th"
Conflicts:	udev-core < 1:135-2
%else
Conflicts:	udev-core < 1:124-3
%endif
Conflicts:	SysVinit < 2.88-16
Conflicts:	lvm2 < 2.02.83
Conflicts:	upstart
Conflicts:	wpa_supplicant < 0.6.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_exec_prefix	/
%define		localedir	/etc/sysconfig/locale
%define		_bindir		/bin
%define		_sbindir	/sbin

%description
This package contains the scripts used to boot a system, change run
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

%package -n run-parts
Summary:	Run scripts or programs in a directory
Summary(pl.UTF-8):	Uruchamianie skryptów lub programów z katalogu
Group:		Base
Conflicts:	rc-scripts < 0.4.14-2

%description -n run-parts
run-parts runs all the executable files named within specific
constraints, found in directory directory. Other files and directories
are silently ignored.

%description -n run-parts -l pl.UTF-8
Program run-parts pozwala na uruchamianie wszystkich plików zgodnych z
pewnymi ograniczeniami, obecnych w katalogu. Inne pliki i katalogi są
po cichu ignorowane.

%prep
%setup -q
%patch100 -p1

# hack, currently this results in errno@@GLIBC_PRIVATE symbol in ppp-watch:
#GLIB_LIBS="-Wl,-static `$PKG_CONFIG --libs --static glib-2.0` -Wl,-Bdynamic"
sed -i -e 's#^GLIB_LIBS=.*#GLIB_LIBS="%{_prefix}/%{_lib}/libglib-2.0.a -lrt -lpthread"#' configure.ac

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
install -d $RPM_BUILD_ROOT/var/{run/netreport,log} \
	$RPM_BUILD_ROOT/etc/sysconfig/{interfaces/data,hwprofiles} \
	$RPM_BUILD_ROOT{%{_sysconfdir},%{_prefix}/lib}/sysctl.d \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	%{!?with_static:ppp_watch_LDADD="$(pkg-config --libs glib-2.0)" ppp_watch_DEPENDENCIES=}

# deprecated shell version
%{__rm} $RPM_BUILD_ROOT%{_bindir}/run-parts.sh

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

# systemd
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdunitdir}/rc-local.service
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/local.service
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/sys-chroots.service
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

# packaged into SysVinit and systemd-init (supported options differ)
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man5/crypttab.5

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
[ -d /etc/sysconfig/network-scripts ] || exit 0
cd /etc/sysconfig/network-scripts
for iface in ifcfg-* ; do
	[ -f $iface ] || continue
	if [ -f /etc/sysconfig/interfaces/$iface ]; then
		echo "/etc/sysconfig/interfaces/$iface renamed to /etc/sysconfig/interfaces/$iface.rpmnew"
		mv -f /etc/sysconfig/interfaces/$iface{,.rpmnew}
	fi
	echo "/etc/sysconfig/network-scripts/$iface moved to /etc/sysconfig/interfaces/$iface"
	mv -f /etc/sysconfig/network-scripts/$iface /etc/sysconfig/interfaces
done

%files
%defattr(644,root,root,755)
%doc ChangeLog
%doc doc/*.txt doc/template.init
%doc sysconfig/interfaces/data/chat-ppp*
%doc sysconfig/interfaces/ifc*
%doc sysconfig/interfaces/tnl*
%doc sysconfig/init-colors*
%doc doc/sysvinitfiles

%dir /etc/rc.d
%dir /etc/rc.d/init.d
%dir /etc/rc.d/rc?.d
/etc/init.d
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
%attr(755,root,root) %{_bindir}/resolvesymlink
%attr(755,root,root) %{_bindir}/usleep

%attr(755,root,root) %{_sbindir}/consoletype
%attr(755,root,root) %{_sbindir}/genhostid
%attr(755,root,root) %{_sbindir}/getkey
%attr(755,root,root) %{_sbindir}/hwprofile
%attr(755,root,root) %{_sbindir}/ifdown
%attr(755,root,root) %{_sbindir}/ifup
%attr(755,root,root) %{_sbindir}/initlog
%attr(755,root,root) %{_sbindir}/loglevel
%attr(755,root,root) %{_sbindir}/minilogd
%attr(755,root,root) %{_sbindir}/netreport
%attr(755,root,root) %{_sbindir}/ppp-watch
%attr(755,root,root) %{_sbindir}/service
%attr(755,root,root) %{_sbindir}/setsysfont
%attr(755,root,root) %{_sbindir}/setuidgid
%attr(755,root,root) %{_sbindir}/start-stop-daemon
%attr(755,root,root) %{_sbindir}/tnldown
%attr(755,root,root) %{_sbindir}/tnlup
%attr(4755,root,root) %{_sbindir}/usernetctl

%attr(755,root,root) /lib/firmware/firmware-loader.sh

%{systemdtmpfilesdir}/rc-scripts.conf
%{systemdunitdir}/local.service
%{systemdunitdir}/rc-local.service
%{systemdunitdir}/sys-chroots.service

%dir /lib/rc-scripts
%attr(755,root,root) /lib/rc-scripts/ifdown-br
%attr(755,root,root) /lib/rc-scripts/ifdown-irda
%attr(755,root,root) /lib/rc-scripts/ifdown-post
%attr(755,root,root) /lib/rc-scripts/ifdown-ppp
%attr(755,root,root) /lib/rc-scripts/ifdown-sl
%attr(755,root,root) /lib/rc-scripts/ifdown-vlan
/lib/rc-scripts/ifup-aliases
%attr(755,root,root) /lib/rc-scripts/ifup-bond
%attr(755,root,root) /lib/rc-scripts/ifup-br
%attr(755,root,root) /lib/rc-scripts/ifup-ipx
%attr(755,root,root) /lib/rc-scripts/ifup-irda
%attr(755,root,root) /lib/rc-scripts/ifup-iucv
/lib/rc-scripts/ifup-neigh
%attr(755,root,root) /lib/rc-scripts/ifup-plip
%attr(755,root,root) /lib/rc-scripts/ifup-plusb
%attr(755,root,root) /lib/rc-scripts/ifup-post
%attr(755,root,root) /lib/rc-scripts/ifup-ppp
/lib/rc-scripts/ifup-routes
%attr(755,root,root) /lib/rc-scripts/ifup-sl
%attr(755,root,root) /lib/rc-scripts/ifup-vlan
%attr(755,root,root) /lib/rc-scripts/makepid
/lib/rc-scripts/functions.network
/lib/rc-scripts/functions

%dir %{_sysconfdir}/ppp
%attr(754,root,root) %{_sysconfdir}/ppp/auth-down
%attr(754,root,root) %{_sysconfdir}/ppp/auth-up
%attr(754,root,root) %{_sysconfdir}/ppp/ip-down
%attr(754,root,root) %{_sysconfdir}/ppp/ip-up
%attr(754,root,root) %{_sysconfdir}/ppp/ipv6-down
%attr(754,root,root) %{_sysconfdir}/ppp/ipv6-up
%attr(754,root,root) %{_sysconfdir}/ppp/ipx-down
%attr(754,root,root) %{_sysconfdir}/ppp/ipx-up
%dir /etc/sysconfig/cpusets
%dir /etc/sysconfig/hwprofiles
%dir /etc/sysconfig/interfaces
%dir /etc/sysconfig/interfaces/data
%dir /etc/sysconfig/isapnp

%dir /etc/sysconfig/interfaces/down.d
%dir /etc/sysconfig/interfaces/down.d/ppp
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/interfaces/down.d/ppp/logger
%dir /etc/sysconfig/interfaces/up.d
%dir /etc/sysconfig/interfaces/up.d/ppp
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

%dir %{_sysconfdir}/sysctl.d
%dir %{_prefix}/lib/sysctl.d

%{_mandir}/man1/consoletype.1*
%{_mandir}/man1/doexec.1*
%{_mandir}/man1/genhostid.1*
%{_mandir}/man1/getkey.1*
%{_mandir}/man1/initlog.1*
%{_mandir}/man1/netreport.1*
%{_mandir}/man1/usleep.1*
%{_mandir}/man8/ppp-watch.8*
%{_mandir}/man8/start-stop-daemon.8*
%{_mandir}/man8/usernetctl.8*
%lang(de) %{_mandir}/de/man?/*
%lang(es) %{_mandir}/es/man?/*
%lang(fr) %{_mandir}/fr/man?/*
%lang(ja) %{_mandir}/ja/man?/*
%lang(ru) %{_mandir}/ru/man?/*
%lang(sv) %{_mandir}/sv/man?/*

%dir %{localedir}
%lang(de) %{localedir}/de
%lang(pl) %{localedir}/pl

%files -n run-parts
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/run-parts
%{_mandir}/man8/run-parts.8*
