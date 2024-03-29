Summary:	H.323 gatekeeper and proxy
Summary(pl.UTF-8):	Gatekeeper i proxy dla protokołu H.323
Name:		openh323proxy
Version:	0.9.13
Release:	2
Epoch:		1
License:	MPL 1.0
Group:		Applications/Communications
Source0:	http://dl.sourceforge.net/openh323proxy/%{name}-%{version}.tar.gz
# Source0-md5:	f25116bd22a0f648222f50cff3a5dd50
Source1:	%{name}.ini
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-mak_files.patch
Patch1:		%{name}-config_file_path.patch
Patch2:		%{name}-c++.patch
Patch3:		%{name}-pwlib.patch
URL:		http://openh323proxy.sourceforge.net/
BuildRequires:	expat-devel
BuildRequires:	openh323-devel >= 1.12.0
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pwlib-devel >= 1.7
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
%requires_eq	openh323
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
H.323 is widely used Internet teleconferencing protocol. Openh323proxy
acts as H.323 gatekeeper and proxy. A H.323 gatekeeper controls all
H.323 clients (endpoints like MS Netmeeting) in his zone. Its most
important function is address translation between symbolic alias
addresses and IP addresses. This way you can call "jan" instead of
knowing which IP address he currently works on.

%description -l pl.UTF-8
H.323 to popularny internetowy protokół telekonferencyjny, używany
między innymi przez program NetMeeting. Openh323proxy służy jako
gatekeeper oraz Proxy dla tego protokołu. Gatekeeper obsługuje
wszystkich klientów H.323 w swoim zasięgu. Jego najważniejszą funkcją
jest tłumaczenie pomiędzy nazwami symbolicznymi i adresami IP. Jako
proxy pakiet ten umożliwia połączenia H.323 pomiędzy siecią wewnętrzną
(za firewallem lub NAT), a Internetem.

%prep
%setup -qn %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make} %{?debug:debugshared}%{!?debug:optshared} \
	OPTCCFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/etc/{/rc.d/init.d,/sysconfig}}

install obj_*/opengate_proxy $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/openh323proxy
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/openh323proxy

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add openh323proxy
if [ -r /var/lock/subsys/openh323proxy ]; then
	/etc/rc.d/init.d/openh323proxy restart >&2
else
	echo "Run \"/etc/rc.d/init.d/openh323proxy start\" to start OpenH323 Proxy."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/openh323proxy ]; then
		/etc/rc.d/init.d/openh323proxy stop >&2
	fi
	/sbin/chkconfig --del openh323proxy
fi

%files
%defattr(644,root,root,755)
%doc *.txt
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openh323proxy.ini
%attr(754,root,root) /etc/rc.d/init.d/openh323proxy
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/openh323proxy
