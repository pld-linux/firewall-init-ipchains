Summary:	Firewall SysV-init style start-up script
Summary(pl):	Skrypt startowy firewalla
Name:		firewall-init
Version:	2.99.5
Release:	2@2.4
License:	GPL
Group:		Networking/Admin
Group(de):	Netzwerkwesen/Administration
Group(pl):	Sieciowe/Administacyjne
Source0:	ftp://ftp.pld.org.pl/software/firewall-init/%{name}-%{version}.tar.gz
Patch0:		%{name}-pre.patch
Requires:	iptables >= 1.2.2-2
Conflicts:	kernel < 2.3.0
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Buildarch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Firewall-init is meant to provide an easy to use interface to start
and stopping the kernel IP packet filter through iptables(8).

%description -l pl
Dziêki firewall-init uzyskuje siê ³atwy interfejs do startowania i
stopowania filtrów IP j±dra poprzez iptables(8).

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README

%post
/sbin/chkconfig --add firewall
/sbin/chkconfig --add firewall-pre

%postun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del firewall
	/sbin/chkconfig --del firewall-pre
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz
%defattr(640,root,root,750)
%verify(not size mtime md5) %config(noreplace) /etc/sysconfig/firewall
%verify(not size mtime md5) %config(noreplace) /etc/sysconfig/firewall.d/ip*
%verify(not size mtime md5) %config(noreplace) /etc/sysconfig/firewall.d/functions.rules
/etc/sysconfig/firewall.d/functions
%attr(754,root,root) /etc/rc.d/init.d/firewall*
%dir /etc/sysconfig/firewall.d
