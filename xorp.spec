%define name xorp
%define version 1.4
%define release %mkrel 4

Summary:  Open Router Platform
Name:    %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: BSD
Group:   Networking/Other
Url:     http://www.xorp.org
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: openssl-devel

%description
XORP is an open router platform being developed at the ICSI Center for
Open Networking (ICON) at the International Computer Science Institute
in Berkeley, California, USA. XORP primary goal is to be both a research
tool and a stable deployment platform that can be used to close the gap
between network research and real world

%prep
%setup -q

%build
%configure \
        --datadir="%{_datadir}/xorp"
%{make} 

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall \
        datadir="%{buildroot}%{_datadir}/xorp"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BUGS BUILD_NOTES ERRATA LICENSE README RELEASE_NOTES TODO VERSION
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/xorp/

%changelog
