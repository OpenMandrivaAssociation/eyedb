# -*-rpm-spec-*-

%define name    eyedb
%define version 2.8.0 
%define release %mkrel 5
%define group   Databases

%define _requires_exceptions devel(libcrypt(64bit))\\|devel(libdl(64bit))\\|devel(libgcc_s(64bit))\\|devel(libm(64bit))\\|devel(libnsl(64bit))\\|devel(libstdc++(64bit))  

%define _unpackaged_files_terminate_build	0
%define _missing_doc_files_terminate_build	0

Name:           %{name} 
Summary:        Object Database Management System
Version:        %{version} 
Release:        %{release} 
URL:            https://www.eyedb.org
License:        LGPL
Group:          %{group}
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot 

%description
EyeDB is an Object Database Management System (ODBMS).

%package common
Summary: EyeDB client and server common libraries
Group: %{group}
Provides: %{name}-common = %{version}
BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: bison
BuildRequires: flex
%description common
EyeDB client and server common libraries

%package client
Summary: EyeDB client libraries and binaries
Group: %{group}
Provides: %{name}-client = %{version}
BuildRequires: make
BuildRequires: gcc-c++
%description client
EyeDB client libraries and binaries

%package server
Summary: EyeDB server libraries and binaries
Group: %{group}
Provides: %{name}-server = %{version}
BuildRequires: make
BuildRequires: gcc-c++
%description server
EyeDB server libraries and binaries

%package devel
Summary: EyeDB headers files
Group: %{group}
Provides: %{name}-devel = %{version}
BuildRequires: make
BuildRequires: gcc-c++
%description devel
EyeDB headers files

%package doc
Summary: EyeDB documentation
Group: %{group}
Provides: %{name}-doc = %{version}
BuildRequires: make
BuildRequires: libxslt-proc
BuildRequires: docbook-style-xsl
BuildRequires: tetex-latex
#BuildRequires: latex2html
%description doc
EyeDB documentation

# other packages: -java, -www
# java: don't forget %{_bindir}/eyedbgetenv

%prep 
%setup -q

%build 
%configure 
%make 

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
make DESTDIR=%{buildroot} install
# Install directories
install -d -m 700 %{buildroot}/var/lib/eyedb/db
install -d -m 700 %{buildroot}/var/lib/eyedb/pipes
install -d -m 700 %{buildroot}/var/lib/eyedb/tmp
# Install the init script
install -d %{buildroot}%{_initrddir}
install -m0755 scripts/eyedb.init %{buildroot}%{_initrddir}/eyedb
# Install the sysconfiguration file
# FIXME
#install -d %{buildroot}%{_sysconfdir}/sysconfig
#install -m0644 eyedb.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/eyedb

%pre server
# create eyedb user
%_pre_useradd eyedb /var/lib/eyedb /bin/bash
# create DBM
#/usr/share/eyedb/tools/eyedb-postinstall.sh

%postun server
%_postun_userdel eyedb

%clean 
#rm -rf %{buildroot}

%files common
%defattr(-,root,root)
%{_libdir}/libeyedb-%{version}.so
%{_libdir}/libeyedb.so
%{_libdir}/libeyedbsm-%{version}.so
%{_libdir}/libeyedbsm.so
%{_libdir}/libeyedbutils-%{version}.so
%{_libdir}/libeyedbutils.so
%{_libdir}/libeyedbrpcfe-%{version}.so
%{_libdir}/libeyedbrpcfe.so
%{_docdir}/%{name}/AUTHORS
%{_docdir}/%{name}/COPYING
%{_docdir}/%{name}/README

%files client
%defattr(-,root,root)
%{_bindir}/eyedbadmin
%{_bindir}/eyedbodl
%{_bindir}/eyedboql
%{_bindir}/eyedbloca
%{_bindir}/eyedbidxadmin
%{_bindir}/eyedbprotadmin
%{_bindir}/eyedbconsadmin
%{_bindir}/eyedbcollimpladmin
%{_bindir}/eyedbgetenv
%{_datadir}/%{name}/eyedb.conf.sample

%files server
%defattr(-,root,root)
%{_sbindir}/eyedbctl
%{_sbindir}/eyedbd
%{_sbindir}/eyedbsmd
%{_sbindir}/eyedbsmtool
%{_libdir}/libeyedbrpcbe-%{version}.so
%{_libdir}/libeyedbrpcbe.so
%{_libdir}/eyedb/oqlctbmthfe-%{version}.so
%{_libdir}/eyedb/oqlctbmthfe.so
%{_libdir}/eyedb/sysclsmthfe-%{version}.so
%{_libdir}/eyedb/sysclsmthfe.so
%{_libdir}/eyedb/utilsmthfe-%{version}.so
%{_libdir}/eyedb/utilsmthfe.so
%{_libdir}/eyedb/oql/stdlib.oql
%{_datadir}/%{name}/eyedbd.conf.sample
%{_datadir}/%{name}/Access.sample
%{_datadir}/%{name}/tools/eyedb-postinstall.sh
%{_initrddir}/eyedb
%attr(700,eyedb,eyedb) %dir %_var/lib/eyedb/db
%attr(700,eyedb,eyedb) %dir %_var/lib/eyedb/pipes
%attr(700,eyedb,eyedb) %dir %_var/lib/eyedb/tmp
# man pages

%files devel
%defattr(-,root,root)
%{_includedir}/eyedb/*.h
%{_includedir}/eyedb/internals/*.h
%{_includedir}/eyedblib/*.h
%{_includedir}/eyedbsm/*.h
%{_libdir}/pkgconfig/eyedb.pc
# must add .la libraries

%files doc
%defattr(-,root,root)
%{_docdir}/%{name}/index.html
%{_docdir}/%{name}/eyedbdoc.css
%{_docdir}/%{name}/examples
%{_docdir}/%{name}/images
%{_docdir}/%{name}/manual
# man pages
# to be completed

# in which package should the APIs docs go?
#%{_docdir}/%{name}-%{version}/api

%changelog 
* Fri Feb 9 2007 Francois Dechelle <francois@dechelle.net>
- initial spec file
