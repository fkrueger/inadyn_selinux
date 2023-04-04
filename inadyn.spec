%global username inadyn

%global gituser troglobit
%global gitrepo inadyn

%define  debug_package %{nil}
%define _build_id_links none

Name:           inadyn
Version:        2.10.0
Release:        1%{?dist}
Summary:        Simple and small DynDNS client written in the C language
License:        GPLv2
URL:            https://github.com/%{gituser}/%{gitrepo}

Source0:        https://github.com/%{gituser}/%{gitrepo}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        inadyn.default
Source2:        inadyn.service
Source3:        inadyn.init
Source4:        inadyn-wrapper.sh

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libconfuse-devel
BuildRequires:  gnutls-devel

Requires:  sudo

%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
Requires:	gnutls, libconfuse
#, inadyn_selinux
%endif

%if 0%{?rhel} == 6
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service
Requires(postun):   /sbin/service
Requires:       gnutls, libconfuse
%endif

%description
In-a-Dyn allows you to keep your dyndns entries updated in a constantly moving world.

That's it.


%prep
%setup -q
#% patch0 -p1


%build
autoreconf -vif
%configure
make %{?_smp_mflags}
cd man
gzip inadyn.8 inadyn.conf.5
cd ..


%install

mkdir -p %{buildroot}%{_datadir}/doc/%{name}/examples/
mkdir -p %{buildroot}/var/lib/inadyn/.inadyn/

install -p -m 755 -D src/inadyn %{buildroot}%{_bindir}/inadyn
install -p -m 755 -D %{SOURCE4} %{buildroot}%{_bindir}/inadyn-wrapper.sh

install -p -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/default/inadyn

install -p -m 644 -D examples/inadyn.conf %{buildroot}%{_sysconfdir}/inadyn.conf

install -p -m 644 -D man/inadyn.conf.5.gz %{buildroot}%{_mandir}/man5/inadyn.conf.5.gz
install -p -m 644 -D man/inadyn.8.gz %{buildroot}%{_mandir}/man8/inadyn.8.gz

install -p -m 644 COPYING %{buildroot}%{_datadir}/doc/%{name}/COPYING
install -p -m 644 ChangeLog.md %{buildroot}%{_datadir}/doc/%{name}/ChangeLog.md
install -p -m 644 README.md %{buildroot}%{_datadir}/doc/%{name}/README.md
install -p -m 644 examples/*.conf %{buildroot}%{_datadir}/doc/%{name}/examples/





%if 0%{?fedora} || 0%{?rhel} >= 7

# Systemd unit files
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_unitdir}/inadyn.service

%else

# Initscripts
install -p -m 755 -D %{SOURCE3} %{buildroot}%{_initrddir}/inadyn

%endif




%pre
getent group %username >/dev/null || groupadd -r %username &>/dev/null || :
getent passwd %username >/dev/null || useradd -r -s /sbin/nologin -d /tmp -M -c 'In-a-Dyn' -g %username %username &>/dev/null || :
exit 0

%if 0%{?fedora} || 0%{?rhel} >= 7

%post
%systemd_post inadyn.service
/bin/firewall-cmd --reload >/dev/null 2>&1 || :

%preun
%systemd_preun inadyn.service
/bin/firewall-cmd --reload >/dev/null 2>&1 || :

%postun
%systemd_postun_with_restart inadyn.service
/bin/firewall-cmd --reload >/dev/null 2>&1 || :
%endif


%if 0%{?rhel} == 6

%post
/sbin/chkconfig --add inadyn

%preun
if [ "$1" = 0 ]; then
  /sbin/service inadyn stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del inadyn
fi

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service inadyn condrestart >/dev/null 2>&1 || :
fi

%endif



%files
%{!?_licensedir:%global license %%doc}
%doc AUTHORS COPYING ChangeLog.md README.md
%doc %{_datadir}/doc/%{name}/examples
%config(noreplace) %{_sysconfdir}/inadyn.conf
%config(noreplace) %{_sysconfdir}/default/inadyn
%{_bindir}/inadyn
%{_bindir}/inadyn-wrapper.sh
%{_mandir}/man5/inadyn.conf.5*
%{_mandir}/man8/inadyn.8*
%dir %attr(2775,inadyn,inadyn) /var/lib/inadyn
%dir %attr(2775,inadyn,inadyn) /var/lib/inadyn/.inadyn
#% {_datadir}/doc/%{name}
%if 0%{?fedora} || 0%{?rhel} >= 7
%{_unitdir}/inadyn.service
%else
%{_initrddir}/inadyn
%endif


%changelog
* Mon Apr 3 2023 Frederic Krueger <fkrueger-dev-el8_inadyn@holics.at> - 2.10.0-1
- Initial spec file release

