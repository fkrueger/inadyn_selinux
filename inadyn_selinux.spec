# vim: sw=4:ts=4:et

%define inadyn_ver 5.21.0
%define selinux_policyver 3.14.3-1
%define selinux_ppname inadyn

%define selinux_dirs /etc/inadyn* /home/*/.inadyn /root/.inadyn /run/inadyn /usr/bin/inadyn* /var/lib/inadyn /var/run/inadyn


Name:   inadyn_selinux
Version:	1.0
Release:	4%{?dist}
Summary:	SELinux policy module for inadyn (based on the GIT releases)
BuildRequires: policycoreutils, selinux-policy-devel
Requires:	selinux-policy, selinux-policy-targeted

Group:	System Environment/Base		
License:	GPLv2+
URL:		https://dev.techno.holics.at/inadyn_selinux/
Source0:	inadyn.te
Source1:	inadyn.fc
Source2:	inadyn.if

Requires: policycoreutils, libselinux-utils
Requires(post): selinux-policy-base >= %{selinux_policyver}, policycoreutils
Requires(postun): policycoreutils
BuildArch: noarch

%description
This package installs and sets up the SELinux policy security module for inadyn (pid-files under /run, /var/run; cache-files under /var/lib/inadyn/.inadyn (and maybe the user homedirs ~/.inadyn for /home and /root).

%install
install -d %{buildroot}/etc/selinux/targeted/contexts/users/
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{_builddir}/%{name}-%{version}-%{release}.%{_arch}/inadyn.pp %{buildroot}%{_datadir}/selinux/packages




%build
TMPB="%{_builddir}/%{name}-%{version}-%{release}.%{_arch}/"
mkdir -p "$TMPB"
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} "$TMPB"
cd "$TMPB"
make -f /usr/share/selinux/devel/Makefile

%post
# install policy modules
semodule -n -i %{_datadir}/selinux/packages/inadyn.pp
if /usr/sbin/selinuxenabled ; then
    /usr/sbin/load_policy
    restorecon -R %{selinux_dirs} >/dev/null 2>&1 ||:
fi;
exit 0

%postun
if [ $1 -eq 0 ]; then
    # then try to remove the policy module
    semodule -n -r inadyn
    if /usr/sbin/selinuxenabled ; then
       /usr/sbin/load_policy
       /usr/sbin/restorecon -R %{selinux_dirs} >/dev/null 2>&1 ||:
    fi;
fi;
exit 0

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/inadyn.pp

%changelog
* Tue Apr 4 2023 Frederic Krueger <fkrueger-dev-selinux_inadyn@holics.at> 1.0-1
- Initial version

