%define schemas baobab gnome-dictionary gfloppy gnome-screenshot gnome-search-tool gnome-system-log
%define major 6
%define libname %mklibname gdict1.0_ %{major}
%define libnamedev %mklibname -d gdict1.0
Summary: GNOME utility programs such as file search and calculator
Name: gnome-utils
Version: 2.25.90
Epoch: 1
Release: %mkrel 1
License: GPLv2+ and GFDL
Group:  Graphical desktop/GNOME
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2

Patch2: gnome-utils-gfloppy-device.patch
Patch3: gnome-utils-2.25.0-format-strings.patch
# (fc) 2.19.92-2mdv unmount floppy before trying for format them (Mdv bug #24590)
Patch4: gnome-utils-2.19.92-unmount-floppy.patch
Patch6: gnome-utils-2.25.90-linking.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
URL: http://www.gnome.org/softwaremap/projects/gnome-utils/

BuildRequires:  libpanel-applet-2-devel >= 2.9.4
BuildRequires:  gnome-desktop-devel >= 2.2.0
BuildRequires:  libglade2.0-devel >= 2.3.0
BuildRequires:  gnome-vfs2-devel >= 2.8.4
BuildRequires:  avahi-glib-devel avahi-client-devel
BuildRequires:  libxmu-devel
BuildRequires:  libgtop2.0-devel
BuildRequires:	ncurses-devel
BuildRequires:  scrollkeeper
BuildRequires:	gnome-doc-utils
BuildRequires:  gnome-common
BuildRequires:  gtk-doc
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
#needed for gfloppy
BuildRequires:  e2fsprogs-devel
BuildRequires:  hal-devel

Requires: gnome-mount
Requires(post): scrollkeeper
Requires(postun): scrollkeeper

Obsoletes:	gfloppy
Obsoletes:	gnome-admin
Obsoletes:	baobab
Provides: gfloppy
Provides: gnome-admin
Provides: baobab

Conflicts: gnome-panel < 2.10.1

%description
GNOME is the GNU Network Object Model Environment. This powerful
environment is both easy to use and easy to configure.

GNOME Utilities is a collection of small applications all there to make
your day just that little bit brighter - System Log Viewer, 
Search Tool, Dictionary, Floppy Format.

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
%patch2 -p1 -b .device
%patch3 -p1
%patch4 -p1 -b .unmount-floppy
%patch6 -p1 -b .linking
autoreconf -fi

%build

%configure2_5x  --enable-gfloppy --enable-hal

%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
rm -rf %buildroot/var

%{find_lang} %{name}-2.0 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/*/{*-??,*-??_??}.omf ;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name-2.0.lang
done

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="X-MandrivaLinux-System-Configuration-Hardware" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/gfloppy.desktop
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
%{_sysconfdir}/gconf/schemas/baobab.schemas
%{_sysconfdir}/gconf/schemas/gfloppy.schemas
%{_sysconfdir}/gconf/schemas/gnome-dictionary.schemas
%{_sysconfdir}/gconf/schemas/gnome-screenshot.schemas
%{_sysconfdir}/gconf/schemas/gnome-search-tool.schemas
%{_sysconfdir}/gconf/schemas/gnome-system-log.schemas
%_bindir/baobab
%_bindir/gfloppy
%_bindir/gnome-dictionary
%_bindir/gnome-panel-screenshot
%_bindir/gnome-screenshot
%_bindir/gnome-search-tool
%_bindir/gnome-system-log
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
