Summary:	inittab and /etc/rc.d scripts
Name:		rc-scripts
Version:	3.66.7
Copyright:	GPL
Group:		Base
Group(pl):	Bazowe	
Release:	2d
Source:		%{name}-%{version}.tar.bz2
Buildroot:	/tmp/buildroot-%{name}-%{version}
Requires:	mingetty
Requires:	mktemp
Requires:	bash >= 2.02.1
Requires:	modutils >= 2.1.121
Prereq:		/sbin/chkconfig
Obsoletes:	initscripts
Summary(de):	inittab und /etc/rc.d Scripts
Summary(fr):	inittab et scripts /etc/rc.d
Summary(pl):	inittab i skrypty startowe z katalogu /etc/rc.d
Summary(tr):	inittab ve /etc/rc.d dosyalarý

%description
This package contains the scripts use to boot a system, change run
levels, and shut the system down cleanly. It also contains the scripts
that activate and deactivate most network interfaces.

%description -l de
Dieses Paket enthält die Scripts, die zum Hochfahren des Systems, Ändern
der Betriebsebene und sauberem Herunterfahren des Systems erforderlich sind.
Außerdem enthält es die Scripts, die Netzwerkschnittstellen aktivieren und
deaktivieren.

%description -l fr
Ce package contient les scripts utilisés pour démarrer le systéme,
changer les niveaux d'exécution, et arréter le systéme proprement.
Il contient aussi les scripts qui activent et désactivent la plupart
des inetrfaces réseau.

%description -l pl
Pakiet zawiera skrypty uruchamiane przy starcie i zamykaniu systemu, a
tak¿e przy zmianie poziomu uruchomienia. 

%description -l tr
Bu paket, sistem açmak, çalýþma düzeylerini deðiþtirmek ve sistemi düzgün bir
þekilde kapatmak için gereken dosyalarý içerir. Ayrýca pek çok bilgisayar aðý
arayüzlerini etkinleþtiren ya da edilginleþtiren programcýklar içerir.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -w" make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc,/var/{log,run/netreport}}

make ROOT=$RPM_BUILD_ROOT install 

install -d $RPM_BUILD_ROOT/etc/rc.d/rc{0,1,2,3,4,5,6}.d

ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc0.d/K80random
ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc1.d/S20random
ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc2.d/S20random
ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc3.d/S20random
ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc4.d/S20random
ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc5.d/S20random
ln -s ../init.d/random $RPM_BUILD_ROOT/etc/rc.d/rc6.d/K80random

ln -s ../init.d/nfsfs $RPM_BUILD_ROOT/etc/rc.d/rc0.d/K95nfsfs
ln -s ../init.d/nfsfs $RPM_BUILD_ROOT/etc/rc.d/rc1.d/K95nfsfs
ln -s ../init.d/nfsfs $RPM_BUILD_ROOT/etc/rc.d/rc2.d/K95nfsfs
ln -s ../init.d/nfsfs $RPM_BUILD_ROOT/etc/rc.d/rc3.d/S15nfsfs
ln -s ../init.d/nfsfs $RPM_BUILD_ROOT/etc/rc.d/rc4.d/S15nfsfs
ln -s ../init.d/nfsfs $RPM_BUILD_ROOT/etc/rc.d/rc5.d/S15nfsfs
ln -s ../init.d/nfsfs $RPM_BUILD_ROOT/etc/rc.d/rc6.d/K95nfsfs

ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc0.d/K97network
ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc1.d/K97network
ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc2.d/S10network
ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc3.d/S10network
ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc4.d/S10network
ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc5.d/S10network
ln -s ../init.d/network $RPM_BUILD_ROOT/etc/rc.d/rc6.d/K97network

ln -s ../init.d/killall $RPM_BUILD_ROOT/etc/rc.d/rc0.d/K90killall
ln -s ../init.d/killall $RPM_BUILD_ROOT/etc/rc.d/rc6.d/K90killall

ln -s ../init.d/halt $RPM_BUILD_ROOT/etc/rc.d/rc0.d/S00halt
ln -s ../init.d/halt $RPM_BUILD_ROOT/etc/rc.d/rc6.d/S00reboot

ln -s ../init.d/single $RPM_BUILD_ROOT/etc/rc.d/rc1.d/S00single

ln -s ../rc.local $RPM_BUILD_ROOT/etc/rc.d/rc2.d/S99local
ln -s ../rc.local $RPM_BUILD_ROOT/etc/rc.d/rc3.d/S99local
ln -s ../rc.local $RPM_BUILD_ROOT/etc/rc.d/rc5.d/S99local

touch $RPM_BUILD_ROOT/etc/sysconfig/{mouse,network,clock,tape,amd}

bzip2 -9 $RPM_BUILD_ROOT/usr/man/man1/*.1
bzip2 -9 sysconfig.txt *.init

%post
/sbin/chkconfig --add random 
/sbin/chkconfig --add nfsfs 
/sbin/chkconfig --add network 

%preun
if [ $1 = 0 ]; then
  /sbin/chkconfig --del random
  /sbin/chkconfig --del nfsfs
  /sbin/chkconfig --del network
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc sysconfig.txt.bz2 *.init.bz2

%config(noreplace) %verify(not md5 mtime size) /etc/adjtime
%config(noreplace) %verify(not md5 mtime size) /etc/inittab

%attr(640,root,root) %config(noreplace) %verify(not size mtime md5)  /etc/sysconfig/network-ip6
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5)  /etc/sysconfig/network-ip6.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5)  /etc/sysconfig/mouse
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5)  /etc/sysconfig/network
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5)  /etc/sysconfig/clock
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5)  /etc/sysconfig/tape
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5)  /etc/sysconfig/amd

%attr(750,root,root) %dir /etc/sysconfig/network-scripts
%attr(640,root,root) %config /etc/sysconfig/network-scripts/ifcfg-lo
%attr(640,root,root) %config /etc/sysconfig/network-scripts/*-ppp0
%attr(640,root,root) %config /etc/sysconfig/network-scripts/network-*
%attr(750,root,root) %config /etc/sysconfig/network-scripts/ifd*
%attr(750,root,root) %config /etc/sysconfig/network-scripts/ifup
%attr(750,root,root) %config /etc/sysconfig/network-scripts/ifup-*

%attr(700,root,root) /etc/rc.d/init.d/*
%attr(700,root,root) %config(missingok) /etc/rc.d/rc[0123456].d/*

%attr(750,root,root) %config /etc/rc.d/rc.sysinit
%attr(750,root,root) %config /etc/rc.d/rc.serial
%attr(750,root,root) %config /etc/rc.d/rc
%attr(700,root,root) %config(noreplace) %verify(not size mtime md5) /etc/rc.d/rc.local
%attr(755,root,root) %config /etc/profile.d/lang.sh
%attr(750,root,root) /sbin/*
%attr(755,root,root) /bin/*
%attr(755,root,root) /usr/sbin/usernetctl

%attr(750,root,root) %dir /var/run/netreport
%attr(750,root,root) %config /etc/ppp/*

%attr(644,root, man) /usr/man/man1/*

%changelog
* Thu Jan 21 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [3.66.7-2d]
- removed /var/log/wtmp -- provides by sysklogd,
- fixed owner && group of scripts.

* Mon Jan 18 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [3.66.7-1d]
- new release 3.66.7,
  (new ppp-scripts written by Grzegorz Stanis³awski <stangrze@open.net.pl>
- compressed %doc.  

* Tue Jan 05 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [3.66.6-1d]
- new /etc/rc.d/init.d/nfsfs file (can handle knfsd)

* Wed Dec 30 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [3.66.5-2d]
- fixed ifdown-ppp. 
- removed %dir /etc/rc.d/init.d -- provides by chkconfig.

* Mon Dec 28 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [3.66.5-1d]
- changes in rc.serial

* Fri Dec 25 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [3.66.4-1d]
- corrected setting PnP devices
- added /etc/rc.d/rc.serial
- modified setsysfont to work with consoletools

* Wed Dec 23 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [3.66.3-1d]
- added removing zmailer pid files
- added ip-up.local and ip-down.local
- /sbin/modrpobe instead only modprobe in rc.sysinit

* Thu Dec 17 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [3.66.2-1d]
- added ipv6 module chcecking
- renamed to rc-scripts and added obsoletes: initscripts

* Mon Dec 07 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [3.66.1-1d]
- fixed ifup & ifdown scripts,
- fixed functions-ip6,
- moved radvd.init & tunnel-ipv6.init to %doc,
- added commpresed man pages (bzip2),
- other -- minor changes.

* Sun Oct 18 1998 Marcin Korzonek <mkorz@shadow.eu.org>
- /etc/rc.d and /etc/rc.d/rc{0,1,2,3,4,5,6} directories 
  now belongs to chkconfig package,
- simplification in %%install,
- translations modified for pl,
- defined files permission according to PLD-devel rules.

* Fri Jun 12 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
 [3.66-5]
- updated to 3.66
- added IPv6 support (Copyriht by P. Bieringer)

* Tue Jun 02 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr


* Mon Jun 01 1998 Erik Troan <ewt@redhat.com>
- ipcalc should *never* have been setgid anything
- depmod isn't run properly for non-serial numbered kernels

* Wed May 06 1998 Donnie Barnes <djb@redhat.com>

- added system font and language setting

* Mon May 04 1998 Michael K. Johnson <johnsonm@redhat.com>

- Added missing files to packagelist.

* Sat May 02 1998 Michael K. Johnson <johnsonm@redhat.com>

- Added lots of linuxconf support.  Should still work on systems that
  do not have linuxconf installed, but linuxconf gives enhanced support.
- In concert with linuxconf, added IPX support.  Updated docs to reflect it.

* Fri May 01 1998 Erik Troan <ewt@redhat.com>

- rc.sysinit uses preferred directory

* Sun Apr 05 1998 Erik Troan <ewt@redhat.com>

- updated rc.sysinit to deal with kernel versions with release numbers

* Sun Mar 22 1998 Erik Troan <ewt@redhat.com>

- use ipcalc to calculate the netmask if one isn't specified

* Tue Mar 10 1998 Erik Troan <ewt@redhat.com>

- added and made use of ipcalc

* Tue Mar 10 1998 Erik Troan <ewt@redhat.com>

- removed unnecessary dhcp log from /tmp

* Mon Mar 09 1998 Erik Troan <ewt@redhat.com>

- if bootpc fails, take down the device

* Mon Mar 09 1998 Erik Troan <ewt@redhat.com>

- added check for mktemp failure

* Thu Feb 05 1998 Erik Troan <ewt@redhat.com>

- fixed support for user manageable cloned devices

* Mon Jan 12 1998 Michael K. Johnson <johnsonm@redhat.com>

- /sbin/ isn't always in $PATH, so call /sbin/route in ifup-routes

* Wed Dec 31 1997 Erik Troan <ewt@redhat.com>

- touch /var/lock/subsys/kerneld after cleaning out /var/lock/subsys
- the logic for when  /var/lock/subsys/kerneld is touched was backwards

* Tue Dec 30 1997 Erik Troan <ewt@redhat.com>

- tried to get /proc stuff right one more time (uses -t nonfs,proc now)
- added support for /fsckoptions
- changed 'yse' to 'yes' in KERNELD= line

* Tue Dec 09 1997 Erik Troan <ewt@redhat.com>

- set domainname to "" if none is specified in /etc/sysconfig/network
- fix /proc mounting to get it in /etc/mtab

* Mon Dec 08 1997 Michael K. Johnson <johnsonm@redhat.com>

- fixed inheritance for clone devices

* Fri Nov 07 1997 Erik Troan <ewt@redhat.com>

- added sound support to rc.sysinit

* Fri Nov 07 1997 Michael K. Johnson <johnsonm@redhat.com>

- Added missing "then" clause

* Thu Nov 06 1997 Michael K. Johnson <johnsonm@redhat.com>

- Fixed DEBUG option in ifup-ppp
- Fixed PPP persistance
- Only change IP forwarding if necessary

* Tue Oct 28 1997 Donnie Barnes <djb@redhat.com>

- removed the skeleton init script
- added the ability to 'nice' daemons

* Tue Oct 28 1997 Erik Troan <ewt@redhat.com>

- touch /var/lock/subsys/kerneld if it's running, and after mounting /var
- applied dhcp fix

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>

- added status|restart to init scripts

* Thu Oct 23 1997 Michael K. Johnson <johnsonm@redhat.com>

- touch random seed file before chmod'ing it.

* Wed Oct 15 1997 Erik Troan <ewt@redhat.com>

- run domainname if NISDOMAIN is set 

* Wed Oct 15 1997 Michael K. Johnson <johnsonm@redhat.com>

- Make the random seed file mode 600.

* Tue Oct 14 1997 Michael K. Johnson <johnsonm@redhat.com>

- bring down ppp devices if ifdown-ppp is called while ifup-ppp is sleeping.

* Mon Oct 13 1997 Erik Troan <ewt@redhat.com>

- moved to new chkconfig conventions

* Sat Oct 11 1997 Erik Troan <ewt@redhat.com>

- fixed rc.sysinit for hwclock compatibility

* Thu Oct 09 1997 Erik Troan <ewt@redhat.com>

- run 'ulimit -c 0' before running scripts in daemon function

* Wed Oct 08 1997 Donnie Barnes <djb@redhat.com>

- added chkconfig support
- made all rc*.d symlinks have missingok flag

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>

- fixed network-scripts to allow full pathnames as config files
- removed some old 3.0.3 pcmcia device handling

* Wed Oct 01 1997 Michael K. Johnson <johnsonm@redhat.com>

- /var/run/netreport needs to be group-writable now that /sbin/netreport
  is setguid instead of setuid.

* Tue Sep 30 1997 Michael K. Johnson <johnsonm@redhat.com>

- Added network-functions to spec file.
- Added report functionality to usernetctl.
- Fixed bugs I introduced into usernetctl while adding clone device support.
- Clean up entire RPM_BUILD_ROOT directory in %clean.

* Mon Sep 29 1997 Michael K. Johnson <johnsonm@redhat.com>

- Clone device support in network scripts, rc scripts, and usernetctl.
- Disassociate from controlling tty in PPP and SLIP startup scripts,
  since they act as daemons.
- Spec file now provides start/stop symlinks, since they don't fit in
  the CVS archive.

* Tue Sep 23 1997 Donnie Barnes <djb@redhat.com>

- added mktemp support to ifup

* Thu Sep 18 1997 Donnie Barnes <djb@redhat.com>

- fixed some init.d/functions bugs for stopping httpd

* Tue Sep 16 1997 Donnie Barnes <djb@redhat.com>

- reworked status() to adjust for processes that change their argv[0] in
  the process table.  The process must still have it's "name" in the argv[0]
  string (ala sendmail: blah blah).

* Mon Sep 15 1997 Erik Troan <ewt@redhat.com>

- fixed bug in FORWARD_IPV4 support

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>

- added support for FORWARD_IPV4 variable

* Thu Sep 11 1997 Donald Barnes <djb@redhat.com>

- added status function to functions along with better killproc 
  handling.
- added /sbin/usleep binary (written by me) and man page
- changed BuildRoot to /var/tmp instead of /tmp

* Tue Jun 10 1997 Michael K. Johnson <johnsonm@redhat.com>

- /sbin/netreport sgid rather than suid.
- /var/run/netreport writable by group root.

- /etc/ppp/ip-{up|down} no longer exec their local versions, so
  now ifup-post and ifdown-post will be called even if ip-up.local
  and ip-down.local exist.

* Tue Jun 03 1997 Michael K. Johnson <johnsonm@redhat.com>

- Added missing -f to [ invocation in ksyms check.

* Fri May 23 1997 Michael K. Johnson <johnsonm@redhat.com>

- Support for net event notification:
  Call /sbin/netreport to request that SIGIO be sent to you whenever
  a network interface changes status (won't work for brining up SLIP
  devices).
  Call /sbin/netreport -r to remove the notification request.
- Added ifdown-post, and made all the ifdown scrips call it, and
  added /etc/ppp/ip-down script that calls /etc/ppp/ip-down.local
  if it exists, then calls ifdown-post.
- Moved ifup and ifdown to /sbin

* Tue Apr 15 1997 Michael K. Johnson <johnsonm@redhat.com>

- usernetctl put back in ifdown
- support for slaved interfaces

* Wed Apr 02 1997 Erik Troan <ewt@redhat.com>

- Created ifup-post from old ifup
- PPP, PLIP, and generic ifup use ifup-post

* Fri Mar 28 1997 Erik Troan <ewt@redhat.com>

- Added DHCP support
- Set hostname via reverse name lookup after configuring a networking
  device if the current hostname is (none) or localhost

* Tue Mar 18 1997 Erik Troan <ewt@redhat.com>

- Got rid of xargs dependency in halt script
- Don't mount /proc twice (unmount it in between)
- sulogin and filesystem unmounting only happened for a corrupt root 
  filesystem -- it now happens when other filesystems are corrupt as well

* Tue Mar 04 1997 Michael K. Johnson <johnsonm@redhat.com>

PPP fixes and additions

* Mon Mar 03 1997 Erik Troan <ewt@redhat.com>

Mount proc before trying to start kerneld so we can test for /proc/ksyms
properly.

* Wed Feb 26 1997 Michael K. Johnson <johnsonm@redhat.com>

Added MTU for PPP.

Put PPPOPTIONS at the end of the options string instead of at the
beginning so that they override other options.  Gives users more rope...

Don't do module-based stuff on non-module systems.  Ignore errors if
st module isn't there and we try to load it.

* Tue Feb 25 1997 Michael K. Johnson <johnsonm@redhat.com>

Changed ifup-ppp and ifdown-ppp not to use doexec, because the argv[0]
provided by doexec goes away when pppd gets swapped out.

ifup-ppp now sets remotename to the logical name of the device.
This will BREAK current PAP setups on netcfg-managed interfaces,
but we needed to do this to add a reasonable interface-specific
PAP editor to netcfg.

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>

1) Added usernetctl wrapper for user mode ifup and ifdown's and man page
2) Rewrote ppp and slip kill and retry code 
3) Added doexec and man page
