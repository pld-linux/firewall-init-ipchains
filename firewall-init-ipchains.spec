Summary:	Firewall SysV-init style start-up script
Name:		firewall-init
Version:	2.0
Release:	1
Copyright:	BSD
Group:		Networking/Admin
Source:		ftp://hunter.mimuw.edu.pl/pub/users/baggins/%{name}-%{version}.tar.gz
Prereq:		/sbin/chkconfig
Requires:	ipchains
Buildarch:	noarch
Buildroot:	/tmp/%{name}-%{version}-root

%description
Firewall-init is meant to provide an easy to use interface to start and
stopping the kernel IP packet filters and accounting through ipchains(8).

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{sysconfig/firewall-rules,rc.d/init.d}

install firewall.init $RPM_BUILD_ROOT/etc/rc.d/init.d/firewall
install firewall $RPM_BUILD_ROOT/etc/sysconfig/

for i in input output forward; do
	echo '#<policy> <proto> <s_addr/s_mask> <s_port> <d_addr/d_mask> <d_port> <interface> <options>' > \
		$RPM_BUILD_ROOT/etc/sysconfig/firewall-rules/${i}
done

%post
/sbin/chkconfig --add firewall

%postun
if [ $1 = 0 ]; then
   /sbin/chkconfig --del firewall
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%doc README input.example
%attr(600, root, root) %verify(not size mtime md5) %config(noreplace) /etc/sysconfig/firewall
%attr(600, root, root) %verify(not size mtime md5) %config(noreplace) /etc/sysconfig/firewall-rules/*
%attr(700, root, root) %dir /etc/sysconfig/firewall-rules
%attr(700, root, root) /etc/rc.d/init.d/firewall

%changelog
* Tue Jul 06 1999 Jan Rêkorajski <baggins@pld.org.pl>
  [2.0-1]
- converted to ipchains
- new source URL

* Thu Oct 29 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.2-6]
- added support for chconfig (firewall-chconfig.patch and %post{un}
  sections).

* Wed Jul 15 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.2-5]
- added status and extstatus functionality to init script.

* Thu Jul  9 1998 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.2-4]
- added -q %setup parameter,
- added using %%{name}, %%{version} macros in Buildroot and Source,
- spec file rewritten for using Buildroot,
- added %clean section,
- removed Packager field from spec (if you want recompile package and
  redistribute this package later put this in your private .rpmrc). 
- replaced "mkdir -p" with "install -d" in %install,
- added %defattr and %attr macros in %files (allows building package from
  non-root account),
- changed permission for config files with firewall rules to 700,
- added %verify(not size mtime md5) for config files with firewall rules,
- added Summary field,
- changed build architecture to noarch,
- added restart and probe10min functionality to init script (probe10min 
  helps on experiments with new FW rules),
- added noreplace parameter for %config for config files with firewall
  rules.

* Mon Aug 18 1997 Bryan C. Andregg <bandregg@redhat.com>
  [1.2-3]
Fixed error handling typo.
Removed handling of the 'any' case in favor of 'any/0'
Added masquerading notes in README.
Added empty config files.

* Sun Aug 17 1997 Bryan C. Andregg <bandregg@redhat.com>
Major bug fixes.
Added 'Requires' field.
Changes S9 to S09 in the rc.d runlevel dirs.
Fixed spelling errors.
Changed %config to %dir for /etc/sysconfig/firewall-rules.

* Wed Aug 13 1997 Bryan C. Andregg <bandregg@redhat.com>
Fixed numerous spelling errors.
Added stderr redirection to > /dev/null and logging of errors to syslogd.
Fixed bugs in /etc/rc.d/init.d/firewall
Changed version to 1.1.
Added support for ANY|any keyword in addrs,masks and ports.
Added accounting rule set.
Fixed xxx.xxx.xxx.xxx netmask format bug.
Cleaned up firewall.init.

* Tue Aug 12 1997 Bryan C. Andregg <bandregg@redhat.com>
Included README.
Moved /etc/sysconfig/firewall-ruels/input to %doc/input.example.
Initial build.
