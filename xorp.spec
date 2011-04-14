#define Werror_cflags %nil
#define _disable_ld_no_undefined 1

# configure options
%define with_shared	1
%define with_optimize	1
%define with_strip	1
%define prefixdir	/usr/local/xorp

Summary:          An eXtensible Open Router Platform (XORP)
Name:             xorp
Version:          1.8.3
Release:          %mkrel 0
License:          GPL
Group:            System/Servers
Source0:          xorp-%{version}.tar.lzma
Source1:          xorp.init
Source2:          xorp.sysconfig
Source3:          xorp.logrotate
Source4:          xorp.conf
URL:              http://www.xorp.org
Buildroot:        %{_tmppath}/xorp-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         traceroute
Requires(pre):    /usr/sbin/groupadd
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig /sbin/service
Requires(postun): /sbin/service
BuildRequires:    libpcap-devel ncurses-devel
BuildRequires:    scons openssl-devel python


%description
XORP is an extensible open-source routing platform. Designed for extensibility
from the start, XORP provides a fully featured platform that implements IPv4
and IPv6 routing protocols and a unified platform to configure them. XORP's
modular architecture allows rapid introduction of new protocols, features and
functionality, including support for custom hardware and software forwarding.


%prep
%setup -q -n xorp


%build
export CXXFLAGS="-Wunused-but-set-variable"
export CFLAGS="-Wunused-but-set-variable"
scons -j4 \
                                DESTDIR=${RPM_BUILD_ROOT}     \
                                sbindir=%{_sbindir}           \
                                prefix=%{prefixdir}           \
                                libexecdir=%{_libexecdir}     \
                                sysconfdir=%{_sysconfdir}     \
                                xorp_confdir=%{_sysconfdir}   \
                                localstatedir=%{_localstatedir} \
				ignore_check_errors=yes \
%if %with_shared
  shared=yes \
%endif
%if %with_optimize
  optimize=yes \
%endif
%if %with_strip
  strip=yes \
%endif


%install
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_initrddir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_sysconfdir}/{logrotate.d,sysconfig,xorp}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_sbindir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_datadir}/xorp

scons \
				DESTDIR=${RPM_BUILD_ROOT}     \
				sbindir=%{_sbindir}           \
                                prefix=%{prefixdir}           \
				libexecdir=%{_libexecdir}     \
				sysconfdir=%{_sysconfdir}     \
				xorp_confdir=%{_sysconfdir}   \
				localstatedir=%{_localstatedir} \
				ignore_check_errors=yes \
%if %with_shared
  shared=yes \
%endif
%if %with_optimize
  optimize=yes \
%endif
%if %with_strip
  strip=yes \
%endif
				install

%{__install} -m 0755 %{SOURCE1}           ${RPM_BUILD_ROOT}%{_initrddir}/xorp
%{__install} -m 0644 %{SOURCE2}           ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/xorp
%{__install} -m 0644 %{SOURCE3}           ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/xorp
%{__install} -m 0660 %{SOURCE4}           ${RPM_BUILD_ROOT}%{_sysconfdir}/xorp

%pre
if ! getent group  %{name} >/dev/null 2>&1; then
  /usr/sbin/groupadd -r %{name}
	/usr/sbin/usermod -G %{name} root
fi
exit 0			# Always pass

%post
%_post_service %{name}

%preun
%_preun_service %{name}


%postun
%_postun_groupdel %{name}


%clean
[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && %{__rm} -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc BUGS  BUILD_NOTES ERRATA  LICENSE*
%doc README RELEASE_NOTES VERSION
%{_initrddir}/xorp
%config(noreplace) %{_sysconfdir}/logrotate.d/xorp
%config(noreplace) %{_sysconfdir}/sysconfig/xorp
%attr(770,root,xorp) %dir %{_sysconfdir}/xorp
%attr(660,root,xorp) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xorp/xorp.conf
%{_sbindir}
%{prefixdir}
%{_datadir}
