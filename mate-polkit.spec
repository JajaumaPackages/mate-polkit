# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.16

# Settings used for build from snapshots.
%{!?rel_build:%global commit 8e0c8e17e0138afa7757a1bdf8edd6f2c7b47a14}
%{!?rel_build:%global commit_date 20150930}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:		mate-polkit
Version:    %{branch}.0
%if 0%{?rel_build}
Release:	1%{?dist}
%else
Release:    0.2%{?git_rel}%{?dist}
%endif
Summary:	Integrates polkit authentication for MATE desktop
License:	LGPLv2+
URL:		http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R mate-polkit.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

BuildRequires:	gtk3-devel
BuildRequires:	mate-common
BuildRequires:	polkit-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	dbus-glib-devel
# needed for gobject-introspection support somehow,
# https://bugzilla.redhat.com/show_bug.cgi?id=847419#c17 asserts this is a bug (elsewhere)
# but I'm not entirely sure -- rex
BuildRequires: 	cairo-gobject-devel

Provides:	PolicyKit-authentication-agent


%description
Integrates polkit with the MATE Desktop environment

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary:	Integrates polkit with the MATE Desktop environment

%description devel
Development libraries for mate-polkit


%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# for snapshots
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure  \
        --disable-static       \
        --with-gtk=3.0         \
        --enable-introspection \
        --enable-accountsservice \
        --enable-gtk-doc-html

make %{?_smp_mflags} V=1

%install
%{make_install}

%find_lang %{name}

find %{buildroot} -name '*.la' -exec rm -fv {} ';'


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -f %{name}.lang
# yes, license really is LGPLv2+, despite included COPYING is about GPL, poke upstreamo
# to include COPYING.LIB here instead  -- rex
%doc AUTHORS COPYING README
%{_sysconfdir}/xdg/autostart/polkit-mate-authentication-agent-1.desktop
%{_libdir}/libpolkit-gtk-mate-1.so.0
%{_libdir}/libpolkit-gtk-mate-1.so.0.0.0
%{_libdir}/girepository-1.0/PolkitGtkMate-1.0.typelib
%{_libexecdir}/polkit-mate-authentication-agent-1

%files devel
%{_libdir}/libpolkit-gtk-mate-1.so
%{_libdir}/pkgconfig/polkit-gtk-mate-1.pc
%{_includedir}/polkit-gtk-mate-1
%{_datadir}/gir-1.0/PolkitGtkMate-1.0.gir


%changelog
* Tue Sep 27 2016 Jajauma's Packages <jajauma@yandex.ru> - 1.16.0-1
- Update to latest upstream release

* Thu Jun 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-1
- update to 1.15.0 release

* Tue Apr 05 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-1
- update to 1.14.0 release

* Sun Feb 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.0-1
- update to 1.13.0 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release

* Wed Oct 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release

* Thu Sep 17 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2.1
- update to 1.10.2 release
- build against gtk3 for f23
- enable accountsservice for faces

* Wed Sep 02 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1.1
- update to 1.10.1 release
- remove upstreamed patch

* Wed Aug 19 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-3
- fix missing focus on polkit windows
- https://github.com/mate-desktop/mate-polkit/pull/22

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release

* Thu Feb 26 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90-1
- update to 1.9.90 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sun Feb 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90 release

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Thu Dec 05 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.
 
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release

* Mon Aug 27 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-4
- drop extraneous update-desktop-database scriptlet
- don't mark .desktop file %%config
- License: LGPLv2+

* Sun Aug 26 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Move PolkitGTKMate gir file to devel package

* Sat Aug 18 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Remove duplicate doc macro, add provides, fix post macro, have devel package own proper dir

* Wed Aug 08 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
