%define schemas baobab gnome-dictionary gnome-screenshot gnome-search-tool gnome-system-log
%define major 6
%define libname %mklibname gdict1.0_ %{major}
%define libnamedev %mklibname -d gdict1.0
Summary: GNOME utility programs such as file search and calculator
Name: gnome-utils
Version: 2.28.1
Epoch: 1
Release: %mkrel 1
License: GPLv2+ and GFDL
Group:  Graphical desktop/GNOME
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
URL: http://www.gnome.org/softwaremap/projects/gnome-utils/

BuildRequires:  libpanel-applet-2-devel >= 2.9.4
BuildRequires:  libglade2.0-devel
BuildRequires:  avahi-glib-devel avahi-client-devel
BuildRequires:  libxmu-devel
BuildRequires:  libgtop2.0-devel
BuildRequires:  libcanberra-devel
BuildRequires:	ncurses-devel
BuildRequires:  scrollkeeper
BuildRequires:	gnome-doc-utils
BuildRequires:  gnome-common
BuildRequires:  gtk-doc
BuildRequires:  intltool
BuildRequires:  desktop-file-utils

Requires: gnome-mount
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

Obsoletes:	gnome-admin
Obsoletes:	baobab
Provides: gnome-admin
Provides: baobab

Conflicts: gnome-panel < 2.10.1

%description
GNOME is the GNU Network Object Model Environment. This powerful
environment is both easy to use and easy to configure.

GNOME Utilities is a collection of small applications all there to make
your day just that little bit brighter - System Log Viewer, 
Search Tool, Dictionary.

%package -n %libname
Group: System/Libraries
Summary: GNOME dictionary shared library

%description -n %libname
This is the shared library required by the GNOME Dictionary.

%package -n %libnamedev
Group: Development/C
Summary: GNOME dictionary library development files
Requires: %libname = %epoch:%version
Provides: libgdict1.0-devel = %epoch:%version-%release
Obsoletes: %mklibname -d gdict1.0_ 5

%description -n %libnamedev
This is the shared library required by the GNOME Dictionary.

%prep
%setup -q

%build

%configure2_5x  --enable-hal

#needed to ensure generated stuff is removed
make clean

%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
rm -rf %buildroot/var

# make gnome-system-log use consolehelper until it starts using polkit
./mkinstalldirs $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
/bin/cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/pam.d/gnome-system-log
#%%PAM-1.0
auth		include		system-auth
account		include		system-auth
session		include		system-auth
EOF

./mkinstalldirs $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
/bin/cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/gnome-system-log
USER=root
PROGRAM=/usr/sbin/gnome-system-log
SESSION=true
FALLBACK=true
EOF

./mkinstalldirs $RPM_BUILD_ROOT%{_sbindir}
/bin/mv $RPM_BUILD_ROOT%{_bindir}/gnome-system-log $RPM_BUILD_ROOT%{_sbindir}
/bin/ln -s /usr/bin/consolehelper $RPM_BUILD_ROOT%{_bindir}/gnome-system-log

%{find_lang} %{name}-2.0 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/*/{*-??,*-??_??}.omf ;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name-2.0.lang
done

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-FileTools" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/{gnome-search-tool.desktop,baobab.desktop}
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-Monitoring" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/gnome-system-log.desktop
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-Office-Accessories" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/gnome-dictionary.desktop

for i in $RPM_BUILD_ROOT%{_datadir}/applications/* ; do
 desktop-file-validate $i
done

rm -fv %buildroot%_bindir/test-reader

%if %mdkversion < 200900
%post
%update_scrollkeeper
%post_install_gconf_schemas %schemas
%{update_menus}
%update_icon_cache hicolor
%endif

%preun
%preun_uninstall_gconf_schemas %schemas

%if %mdkversion < 200900
%postun
%clean_scrollkeeper
%{clean_menus}
%clean_icon_cache hicolor
%endif

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-2.0.lang
%defattr(-, root, root)

%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/security/console.apps/gnome-system-log
%{_sysconfdir}/pam.d/gnome-system-log
%{_sysconfdir}/gconf/schemas/baobab.schemas
%{_sysconfdir}/gconf/schemas/gnome-dictionary.schemas
%{_sysconfdir}/gconf/schemas/gnome-screenshot.schemas
%{_sysconfdir}/gconf/schemas/gnome-search-tool.schemas
%{_sysconfdir}/gconf/schemas/gnome-system-log.schemas
%_bindir/baobab
%_bindir/gnome-dictionary
%_bindir/gnome-panel-screenshot
%_bindir/gnome-screenshot
%_bindir/gnome-search-tool
%_bindir/gnome-system-log
%{_sbindir}/gnome-system-log
%{_libdir}/bonobo/servers/*
%{_datadir}/applications/*
%{_datadir}/baobab/
%{_datadir}/gnome-screenshot
%{_datadir}/gnome-utils
%{_datadir}/gnome-2.0/ui/*
%_libexecdir/gnome-dictionary-applet
%_datadir/gdict*
%{_datadir}/gnome-dictionary/
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%_datadir/icons/hicolor/*/apps/*
%{_mandir}/*/*
%{_datadir}/pixmaps/*

%files -n %libname
%defattr(-, root, root)
%_libdir/libgdict-1.0.so.%{major}*

%files -n %libnamedev
%defattr(-, root, root)
%_libdir/libgdict*.so
%attr(644,root,root) %_libdir/libgdict*a
%_libdir/pkgconfig/gdict*.pc
%{_datadir}/gtk-doc/html/gdict
%_includedir/gdict*
