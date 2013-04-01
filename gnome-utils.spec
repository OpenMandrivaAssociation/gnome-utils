%define api 1.0
%define major 6
%define libname %mklibname gdict %{api} %{major}
%define develname %mklibname -d gdict %{api}

Summary: GNOME utility programs such as file search and calculator
Name: gnome-utils
Epoch: 1
Version: 3.2.1
Release: 1
License: GPLv2+ and GFDL
Group:  Graphical desktop/GNOME
URL: http://www.gnome.org/softwaremap/projects/gnome-utils/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.xz

BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
#BuildRequires:	pkgconfig(ice)
BuildRequires:	libice-devel
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)

%description
GNOME is the GNU Network Object Model Environment. This powerful
environment is both easy to use and easy to configure.

GNOME Utilities is a collection of small applications all there to make
your day just that little bit brighter - System Log Viewer, 
Search Tool, Dictionary.

%package -n %{libname}
Group: System/Libraries
Summary: GNOME dictionary shared library

%description -n %{libname}
This is the shared library required by the GNOME Dictionary.

%package -n %{develname}
Group: Development/C
Summary: GNOME dictionary library development files
Requires: %{libname} = %{EVRD}
Provides: libgdict1.0-devel = %{EVRD}

%description -n %{develname}
This is the shared library required by the GNOME Dictionary.

%prep
%setup -q
#fix gnome-doc-utils check
perl -p -i -e 's/gdu_cv_version_required=0.3.2/gdu_cv_version_required=0.20.2/' configure
%build
%configure2_5x \
	--disable-static \
	--disable-scrollkeeper \
	--disable-schemas-install

%make LIBS='-lgmodule-2.0 -lgthread-2.0'

%install
rm -rf %{buildroot}
%makeinstall_std
rm -rf %{buildroot}/var
rm -fv %{buildroot}%{_bindir}/test-reader

# make gnome-system-log use consolehelper until it starts using polkit
./mkinstalldirs %{buildroot}%{_sysconfdir}/pam.d
/bin/cat <<EOF >%{buildroot}%{_sysconfdir}/pam.d/gnome-system-log
#%%PAM-1.0
auth		include		system-auth
account		include		system-auth
session		include		system-auth
EOF

./mkinstalldirs %{buildroot}%{_sysconfdir}/security/console.apps
/bin/cat <<EOF >%{buildroot}%{_sysconfdir}/security/console.apps/gnome-system-log
USER=root
PROGRAM=/usr/sbin/gnome-system-log
SESSION=true
FALLBACK=true
EOF

./mkinstalldirs %{buildroot}%{_sbindir}
/bin/mv %{buildroot}%{_bindir}/gnome-system-log %{buildroot}%{_sbindir}
/bin/ln -s /usr/bin/consolehelper %{buildroot}%{_bindir}/gnome-system-log

%{find_lang} %{name}-2.0 --with-gnome --all-name


%files -f %{name}-2.0.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%{_sysconfdir}/security/console.apps/gnome-system-log
%{_sysconfdir}/pam.d/gnome-system-log
%{_sysconfdir}/gconf/schemas/gnome-search-tool.schemas
%{_bindir}/baobab
%{_bindir}/gnome-dictionary
%{_bindir}/gnome-font-viewer
%{_bindir}/gnome-panel-screenshot
%{_bindir}/gnome-screenshot
%{_bindir}/gnome-search-tool
%{_bindir}/gnome-system-log
%{_bindir}/gnome-thumbnail-font
%{_sbindir}/gnome-system-log
%{_datadir}/applications/*
%{_datadir}/baobab/
%{_datadir}/GConf/gsettings/gnome-screenshot.convert
%{_datadir}/GConf/gsettings/logview.convert
%{_datadir}/gdict*
%{_datadir}/glib-2.0/schemas/org.gnome.baobab.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.dictionary.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-screenshot.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-system-log.gschema.xml
%{_datadir}/gnome-dictionary/
%{_datadir}/gnome-screenshot
%{_datadir}/gnome-utils
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/pixmaps/*
%{_datadir}/thumbnailers/gnome-font-viewer.thumbnailer
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libgdict-%{api}.so.%{major}*

%files -n %{develname}
%{_libdir}/libgdict*.so
%{_libdir}/pkgconfig/gdict*.pc
%{_datadir}/gtk-doc/html/gdict
%{_includedir}/gdict*

