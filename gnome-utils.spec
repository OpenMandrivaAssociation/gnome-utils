%define schemas baobab gnome-dictionary gfloppy gnome-screenshot gnome-search-tool logview
%define major 6
%define libname %mklibname gdict1.0_ %{major}
%define libnamedev %mklibname -d gdict1.0
Summary: GNOME utility programs such as file search and calculator
Name: gnome-utils
Version: 2.24.1
Epoch: 1
Release: %mkrel 2
License: GPLv2+ and GFDL
Group:  Graphical desktop/GNOME
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Source10: gdict_48.png
Source11: gdict_32.png
Source12: gdict_16.png
Source13: gfloppy-48.png
Source14: gfloppy-32.png
Source15: gfloppy-16.png
Source22: gnome-searchtool-48.png
Source23: gnome-searchtool-32.png
Source24: gnome-searchtool-16.png
Source34: logview-48.png
Source35: logview-32.png
Source36: logview-16.png

Patch0: gnome-utils-2.0.5-pam.patch
Patch1: gnome-utils-2.12.2-pam_pwdb.patch
Patch2: gnome-utils-gfloppy-device.patch
# (fc) 2.19.92-2mdv unmount floppy before trying for format them (Mdv bug #24590)
Patch4: gnome-utils-2.19.92-unmount-floppy.patch
#(blino) remove icon extension in gnome-dictionary desktop file (Gnome #558980)
Patch5: gnome-utils-2.24.1-iconext.patch
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
BuildRequires:	pam-devel
BuildRequires:	usermode
BuildRequires:  scrollkeeper
BuildRequires:	gnome-doc-utils
#BuildRequires:  gtk-doc
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
#needed for gfloppy
BuildRequires:  e2fsprogs-devel
BuildRequires:  hal-devel

Requires: usermode-consoleonly
Requires: usermode 
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
%patch0 -p1 -b .pam
%patch1 -p1 -b .pam_pwdb
%patch2 -p0 -b .device
%patch4 -p1 -b .unmount-floppy
%patch5 -p1 -b .iconext

%build

%configure2_5x --enable-console-helper --enable-gfloppy \
 --enable-hal

%make

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std
rm -rf %buildroot/var

%{find_lang} %{name}-2.0 --with-gnome --all-name
for omf in %buildroot%_datadir/omf/*/{*-??,*-??_??}.omf ;do
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed s!%buildroot!!)" >> %name-2.0.lang
done


mkdir -p $RPM_BUILD_ROOT/%{_iconsdir}
mkdir -p $RPM_BUILD_ROOT/%{_liconsdir}
mkdir -p $RPM_BUILD_ROOT/%{_miconsdir}
cp %{SOURCE10} $RPM_BUILD_ROOT/%{_liconsdir}/gdict.png
cp %{SOURCE11} $RPM_BUILD_ROOT/%{_iconsdir}/gdict.png
cp %{SOURCE12} $RPM_BUILD_ROOT/%{_miconsdir}/gdict.png
cp %{SOURCE13} $RPM_BUILD_ROOT/%{_liconsdir}/gfloppy.png
cp %{SOURCE14} $RPM_BUILD_ROOT/%{_iconsdir}/gfloppy.png
cp %{SOURCE15} $RPM_BUILD_ROOT/%{_miconsdir}/gfloppy.png
cp %{SOURCE22} $RPM_BUILD_ROOT/%{_liconsdir}/gnome-searchtool.png
cp %{SOURCE23} $RPM_BUILD_ROOT/%{_iconsdir}/gnome-searchtool.png
cp %{SOURCE24} $RPM_BUILD_ROOT/%{_miconsdir}/gnome-searchtool.png
cp %{SOURCE34} $RPM_BUILD_ROOT/%{_liconsdir}/logview.png
cp %{SOURCE35} $RPM_BUILD_ROOT/%{_iconsdir}/logview.png
cp %{SOURCE36} $RPM_BUILD_ROOT/%{_miconsdir}/logview.png

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
%{_sysconfdir}/gconf/schemas/logview.schemas
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%_bindir/baobab
%_bindir/gfloppy
%_bindir/gnome-dictionary
%_bindir/gnome-panel-screenshot
%_bindir/gnome-screenshot
%_bindir/gnome-search-tool
%_bindir/gnome-system-log
%{_sbindir}/*
%{_libdir}/bonobo/servers/*
%{_datadir}/applications/*
%{_datadir}/baobab/
%{_datadir}/gnome-screenshot
%{_datadir}/gnome-utils
%{_datadir}/gnome-system-log
%{_datadir}/gnome-2.0/ui/*
%_libexecdir/gnome-dictionary-applet
%_datadir/gdict*
%{_datadir}/gnome-dictionary/
%dir %{_datadir}/omf/*
%{_datadir}/omf/*/*-C.omf
%_datadir/icons/hicolor/*/apps/*
%{_mandir}/*/*
%{_liconsdir}/*.png
%{_iconsdir}/*.png
%{_miconsdir}/*.png
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
