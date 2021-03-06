%define		_name	firewall-init
Summary:	ipchains firewall SysV-init style start-up script
Summary(pl.UTF-8):	Skrypt startowy firewalla ipchains
Name:		%{_name}-ipchains
Version:	2.1
Release:	5
License:	BSD
Group:		Networking/Admin
Source0:	%{_name}-%{version}.tar.gz
# Source0-md5:	07ba7a897e2d903d629e6607e3b495f3
Patch0:		%{_name}-syntax_verify.patch
Requires(post,preun):	/sbin/chkconfig
Requires:	ipchains
Requires:	rc-scripts
Obsoletes:	firewall-init < 2.2
Conflicts:	firewall-init >= 2.99
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Firewall-init is meant to provide an easy to use interface to start
and stopping the kernel IP packet filters and accounting through
ipchains(8).

%description -l pl.UTF-8
Dzięki firewall-init uzyskuje się łatwy interfejs do startowania i
stopowania filtrów IP jądra oraz zliczania pakietów poprzez
ipchains(8).

%prep
%setup -q -n %{_name}-%{version}
%patch0 -p1

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
%attr(600,root,root) %verify(not md5 mtime size) %config(noreplace) /etc/sysconfig/firewall
%attr(600,root,root) %verify(not md5 mtime size) %config(noreplace) /etc/sysconfig/firewall-rules/*
%attr(700,root,root) %dir /etc/sysconfig/firewall-rules
%attr(754,root,root) /etc/rc.d/init.d/firewall
