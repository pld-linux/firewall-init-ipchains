Summary:	Firewall SysV-init style start-up script
Summary(pl):	Skrypt startowy firewalla
Name:		firewall-init
Version:	2.1
Release:	2@2.2
License:	BSD
Group:		Networking/Admin
Source0:	ftp://ftp.lj.pl/pub/linux/%{name}-%{version}.tar.gz
Requires:	ipchains
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
Buildarch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Firewall-init is meant to provide an easy to use interface to start
and stopping the kernel IP packet filters and accounting through
ipchains(8).

%description -l pl
Dziêki firewall-init uzyskuje siê ³atwy interfejs do startowania i
stopowania filtrów IP j±dra oraz zliczania pakietów poprzez
ipchains(8).

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
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del firewall
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README input.example
%attr(600,root,root) %verify(not size mtime md5) %config(noreplace) /etc/sysconfig/firewall
%attr(600,root,root) %verify(not size mtime md5) %config(noreplace) /etc/sysconfig/firewall-rules/*
%attr(700,root,root) %dir /etc/sysconfig/firewall-rules
%attr(754,root,root) /etc/rc.d/init.d/firewall
