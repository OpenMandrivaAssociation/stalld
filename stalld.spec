Summary:	Daemon that finds starving tasks and gives them a temporary boost
Name:		stalld
Version:	1.5
Release:	1
License:	GPLv2
URL:		https://git.kernel.org/pub/scm/utils/stalld/stalld.git
Source0:	https://git.kernel.org/pub/scm/utils/stalld/stalld.git/snapshot/%{name}-%{version}.tar.gz
BuildRequires:	glibc-devel
BuildRequires:	systemd-macros
Requires:	systemd

%description
The stalld program monitors the set of system threads,
looking for threads that are ready-to-run but have not
been given processor time for some threshold period.
When a starving thread is found, it is given a temporary
boost using the SCHED_DEADLINE policy. The default is to
allow 10 microseconds of runtime for 1 second of clock time.

%prep
%autosetup -p1

%build
%set_build_flags
%make_build CC=%{__cc} CFLAGS="%{optflags} -DVERSION="\\\"%{version}\\\""" LDFLAGS="%{build_ldflags}"

%install
%make_install DOCDIR=%{_docdir} MANDIR=%{_mandir} BINDIR=%{_bindir} DATADIR=%{_datadir} VERSION=%{version}
%make_install -C redhat UNITDIR=%{_unitdir}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/stalld
%doc %{_docdir}/README.md
%doc %{_mandir}/man8/stalld.8*
%license gpl-2.0.txt
